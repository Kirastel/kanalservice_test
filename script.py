import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import psycopg2
import schedule
from dollar import dollar_exchange_rate


def get_data():
    """
    The function returns the data received from the google sheets API
     as a list with tuples.
    """

    # File received in Google Developer Console
    CREDENTIALS_FILE = 'creds.json'
    # Document Google Sheets ID (from its URL)
    spreadsheet_id = '1m5xOYpGZs9Oy3qS-bS23K0K-UHSMUdxBo3s7DpFV3DU'

    # Authorization and getting service - API access instance
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Reading a file
    data_from_sheets = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Page1',
        majorDimension='ROWS'
    ).execute()

    dollar_exchange = dollar_exchange_rate()

    data = []
    for value in data_from_sheets['values'][1:]:
        num = int(value[0])
        order = int(value[1])
        price_dol = int(value[2])
        price_rub = int(price_dol * dollar_exchange)
        date = datetime.strptime(value[3], "%d.%m.%Y").date()
        data.append((num, order, price_dol, price_rub, date))

    return data


def put_in_bd(data: (list, tuple)):
    """
    The function takes a list or tuple with data as an argument
    and enters them into the database.
    """

    try:
        conection = psycopg2.connect(
            database="google_sheets",
            user="postgres",
            password="admin",
            host="127.0.0.1",
            port="5432"
        )

        conection.autocommit = True

        with conection.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS orders(
                                                № serial NOT NULL PRIMARY KEY,
                                                order_№ INTEGER,
                                                price_$ INTEGER,
                                                price_rub INTEGER,
                                                date_delivery timestamp
                                                );
                                                ''')

            insert_query = ("""INSERT INTO orders(№, order_№, price_$, price_rub, date_delivery)
                               VALUES (%s, %s, %s, %s, %s)
                               ON CONFLICT (№) DO UPDATE
                               SET order_№ = excluded.order_№,
                                    price_$ = excluded.price_$,
                                    price_rub = excluded.price_rub,
                                    date_delivery = excluded.date_delivery;
                                   """)

            cursor.executemany(insert_query, data)


    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)


def main():
    data = get_data()
    put_in_bd(data)
    print('[INFO] Successfully!')


if __name__ == "__main__":
    schedule.every(1).minutes.do(main)
    while True:
        schedule.run_pending()
