import random
from flask import Flask, request
from pymessenger.bot import Bot
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from datetime import datetime
import os


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

    def __init__(self, user_id, last_timestamp):
        self.user_id = user_id
        self.last_timestamp = last_timestamp

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
                if not db.session.query(User).filter(User.user_id == recipient_id).count():
                    bot.send_text_message(recipient_id, "Welcome, we've added you to our database at time " + str(datetime.now()))
                    insert = User(recipient_id, datetime.now())
                    db.session.add(insert)
                    db.session.commit()
                else:
                    bot.send_text_message(recipient_id, "Hi, you're already a user. Welcome back! :)")
                # if message['message'].get('text'):
                #     response_sent_text = get_message()
                #     send_message(recipient_id, response_sent_text)
                # #if user sends us a GIF, photo,video, or any other non-text item
                # if message['message'].get('attachments'):
                #     response_sent_nontext = get_message()
                #     send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


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

if __name__ == "__main__":
    app.run(host='0.0.0.0')