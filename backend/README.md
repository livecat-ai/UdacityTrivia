# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<category_id>/questions'
POST '/questions'
DELETE '/questions/<item_id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


GET '/questions'
- Fetches a paginated list of questions (10 questions per page)
- Returns a json object:
            {
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'categories': categories,
            'current_category': None
            }
    Where paginated_questions is a list of Question objects as defined in model.py

- Usage example:    curl -X GET localhost:5000/questions&page=1 - to get the first 10 questions
                    curl -X GET localhost:5000/questions&page=5 - to get the fifth page of questions
- Error: 404 if no books are found.


GET '/categories/<category_id>/questions'
- Fetches a list of question within a specified category
- Returns a json object:
        {
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': category
        }
    Where questions is a list of question objects as defined in models.py
    and currentCategory is a category id.
- Usage example:    curl -X GET localhost:5000/categories/1/questions'
- Error: 400 if the query is badly formed


DELETE '/questions/<item_id>'
- Deletes an row in the question database table equal to item_id
- Returns {'success': True}
- Usage example: curl -X DELETE localhost:5000/questions/10 - Delete item 10 in the questions table
- Error:    404 if item_id doesn't exist
            400 if the request is badly formed


POST '/questions'
- Add a new question to the question table
- Requirs a json object in the form:
        {
            'question': "question text",
            'answer': "answere text,
            'category': category_id(int),
            'difficulty': difficulty level(int)
        }
- Returns: 
        {
            'success': True,
            'created': item_id,
            'questions': questions
        }
    Where question is a list of question objects
- Usage Example:  curl -X POST -H "Content-Type: application/json" \
                            -d '{'question': "question text",
                                'answer': "answere text,
                                'category': category_id(int),
                                'difficulty': difficulty level(int)}' \
                                localhost:5000/questions
- Error: 500 if request can't be processed
        


POST '/questions/search'
- Searches and returns a list of questions given a search term
- Requires a json object in the form: {'searchTerm': query_text}
- Returns: {
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': None
        }
    Where questions is a list of questions that match the query
- Usage Example: curl -X POST -H "Content-Type: application/json" \
                            -d '{'searchTerm': "and"} \
                            localhost:5000/questions/search
- Error: 404 if no questions match the search pattern.

GET '/categories/<category_id>/questions'


POST '/quizzes'
- Fetches a random question from a category if specified or the whole database if category=0.
    Once the quetion is asked it won't be asked again in the current game
- Requires a json object in the form: {'previous_questions': <list of previous questions ids>, 
                                        "quiz_category": {'type': 'Geography', 'id': '3'}
- Returns: {'success': True, 'question': question}
- Error: 500 if the request can't be processed
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```