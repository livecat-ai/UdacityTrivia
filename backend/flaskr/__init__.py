import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Helper functions


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [questions.format() for questions in selection]
    current_questions = questions[start:end]
    return current_questions


def is_valid_int(item):
    # if it's a valid number it can be converted to float
    try:
        item = float(item)
    except BaseException:
        return False
    # check if it's really an int
    if (item - round(item)) != 0:
        return False
    return True
# End helper functions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins.
        Delete the sample route after completing the TODOs
  '''
    CORS(app, rescourses={r"/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Autorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE')
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = {
            category.id: category.type for category in Category.query.all()}
        body = {
            'success': True,
            'categories': categories
        }
        return jsonify(body)

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of
  the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginate_questions(request, questions)

        categories = {
            category.id: category.type for category in Category.query.all()}
        if len(paginated_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'categories': categories,
            'current_category': None
        })
    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
  the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<item_id>', methods=['DELETE'])
    def delete_question(item_id):
        if is_valid_int(item_id):
            item_id = int(item_id)
        else:
            abort(400)

        query = Question.query.get(item_id)
        if query is None:
            abort(404)
        else:
            query.delete()

        return jsonify({
            'success': True,
        })

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        data = request.get_json()
        question = Question(question=data['question'],
                            answer=data['answer'],
                            category=data['category'],
                            difficulty=data['difficulty'])
        question.insert()
        item_id = 1
        questions = [question.format() for question in Question.query.all()]
        body = {
            'success': True,
            'created': item_id,
            'questions': questions
        }
        return jsonify(body)
    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        term = request.get_json()['searchTerm']
        search_results = Question.query.filter(
            Question.question.like(f'%{term}%')).all()
        questions = paginate_questions(request, search_results)

        if len(questions) == 0:
            abort(404)

        body = {
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': None
        }
        return jsonify(body)

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def list_questions_in_category(category_id):
        if is_valid_int(category_id):
            category_id = int(category_id)
        else:
            abort(400)

        query = Question.query.filter(Question.category == category_id)
        questions = paginate_questions(request, query)
        category = Category.query.get(category_id).format()
        body = {
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': category
        }
        return jsonify(body)

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        data = request.get_json()
        previous_questions = data.get('previous_questions', None)
        category_id = data.get('quiz_category', None)['id']
        # print(f"category_id type from json body: {type(category_id)}")
        # print(category_id)
        if category_id == 0:
            query = Question.query.filter(
                Question.id.notin_(previous_questions)).all()
        else:
            query = Question.query.filter(
                Question.category == category_id).filter(
                Question.id.notin_(previous_questions)).all()
        if query:
            question = random.choice(query).format()
        else:
            question = None
        body = {
            'success': True,
            'question': question,
        }
        return jsonify(body)
    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        })

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app

