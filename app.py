import random
from flask import Flask, request
from pymessenger.bot import Bot
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from datetime import datetime
import os
import questions


app = Flask(__name__)
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
    last_timestamp = db.Column(db.String(120))
    fractions_in_progress = db.Column(db.Boolean())
    quadratics_in_progress = db.Column(db.Boolean())
    question_number = db.Column(db.Integer)

    def __init__(self, user_id, last_timestamp, fractions_in_progress = False, quadratics_in_progress = False, question_number = 0):
        self.user_id = user_id
        self.last_timestamp = last_timestamp
        self.fractions_in_progress = fractions_in_progress
        self.quadratics_in_progress = quadratics_in_progress
        self.question_number = question_number

    def __repr__(self):
        return '<User ID %r>' % self.user_id

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
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
                        bot.send_text_message(recipient_id, "Welcome. You can...")
                        insert = User(recipient_id, str(datetime.now())[:19])
                        db.session.add(insert)
                        db.session.commit()
                    else:
                        user = User.query.filter_by(user_id=recipient_id).first()

                        if abs(datetime.now() - datetime.strptime(user.last_timestamp, '%Y-%m-%d %H:%M:%S')).seconds > 600:
                            bot.send_text_message(recipient_id, "You've been away for a while! Start again...")
                            reset(user)

                        if 'quick_reply' in message['message']:
                            payload = message['message']['quick_reply']['payload']
                            print("payload is: " + str(payload))

                            if user.fractions_in_progress:
                                if payload == 'correct':
                                    bot.send_text_message(recipient_id, "Well done!")
                                    send_fractions_question(recipient_id)
                                else:
                                    bot.send_text_message(recipient_id, "Not quite...")

                            if payload == "fractions":
                                print(user.fractions_in_progress)
                                user.fractions_in_progress = True
                                db.session.commit()
                                send_fractions_question(recipient_id)
                            elif payload == "help":
                                send_help(recipient_id)
                            elif payload == "quadratic_equations":
                                user.quadratics_in_progress = True
                                db.session.commit()
                                send_quadratics_questions(recipient_id)

                        else:
                            welcome_screen(recipient_id)
                # if message['message'].get('text'):
                #     response_sent_text = get_message()
                #     send_message(recipient_id, response_sent_text)
                # #if user sends us a GIF, photo,video, or any other non-text item
                # if message['message'].get('attachments'):
                #     response_sent_nontext = get_message()
                #     send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def send_fractions_question(recipient_id):
    question = questions.questiontype1()
    quick_reply = []
    for option in question['options']:
        if question['answer'] == option:
            quick_reply.append((option, 'correct'))
        else:
            quick_reply.append((option, 'incorrect'))

    send_quick_reply(recipient_id, question['question'], quick_reply)


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["$$x+2 = 3$$"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def welcome_screen(recipient_id):
    user_name = get_user_info(recipient_id, fields='first_name')
    print(user_name)
    welcome_string = "Hi there, " + "Zain" + ". What would you like to do?"
    #bot.send_text_message(recipient_id, welcome_string)
    return send_quick_reply(recipient_id, welcome_string, [("Fractions", "fractions"), ("Quadratic Equations", "quadratic_equations"), ("Help", "help")])

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

def get_user_info(self, recipient_id, fields=None):
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

        params.update(self.auth_args)

        request_endpoint = '{0}/{1}'.format(self.graph_url, recipient_id)
        response = requests.get(request_endpoint, params=params)
        if response.status_code == 200:
            return response.json()

        return None

def send_help(recipient_id):
     pass


if __name__ == "__main__":
    app.run(host='0.0.0.0')