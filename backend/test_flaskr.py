import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('johnlockwood', 'jal109', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.question_data = {
            'question': 'To be or not to be',
            'answer': 'Now that is a quesion',
            'category': 4,
            'difficulty': 2
            }

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_catagories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_error_get_catagories(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)


    def test_get_404_error_paginated_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_question_by_id(self):
        '''
        Add a new question so that we can delete it
        '''
        query = Question.query.filter(Question.question==self.question_data['question']).first()
        # print(f'query 1 = {query.id}')
        if query == None:
            new_question = Question(self.question_data['question'],
                                    self.question_data['answer'],
                                    self.question_data['category'],
                                    self.question_data['difficulty'])
            new_question.insert()
            query = Question.query.filter(Question.question==self.question_data['question']).first()
            # print(f'query2 = {query.id}')

        res = self.client().delete(f"/questions/{query.id}")
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        query = Question.query.filter(Question.question==self.question_data['question']).first()
        self.assertEqual(query, None)


    def test_404_error_delete_question_by_id(self):
        query = 99999999
        res = self.client().delete(f'/questions/{query}')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_400_error_delete_question_by_id_string(self):
        res = self.client().delete(f'/questions/bad_request')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')


    def test_400_error_delete_question_by_id_float(self):
        res = self.client().delete(f'/questions/1.1')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

        
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.question_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    def test_405_question_creation_not_allowd(self):
        res = self.client().post('/questions/42', json=self.question_data)
        data = json.loads(res.data)

        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    
    def test_search_questions(self):
        query_text = 'title'
        res = self.client().post('/questions/search', json={'searchTerm': query_text})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])


    def test_404_search_questions_not_found(self):
        query_text = "windowsmokestackdirtyloo"
        res = self.client().post('/questions/search', json={'searchTerm': query_text})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_get_questions_in_category(self):
        quiz_data = {
             'previous_questions':[],
            "quiz_category": {'type': 'Geography', 'id': '3'}
            }
        res = self.client().post('/quizzes', data=json.dumps(quiz_data), content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])


    def test_404_get_questions_in_category_not_found(self):
        category = 'Pot Holes'
        res = self.client().post(f'/quizzes/{category}')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_list_questions_in_category(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # #don't test for questions because there might not be any questions in that list yet
        # self.assertTrue(data['question'])
        self.assertGreaterEqual(data['totalQuestions'], 0)
        self.assertTrue(data['currentCategory'])
    
    def test_400_bad_request_list_questions_category(self):
        category_id = 1.2
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request' )


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()