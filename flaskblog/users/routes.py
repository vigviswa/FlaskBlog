from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, brcypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.users.utils import save_picture

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("main.home_page"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = brcypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(
            "Your Account has been Created! You can now Login!".format(
                {form.username.data}
            ),
            "success",
        )
        return redirect(url_for("users.login_page"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.home_page"))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and brcypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")

            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("main.home_page"))
            )
        else:
            flash("Login Unsuccessful. Please check the Email and Password", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout_page():
    logout_user()
    return redirect((url_for("main.home_page")))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account_page():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been updated", "success")
        return redirect(url_for("users.account_page"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=3)
    )
    return render_template("user_posts.html", posts=posts, user=user)
