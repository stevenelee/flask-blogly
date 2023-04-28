"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, DEFAULT_IMAGE_URL

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
    posts = user.posts

    return render_template("user_detail.html", user=user, posts=posts)


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


@app.get('/users/<user_id>/posts/new')
def display_post_form(user_id):
    """displays new post form"""

    user = User.query.get_or_404(user_id)

    return render_template("new_post_form.html", user=user)


@app.post('/users/<user_id>/posts/new')
def handle_new_post(user_id):
    """
    takes inputs from post form and adds that information to the database
    redirects to the user detail page

    """

    title = request.form['title']
    content = request.form['content']

    post = Post(
        title = title,
        content = content,
        user_id = user_id
        )

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.get('/posts/<post_id>')
def show_post(post_id):
    """displays a given post"""

    post =  Post.query.get_or_404(post_id)
    user = post.user

    return render_template('post_detail.html', user=user, post=post)


@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
def display_post_editor(post_id):
    """displays the edit post page"""

    post =  Post.query.get_or_404(post_id)

    user_id = post.user_id

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        post.title = title
        post.content = content

        db.session.commit()

        return redirect(f'post_detail.html/{post_id}')

    elif request.method == 'GET':

        return redirect(f'/users/{user_id}')