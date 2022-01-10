## URL where the application is hosted



## Instructions to set up authentication


## Run the app

* Create and start a virtual environment
* Set up environment variables by executing:
````
chmod +x setup.sh
source setup.sh
```` and test the environment variables, e.g. `echo $DATABASE_URL`

* Install requirements and run app 
````
pip install -r requirements.txt
python3 app.py
````
--> app should now run on `http://10.12.21.79:8080/`


* Add actor and movie table to postgres database (user postgres) and add data
````
psql postgres < db.sql
`````

* Create database for testing the app
````
createdb capstone_test
psql capstone_test < db.sql
````
