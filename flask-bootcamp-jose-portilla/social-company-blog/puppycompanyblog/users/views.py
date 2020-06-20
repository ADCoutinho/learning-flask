# users/views.py

from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from puppycompanyblog import db
from puppycompanyblog.models import User, BlogPost
from puppycompanyblog.users.forms import RegistrationForm, LoginForm
from puppycompanyblog.users.forms import UpdateUserForm
from puppycompanyblog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)


# register
@users.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data, username=form.username.data,
            password=form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Thanks for the registration!")

        return redirect(url_for('users.register'))

    return render_template('register.html', form=form)


# login
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exist
        user = User.query.filter_by(email=form.email.data).first()
        # Check the password with werkzeug and if user exist
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Login Success!")
            # Check if the user request another page that require login
            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html', form=form)


# logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


# account (update UserForm)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("User Account Updated!")

        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for(
        'static', filename='profile_pics/'+current_user.profile_image)
    return render_template(
        'account.html', profile_image=profile_image, form=form)


# user's list of Blog posts
@users.route('/<username>')
def user_posts(username):
    # Using pagination to handle pages inside this route
    page = request.args.get('page', 1, type=int)
    # Querying if user exists and if not 404 to request
    user = User.query.filter_by(username=username).first_or_404()
    # Order query result per date descending and create pagination for results
    blog_posts = BlogPost.query.filter_by(author=user).order_by(
        BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template(
        'user_blogposts.html', blog_posts=blog_posts, user=user)
