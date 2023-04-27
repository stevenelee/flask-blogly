"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get('/')
def to_users():
    """redirect to user list"""

    return redirect("/users")


@app.get('/users')
def get_users():
    """display all users"""

    users = User.query.all()

    return render_template("user_list.html", users = users)


@app.get('/users/new')
def display_new_user_form():
    """display new user form"""

    return render_template("new_user_form.html")


@app.post('/users/new')
def handle_new_user():
    """
    creates a new user from the new user form and redirects to the user list

    """

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or None

    # creates instance of User class
    user = User(
        first_name = first_name,
        last_name = last_name,
        image_url = image_url
    )

    # input into database
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.get('/users/<user_id>')
def get_user(user_id):
    """shows information of the given user"""

    user = User.query.get_or_404(user_id)

    return render_template("user_detail.html", user=user)


@app.get('/users/<user_id>/edit')
def edit_user(user_id):
    """display edit page for the given user"""

    user = User.query.get_or_404(user_id)

    return render_template("edit_user_form.html", user=user)


@app.post('/users/<user_id>/edit')
def handle_user_edit(user_id):
    """
    processes the edit form and makes the changes to the given user. redirects
    to user list

    """
    user = User.query.get_or_404(user_id)

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or DEFAULT_IMAGE_URL

    #update database
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect("/users")


@app.post('/users/<user_id>/delete')
def delete_user(user_id):
    """delete the user"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")