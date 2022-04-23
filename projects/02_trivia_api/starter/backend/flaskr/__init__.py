import os
from unicodedata import category
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def pagination(request,question_list):
  pages = request.args.get('page',1,type=int)
  start_page = (pages - 1) * QUESTIONS_PER_PAGE
  end_page = start_page + QUESTIONS_PER_PAGE
  formatted_questions = [question.format() for question in question_list]
  return formatted_questions[start_page:end_page]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):

    response.headers.add('Access-Control-Allow-Headers','Content-type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,PATCH,POST,DELETE')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    category_list = Category.query.all()
    #formatted_categories = [category.format() for category in category_list]

    return jsonify({
      'success':True,
      'categories':{category.id: category.type for category in category_list}
      #'categories':[category.type for category in Category.query.all()]
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def retrieve_questions():
    questions_list = Question.query.all()
    display_list = pagination(request,questions_list)
    categories = Category.query.all()

    return jsonify({
      'success':True,
      'questions':display_list,
      'total_questions':len(questions_list),
      'current_category': [],
      'categories': {category.id: category.type for category in categories}
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>',methods=['DELETE'])
  def delete_question(id):
    question = Question.query.filter(Question.id == id).one_or_none()
    question.delete()
    questions_list = Question.query.all()
    display_list = pagination(request,questions_list)
    categories = Category.query.all()

    return jsonify({
      'success':True,
      'questions':display_list,
      'total_questions':len(questions_list),
      'deleted': id,
      'current_category': [],
      'categories': {category.id: category.type for category in categories}
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
  @app.route('/questions',methods=['POST'])
  def add_question():
    body = request.get_json()

    added_category = body.get('category')
    added_question = body.get('question')
    added_answer = body.get('answer')
    added_difficulty = body.get('difficulty')
    
    new_question = Question(category=added_category, question=added_question, 
                        answer=added_answer, difficulty=added_difficulty)
    new_question.insert()

    #questions_list = Question.query.all()
    questions_list = pagination(request, Question.query.order_by(Question.id).all())

    return jsonify({
      'success': True,
      'questions': questions_list,
      'total_questions': len(Question.query.all()),
      'created': new_question.id,
    })
  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/find',methods=['POST'])
  def find_question():

    data = request.get_json()
    search_key = data.get('searchTerm')

    questions_filtered = Question.query.filter(Question.question.ilike
                                                  (f'%{search_key}%')).order_by(Question.id).all()
    questions_list = pagination(request, questions_filtered)

    return jsonify({
      'success':True,
      'currentCategory': None,
      'questions': questions_list,
      'total_questions': len(questions_filtered),
    })
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_for_category(id):

    questions_filtered = Question.query.filter(Question.category == id).order_by(Question.id).all()

    questions_list = pagination(request, questions_filtered)

    current_category = Category.query.get(id).type

    return jsonify({
      'success':True,
      'current_category': current_category,
      'questions': questions_list,
      'total_questions':len(questions_filtered),

    })

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
  @app.route('/quizzes',methods=['POST'])
  def get_quiz_questions():

    data = request.get_json()

    category = data.get('quiz_category')
    prev_questions = data.get('previous_questions')


    if(category['id'] != 0):
      category_id = category['id']
      quizz_questions = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    else: 
      quizz_questions = Question.query.order_by(Question.id).all()

    display_question = random.choice(quizz_questions).format()

    while display_question['id'] in prev_questions:
      display_question = random.choice(quizz_questions).format()

    return jsonify({
      'success':True,
      'question':display_question
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }), 500

  return app

