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
        self.database_path = 'postgresql://{0}:{1}@{2}/{3}'.format("postgres","password","localhost:5432","trivia_test")

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_category_list(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['categories'])

    def test_404_get_categories_not_found(self):
        res = self.client().get('/categories/8')
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'resource not found')

    def test_get_questions_list(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_get_questionpage_not_found(self):
        res = self.client().get('/questions/page=10')
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'resource not found')
        
    def test_new_question(self):
        new_question={
            'category':6,
            'question':'Which is national sport of India?',
            'answer':'Hockey',
            'difficulty':'2'
        }

        res = self.client().post('/questions',json=new_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])

    def test_new_question_bad_request(self):
        new_test_question={
            'question':'what is capital of India?',
            'answer':'New Delhi',
            'difficulty':'1'
        }

        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['message'],'bad request')

    

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['deleted'])
        self.assertTrue(data['total_questions'])

    
    def test_delete_question_not_found(self):
        res = self.client().delete('/questions/abc')
        data = json.loads(res.data)

        self.assertEqual(data['success'],False)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'resource not found')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()