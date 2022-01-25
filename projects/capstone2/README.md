

## Steps

### Setup and fill database
````
createdb postgres # create a database called postgres
psql postgres < db.sql # fill the database with predefined tables and entries
````

### Install dependencies
`pip install -r requirements.txt``


### Files relevant for Heroku deployment
- Procfile
- manage.py
- runtime.txt


### Setup the environment variables
````
chmod +x setup.sh
source setup.sh
````

### Run the app
`python3 app.py``


