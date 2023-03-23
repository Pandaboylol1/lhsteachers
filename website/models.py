from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Game(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.String(99999))
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  inviter = db.Column(db.String(99999))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  invitee = db.Column(db.String(99999))
  to_move = db.Column(db.String(100))
  

class Invite(db.Model):
  email = db.Column(db.String(10000))
  id = db.Column(db.Integer, primary_key=True)
  game_id = db.Column(db.Integer)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  first_name = db.Column(db.String(150))
  invites = db.relationship('Invite')
  current_game_id =db.Column(db.Integer)
  current_teacher_id = db.Column(db.Integer)

class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  review = db.Column(db.String(99999))
  teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

class Rating(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  review = db.Column(db.Integer())
  teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
  
class Teacher(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(150))
  last_name = db.Column(db.String(150))
  course = db.Column(db.String(150))
  reviews = db.relationship('Review')
  ratings = db.relationship('Rating')