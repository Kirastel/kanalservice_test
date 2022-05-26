# Instructions for setting up and launching the application.

Clone the repository: 
```
git clone https://github.com/Kirastel/kanalservice_test.git && cd kanalservice_test
```
Create a virtual environment: 
```
python3 -m venv venv
```
Activate the virtual environment: 
```
source venv/bin/activate
```
## Deploying a Docker container: 
Create a image:
```
docker build .
```

Build a new image and run two containers:
```
docker-compose up -d --build
```

## Run without docker:
Install all required dependencies:
```
pip install -r requirements.txt
```

Run app:
```
script.py
```

