# Capstone Project: The Casting Agency
The Casting Agency offers an API to manage actor and movie data. Users can view existing actor and movie data and, depending on their role and privileges, can add, update and delete data.
The API connects to a PostgreSQL database and uses a Flask server.
The API can either be accessed via an external URL or run locally. Both alternatives are outlined below.


## URL for the hosted API
https://capstoneproject79117.herokuapp.com/

## Run the app locally
In case you would like to run the app locally, please follow these steps:

### Clone a local copy of this repo
Fork this repo to your own Github profile and clone locally by navigating to the local directory you want to clone it to and then by running
````
git clone <URL to repo>
````

### Install Python and PostgreSQL
In case you don't have Python and PostgreSQL installed:
* Install Python (latest version) (https://www.python.org/downloads/)
* Install PostgreSQL (https://www.postgresql.org/download/) 


### Create and start a virtual machine
If you don't have the Python `virtualenv` package installed, run: `pip3 install virtualenv``
Then create a new virtual environment (called `env` in this case, but feel free to choose another name) and activate it:
````
python3 -m venv env
source env/bin/activate
````

### Install all required dependencies
````
pip install -r requirements.txt
````

### Setup authentication
Some of the endpoints require authentication since they can only be access vy users with a certain role and corresponing privileges. Roles for this API have been set up on Auth0 (https://auth0.com/)

### Setup database 
Create a new database called `capstone` and populate it with data from the db.sql file by running:
````
createdb capstone
psql capstone < db.sql
````
Adapt the `DATABASE_URL` in the setup.sh file, replacing `naomiradke` with your default postgres user name.

### Run the development server
Set the environment variables and run the server:
````
chmod +x setup.sh # make setup.sh executable
source setup.sh # set the environment variables
python3 app.py # run the app



## API endpoints
The API has the following endpoints to query, extend, update and delete the actor and movie data.

### GET /actors
* Fetches a list of all actors in the database by id, name, age and gender
* Expected return format:
````
{
  "actors": [
    {
      "age": 15, 
      "gender": "W", 
      "id": 1, 
      "name": "Tweety"
    }, 
    {
      "age": 44, 
      "gender": "W", 
      "id": 2, 
      "name": "Sarah B"
    }, 
    {
      "age": 14, 
      "gender": "M", 
      "id": 3, 
      "name": "Roy Black"
    }, 
    {
      "age": 35, 
      "gender": "W", 
      "id": 4, 
      "name": "Hannah Holy"
    }, 
    {
      "age": 45, 
      "gender": "W", 
      "id": 5, 
      "name": "Jane Austin"
    }
  ], 
  "success": true
}
````


### GET /actors/<int:actor_id>
* Fetches an actor of a certain id
* Returns its id, name, age and gender
* Expected return format:

````
{
  "actor": [
    {
      "age": 15, 
      "gender": "W", 
      "id": 1, 
      "name": "Tweety"
    }
  ], 
  "success": true
}
````

### PATCH /actors/<int:actor_id>
* Updates an actor database entry of a given id
* Expected return format:
````
{
    "success": true,
    "updated": 1
}
````

### DELETE /actors/<int:actor_id>
* Deletes an actor database entry of a given id
* Expected return format:
````
{
    "deleted": 1,
    "success": true
}
````

### POST /actors
* Post a new actor to the database
* Requires a body in json format giving details on name, age and gender, for example:
````
{
    "name": "The new one",
    "age": 20,
    "gender": "F"
}
````
* Expected return format:
````
{
    "created": 6,
    "success": true,
    "total_actors": 5
}
````

### GET /movies
* Fetches a list of all movies in the database by id, title and release date
* Expected return format:
````
{
  "movies": [
    {
      "id": 1, 
      "release_date": "Wed, 03 Apr 2019 23:00:00 GMT", 
      "title": "The Mountains"
    }, 
    {
      "id": 2, 
      "release_date": "Fri, 02 Aug 2013 23:00:00 GMT", 
      "title": "The River"
    }, 
    {
      "id": 3, 
      "release_date": "Thu, 13 Feb 2020 23:00:00 GMT", 
      "title": "Fun Facts"
    }
  ], 
  "success": true
}
````


### GET /movies/<int:movie_id>
* Fetches a movie of a certain id
* Returns its id, title and release date
* Expected return format:

````
{
  "movie": [
    {
      "id": 2, 
      "release_date": "Fri, 02 Aug 2013 23:00:00 GMT", 
      "title": "The River"
    }
  ], 
  "success": true
}
````

### PATCH /movies/<int:movie_id>
* Updates a movie database entry of a given id
* Expected return format:
````
{
    "success": true,
    "updated": 1
}
````

### DELETE /movies/<int:movie_id>
* Deletes a movie database entry of a given id
* Expected return format:
````
{
    "deleted": 1,
    "success": true
}
````

### POST /movies
* Post a new movie to the database
* Requires a body in json format giving details on title and release date, for example:
````
{
    "title": "The new one",
    "release_date": "1980-05-04 00:00:00"
}
````
* Expected return format:
````
{
    "created": 5,
    "success": true,
    "total_movies": 5
}
"""


## Roles (RBAC)
To allow certain operations on the API to certain persons, we set two different roles with different privileges regarding operations on the API endpoints. So certain endpoints require authentication to make sure the user has the privileges for operating the endpoints.

The *GET* endpoints do not require any authentication.
We set 2 roles with the corresponding privileges:
* Casting director:
  * DELETE actors
  * POST actors
  * PATCH actors + movies

* Executive producer:
  * DELETE actors + movies
  * POST actors + movies
  * PATCH actors + movies



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


