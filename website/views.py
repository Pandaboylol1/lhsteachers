from flask import Blueprint, render_template, request, flash, jsonify
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from .models import Invite, Game, User, Review, Rating, Teacher
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
  if request.method == 'POST':
    if request.form.get('invite_id') != None:
      teacher = int(request.form.get('invite_id'))
      teacher = Teacher.query.filter_by(id=teacher).first()
      user = User.query.filter_by(id=current_user.id).first()
      user.current_teacher_id = teacher.id
      db.session.add(user)
      db.session.commit()
      return render_template("teacherpage.html", user=current_user, teacher=teacher, reviews=teacher.reviews)
    if request.form.get('review') != None:
      print(request.form.get('review') + request.form.get('teacher_id'))
      review = Review(review = request.form.get('review'), teacher_id = int(request.form.get('teacher_id')))
      db.session.add(review)
      db.session.commit()
      flash("Review posted!", category='success')
      teacher = Teacher.query.filter_by(id=current_user.current_teacher_id).first()
      return render_template("teacherpage.html", user=current_user, teacher=teacher, reviews=teacher.reviews)
  # Retrieve all the teachers from the database
  teachers = Teacher.query.all()

  
  
  return render_template("home.html", user=current_user, teachers=teachers)


@views.route('/game', methods=['GET', 'POST'])
@login_required
def game():
  game = Game.query.filter_by(id=current_user.current_game_id).first()
  player1 = User.query.filter_by(email=game.inviter).first()
  player2 = User.query.filter_by(email=game.invitee).first()
  if request.method == 'POST':
    move = request.form.get('move')
    game.data = move
    if game.to_move == 'white':
      game.to_move = 'black'
    else:
      game.to_move = 'white'
    db.session.commit()
  if player1.email == current_user.email:
    opponent = player2
  else:
    opponent = player1
  return render_template("chess.html",
                         user=current_user,
                         game=game,
                         opponent=opponent)


@views.route('/get_fen', methods=['GET'])
def get_fen():

  return jsonify(
    fen=Game.query.filter_by(id=current_user.current_game_id).first().data,
    turn=Game.query.filter_by(id=current_user.current_game_id).first().to_move)


@views.route('/update_position', methods=['POST'])
def update_fen():
  data = request.get_json()
  game_id = data['game_id']
  old_fen = data['oldPos']
  new_fen = data['newPos']
  side = data['orientation']
  if side == Game.query.filter_by(
      id=current_user.current_game_id).first().to_move:
    game = Game.query.filter_by(id=game_id).first()
    game.data = new_fen
    if game.to_move == 'white':
      game.to_move = 'black'
    else:
      game.to_move = 'white'
    db.session.commit()
    # Do something with the FEN string and game ID, such as updating a database or sending it to other clients
  return ''


@views.route('/inbox', methods=['GET', 'POST'])
@login_required
def inbox():
  if request.method == 'POST':
    invite_id = request.form.get('invite_id')
    submit_type = request.form.get('submit')
    if submit_type == 'accept':
      invite = Invite.query.get(invite_id)
      current_user.current_game_id = invite.game_id
      db.session.delete(invite)
      db.session.commit()
      flash('Invite Accepted!', category='success')
      return redirect(url_for('views.game'))
    else:
      invite = Invite.query.get(invite_id)
      game = Game.query.filter_by(id=invite.game_id).first()
      inviter = User.query.filter_by(current_game_id=invite.game_id).first()
      inviter.current_game_id = None
      db.session.delete(invite)
      db.session.delete(game)
      db.session.commit()
      flash('Invite Rejected!', category='error')
  return render_template("inbox.html", user=current_user)
