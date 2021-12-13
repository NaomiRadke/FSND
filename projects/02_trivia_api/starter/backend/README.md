# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Endpoints

**GET '/categories'**

- Fetches a list of categories in which the keys are the ids and the value is the corresponding string of the category
- Request arguments: None
- Returns: A dictionary of categories with id:type key value pair. 
- Sample Request: `curl -X GET localhost:5000/categories`
- Sample Response: 
```bash
"categories":{ '1' : "Science", '2' : "Art", '3' : "Geography", '4' : "History", '5' : "Entertainment", '6' : "Sports" }, "success":true,
```


**GET '/questions'**

- Fetches an array of questions in the current category, their answer, category, difficulty and id.
- Request arguments: None
- Returns: List of categories, current category, number of total questions in the current category and an array of all questions in the current category. 
- Sample Request: `curl -X GET http://127.0.0.1:5000/categories
- Sample Response: 

```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "Sports", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
 ```


**GET '/categories/<cat_id>/questions'**

- Fetches an array of questions in the specified category, with their answers and difficulty levels.
- Request arguments: category id
- Returns: Current category, number of questions in the current category and an array of all questions in the current category. 
- Sample Request: `curl -X GET http://127.0.0.1:5000/categories/3/questions`
- Sample Response: 

```bash
{
  "current_category": "Geography", 
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

**POST '/questions/add'**

- Adds a new question to the list of questions in frontend and database
- Request arguments: Question, category, answer and difficulty level
- Returns: Result of the request 
- Sample Request: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{ "question":"new?", "answer":"this", "difficulty":3, "category":2}'` 
- Sample Response: `"success":true`

**POST '/questions/search'**

- Search for questions based on a search term
- Request arguments: search term
- Returns: Questions that match the search term. 
- Sample Request: `curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm":"movie"}'`
- Sample Response: 
```bash
{
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

**DELETE '/questions/<qn_id>'**

- Deletes the question of a given id
- Request argument: question id
- Returns: Result of the request 
- Sample Request: `curl -X DELETE http://127.0.0.1:5000/questions/2`
- Sample Response: `{"deleted": 2, "success": true}`


**POST '/quizzes'**

- Randomly fetches a question from a specified category. If no category is specified.
- Request argument: Previous questions, quiz category
- Returns: Question with answer and difficulty level 
- Sample Request: `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category": {"type": "History", "id": 4}, "previous_questions":[2]}'`
- Sample Response: question": 
```bash
{
  "question": {
    "answer": "George Washington Carver", 
    "category": 4, 
    "difficulty": 2, 
    "id": 12, 
    "question": "Who invented Peanut Butter?"
  }, 
  "success": true
}
````






## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
