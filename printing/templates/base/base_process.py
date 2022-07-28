from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from printing.models import *
from printing import mail
from flask import url_for

def send_reset_email(email, token):
    msg = Message(subject='Password Reset Request',
                  sender='jeremy@jeremyguill.com',
                  recipients=[email])
    msg.body = f'To reset your password, visit the following link: \n {url_for("base.reset_token", token=token, _external=True)}\n\nIf you did not make this request then simply ignore this email and no changes will be made.'
    mail.send(msg)
    
def get_reset_token(userid, expires_sec=1800):
        s = Serializer(os.environ.get('SECRET_KEY'), expires_sec)
        return s.dumps({'user_id': userid}).decode('utf-8')

def verify_reset_token(token):
    s = Serializer(os.environ.get('SECRET_KEY'))
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return User.query.get(user_id)