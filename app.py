"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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

    return render_template("userlist.html")


@app.get('/users/new')
def display_new_user_form():
    """display new user form"""

    return render_template("newuserform.html")


@app.post('/users/new')
def handle_new_user():
    """creates a new user from the new user form and redirects to the user list"""

    return render_template("userlist.html")


@app.get('/users/<user_id>')
def get_user(user_id):
    """shows information of the given user"""


@app.get('/users/<user_id>/edit')
def edit_user(user_id):
    """display edit page for the given user"""


@app.post('/users/<user_id>/edit')
def handle_user_edit(user_id):
    """processes the edit form and makes the changes to the given user. redirects
    to user list"""


@app.post('/users/<user_id>/delete')
def delete_user(user_id):
    """delete the user"""