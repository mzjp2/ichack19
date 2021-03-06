import random
from flask import Flask, request, jsonify
from pymessenger.bot import Bot
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from datetime import datetime
import os
import questions
import requests
from sqlalchemy.dialects import postgresql
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
ACCESS_TOKEN = 'EAAfnLOamFLkBAOfiSZCw9uScml7VYJ2F172pcZAAtlfE7ZCfdA6Q6U3pHb6sQaE3XSGbQfuNdresz5zRZAWQz0hY1jSOJxsukudGngzeE44OxHI7g2LBmxLKFA7h8ZBG6K9umSAjras8H3tuf9UbJiROdnFayaGAylotLAq4IdgZDZD'
VERIFY_TOKEN = 'SSA19'
heroku = Heroku(app)
bot = Bot(ACCESS_TOKEN)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), unique=True)
    user_first_name = db.Column(db.String(120))
    user_last_name = db.Column(db.String(120))
    last_timestamp = db.Column(db.String(120))
    fractions_in_progress = db.Column(db.Boolean())
    quadratics_in_progress = db.Column(db.Boolean())
    question_number = db.Column(db.Integer())
    num_fractions_questions = db.Column(db.Integer())
    num_quadratics_questions = db.Column(db.Integer())
    num_correct_fractions_questions = db.Column(db.Integer())
    num_correct_quadratics_questions = db.Column(db.Integer())
    prev_q = db.Column(db.String(240))
    comment_flag = db.Column(db.Boolean())
    comment = db.Column(db.String())
    

    def __init__(self, user_id, last_timestamp, user_first_name, user_last_name, fractions_in_progress = False, quadratics_in_progress = False, question_number = 0, num_fractions_questions = 0, num_quadratics_questions = 0, num_correct_fractions_questions = 0, num_correct_quadratics_questions = 0, prev_q = "", comment_flag = False, comment=""):
        self.user_id = user_id
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.last_timestamp = last_timestamp
        self.fractions_in_progress = fractions_in_progress
        self.quadratics_in_progress = quadratics_in_progress
        self.question_number = question_number
        self.num_fractions_questions = num_fractions_questions
        self.num_quadratics_questions = num_quadratics_questions
        self.num_correct_fractions_questions = num_correct_fractions_questions
        self.num_correct_quadratics_questions = num_correct_quadratics_questions
        self.prev_q = prev_q
        self.comment_flag = comment_flag
        self.comment = comment

    def __repr__(self):
        return '<User ID %r>' % self.user_id

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    global question_prev
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if not recipient_id == '316120302349805':
                    if not db.session.query(User).filter(User.user_id == recipient_id).count():
                        bot.send_text_message(recipient_id, "Welcome. It looks like this is the first time you're using LambdaMaths. A quick introduction: we're an early prototype, built by Team SSA at ICHack19 with the purpose of helping students and teachers collaborate and smooth over the process of doing homework and studying maths in small increments. We also want to make students progress and feedback as transaparent as possible for them. Please send in any message to continue to the main page. Have fun!")
                        user_info = get_user_info(recipient_id, fields='first_name')
                        insert = User(recipient_id, str(datetime.now())[:19], user_info['first_name'], user_info['last_name'])
                        db.session.add(insert)
                        db.session.commit()
                    else:
                        user = User.query.filter_by(user_id=recipient_id).first()
                        user.last_timestamp = str(datetime.now())[:19]

                        if abs(datetime.now() - datetime.strptime(user.last_timestamp, '%Y-%m-%d %H:%M:%S')).seconds > 600:
                            bot.send_text_message(recipient_id, "You've been away for a while! Start again...")
                            reset(user)

                        if user.comment_flag:
                            user.comment = message['message']['text']
                            user.comment_flag = False
                            bot.send_text_message(recipient_id, "Your comment has been sent to your teacher and you'll get help soon! :)")
                            db.session.commit()


                        if 'quick_reply' in message['message']:
                            payload = message['message']['quick_reply']['payload']
                            print("payload is: " + str(payload))

                            if payload == 'summary':
                                ask_summary(recipient_id)
                            elif '-summary' in payload:
                                compute_summary(recipient_id, user, payload)


                            if user.fractions_in_progress:
                                user.num_fractions_questions += 1
                                db.session.commit()
                                if payload == 'correct':
                                    user.num_correct_fractions_questions += 1
                                    db.session.commit()
                                    bot.send_text_message(recipient_id, "Well done!")
                                    send_fractions_question(recipient_id, user)
                                elif payload == 'incorrect':
                                    send_quick_reply(recipient_id, 'Not quite...', [('Comment', 'comment'), ('Next', 'next'), ('Stop', 'stop')])
                                elif payload == 'next':
                                    send_fractions_question(recipient_id, user)
                                elif payload == 'stop':
                                    user.num_fractions_questions -= 1
                                    db.session.commit()
                                    reset(user)
                                elif payload == 'comment':
                                    user.comment_flag = True
                                    db.session.commit()
                                    bot.send_text_message(recipient_id, 'Enter your comment, stating your answer and why you thought it was correct')
                                



                            if user.quadratics_in_progress:
                                user.num_quadratics_questions += 1
                                db.session.commit()
                                if payload == 'correct':
                                    user.num_correct_quadratics_questions += 1
                                    db.session.commit()
                                    bot.send_text_message(recipient_id, "Well done!")
                                    send_quadratics_question(recipient_id, user)
                                elif payload == 'incorrect':
                                    send_quick_reply(recipient_id, 'Not quite...', [('Comment', 'comment'), ('Next', 'next'), ('Stop', 'stop')])
                                elif payload == 'next':
                                    send_quadratics_question(recipient_id, user)
                                elif payload == 'stop':
                                    user.num_quadratics_questions -=1
                                    db.session.commit()
                                    reset(user)
                                elif payload == 'comment':
                                    bot.send_text_message(recipient_id, 'hi')

                            if payload == "fractions":
                                user.fractions_in_progress = True
                                db.session.commit()
                                question_prev = send_fractions_question(recipient_id, user)
                            elif payload == "help":
                                send_help(recipient_id)
                            elif payload == "quadratic_equations":
                                user.quadratics_in_progress = True
                                db.session.commit()
                                send_quadratics_question(recipient_id, user)
                        else:
                            welcome_screen(recipient_id)
    return "Message Processed"

def send_fractions_question(recipient_id, user):
    question = questions.questiontype1()
    quick_reply = []
    for option in question['options']:
        if question['answer'] == option:
            quick_reply.append((option, 'correct'))
        else:
            quick_reply.append((option, 'incorrect'))
    user.question_number += 1
    user.prev_q = question['question']
    db.session.commit()
    send_quick_reply(recipient_id, "Question #" + str(user.question_number) + ": " + question['question'], quick_reply)
    return question

def send_quadratics_question(recipient_id,user):
    question = questions.questiontype2()
    quick_reply = []
    for option in question['options']:
        if question['answer'] == option:
            quick_reply.append((option, 'correct'))
        else:
            quick_reply.append((option, 'incorrect'))
    user.question_number += 1
    user.prev_q = question['question']
    db.session.commit()
    send_quick_reply(recipient_id, "Question #" + str(user.question_number) + ": " + question['question'], quick_reply)


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def welcome_screen(recipient_id):
    user_info = get_user_info(recipient_id, fields='first_name')
    welcome_string = "Hi there, " + user_info['first_name'] + ". What would you like to do?"
    return send_quick_reply(recipient_id, welcome_string, [("Fractions", "fractions"), ("Quadratic Equations", "quadratic_equations"), ("View summary", "summary")])

def send_quick_reply(recipient_id, text, quick_replies):
    quick_replies_array = []
    for quick_reply in quick_replies:
        quick_replies_array.append({"content_type": "text", "title": quick_reply[0], "payload":quick_reply[1]})
    message = {"text": text, "quick_replies": quick_replies_array}
    return bot.send_message(recipient_id, message)

def reset(user):
    user.fractions_in_progress = False
    user.quadratics_in_progress = False
    user.question_number = 0
    db.session.commit()
    welcome_screen(user.user_id)

def get_user_info(recipient_id, fields=None):
        """Getting information about the user
        https://developers.facebook.com/docs/messenger-platform/user-profile
        Input:
          recipient_id: recipient id to send to
        Output:
          Response from API as <dict>
        """
        params = {}
        if fields is not None and isinstance(fields, (list, tuple)):
            params['fields'] = ",".join(fields)

        params.update(bot.auth_args)

        request_endpoint = '{0}/{1}'.format(bot.graph_url, recipient_id)
        response = requests.get(request_endpoint, params=params)
        if response.status_code == 200:
            return response.json()

        return None

def send_help(recipient_id):
     pass

def ask_summary(recipient_id):
    user_info = get_user_info(recipient_id, fields='first_name')
    send_quick_reply(recipient_id, "Hi,  " + user_info['first_name'] + '!' + " What would you like to see?", [('Fractions summary', 'fractions-summary'), ('Quadratics summary', 'quadratics-summary'), ('All summary', 'all-summary')])

def compute_summary(recipient_id, user, payload):
    bot.send_text_message(recipient_id, "Name: " + user.user_first_name + " " + user.user_last_name)
    bot.send_text_message(recipient_id, "Teacher: Matthew A.")
    bot.send_text_message(recipient_id, "Class: Maths -- Year 13, Set 8")

    if payload == 'fractions-summary':
        bot.send_text_message(recipient_id, "You've answered " + str(user.num_correct_fractions_questions) + " questions correctly out of a total of " + str(user.num_fractions_questions))
        bot.send_text_message(recipient_id, 'Predicted grade for fractions: ' + str(questions.gradefunction(user.num_correct_fractions_questions / user.num_fractions_questions * 100)))
    elif payload == 'quadratics-summary':
        bot.send_text_message(recipient_id, "You've answered " + str(user.num_correct_quadratics_questions) + " correctly out of a total of " + str(user.num_quadratics_questions))
        bot.send_text_message(recipient_id, 'Predicted grade for quadratics: ' + str(questions.gradefunction(user.num_correct_quadratics_questions / user.num_quadratics_questions * 100)))
    elif payload == 'all-summary':
        bot.send_text_message(recipient_id, "You've answered " + str(user.num_correct_fractions_questions + user.num_correct_quadratics_questions) + " correctly, out of " + str(user.num_fractions_questions + user.num_quadratics_questions))
        bot.send_text_message(recipient_id, 'Predicted grade: ' + str(questions.gradefunction((user.num_correct_fractions_questions + user.num_correct_quadratics_questions) / (user.num_fractions_questions + user.num_quadratics_questions) * 100)))
    
    send_quick_reply(recipient_id, "What would you like to do now?", [("Fractions", "fractions"), ("Quadratic Equations", "quadratic_equations"), ("View summary", "summary")])



@app.route("/homework", methods=['POST', 'GET'], endpoint='homework')
@cross_origin()
def homework():
    if request.method == 'POST':
        print(request.json['amount'])

    content = request.get_json()
    print(content)
    recipient_id = '1979973702071807'
    bot.send_text_message(recipient_id, "Hi, Chris! Your teacher has asked you to complete " + content['amount'] + " questions on " + content['topic'] + ". This assignment will be at grade " + content['grade'] + " level. Good luck!")
    return 'success'

@app.route("/get_fractions_score", methods=['POST', 'GET'], endpoint='get_fractions_score')
@cross_origin()
def get_fractions_score():
    user = User.query.filter_by(user_id='1979973702071807').first()
    return jsonify(correct_fractions = user.num_correct_fractions_questions, total_fractions = user.num_fractions_questions)

@app.route("/get_quadratics_score", methods=['POST', 'GET'], endpoint='get_quadratics_score')
@cross_origin()
def get_quadratics_score():
    user = User.query.filter_by(user_id='1979973702071807').first()
    return jsonify(correct_quadratics = user.num_correct_quadratics_questions, total_quadratics = user.num_quadratics_questions)

@app.route("/get_total_score", methods=['POST', 'GET'], endpoint='get_total_score')
@cross_origin()
def get_total_score():
    user = User.query.filter_by(user_id='1979973702071807').first()
    return jsonify(correct_questions = user.num_correct_fractions_questions + user.num_correct_quadratics_questions, total_fractions = user.num_fractions_questions + user.num_quadratics_questions)

@app.route("/get_comment", methods=['POST', 'GET'], endpoint='get_comment')
@cross_origin()
def get_total_score():
    user = User.query.filter_by(user_id='1979973702071807').first()
    return jsonify(comment=user.comment)

if __name__ == "__main__":
    app.run(host='0.0.0.0')