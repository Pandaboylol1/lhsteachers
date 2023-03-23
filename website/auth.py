from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Teacher, Review
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
  adminusers = ['nicholasson12@gmail.com', 'dhruv.kulkarni@lps-students.org', 'prakhar.samaiya@lps-students.org', 'gregory232008@gmail.com']
  if request.method == 'POST':
    if request.form.get('deletereview') != None:
      id = request.form.get('deletereview')
      review = Review.query.get(id)
      db.session.delete(review)
      db.session.commit()
    
    if request.form.get('deleteteacher') != None:
      id = request.form.get('deleteteacher')
      teacher = Teacher.query.filter_by(id=id).first()
      db.session.delete(teacher)
      db.session.commit()
      flash("Teacher successfully deleted.", category='success')
    if request.form.get('first_name') != None:
      teacher = Teacher(first_name=request.form.get('first_name'), last_name=request.form.get('last_name'), course= request.form.get('course'))
      db.session.add(teacher)
      db.session.commit()
      flash("Teacher successfully added!", category='success')
    userid = request.form.get('delete')
    user = User.query.get(userid)
    if user:
      if current_user.email == 'nicholasson12@gmail.com':
        db.session.delete(user)
        db.session.commit()
        flash('User successfully deleted!', category='success')
  print(current_user.email)
  if current_user.email in adminusers:
    users = User.query.all()
    user_list = []
    for user in users:
      user_dict = {'id': user.id, 'email': user.email, 'password': user.password, 'first_name': user.first_name}
      user_list.append(user_dict)

    reviews = Review.query.all()
    teachers = Teacher.query.all()
    return render_template("admin.html", user=current_user, user_list = user_list, reviews = reviews, teachers=teachers)
  else:
    return redirect(url_for('views.home'))




@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email').lower()
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        flash('Logged in succesfully!', category = 'success')
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password, please check your spelling and try again.', category = 'error')
    else:
      flash('User with this email does not exist.', category='error')
    
  return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email').lower()
    firstName = request.form.get('firstName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    user = User.query.filter_by(email=email).first()

    if user:
      flash('Email already exists, please log in to your account.', category='error')
      return render_template("sign_up.html")
    
    if len(email) < 4:
      flash('Email must be greater than 3 characters.', category = 'error')
    elif len(firstName) < 2:
      flash('First name must be greater than 1 character.', category = 'error')
    elif password1 != password2:
      flash('Passwords do not match.', category = 'error')
    elif len(password1) < 5:
      flash('Password must be at least 5 characters.', category = 'error')
    else:
      new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))

      db.session.add(new_user)
      db.session.commit()
      flash('Account created!', category='success')
      login_user(new_user, remember=True)
      return redirect(url_for('views.home'))
      
      
  return render_template("sign_up.html", user=current_user)