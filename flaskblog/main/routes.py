from flask import render_template, request, Blueprint
from flaskblog.models import Post
import socket

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home_page():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    # posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("home.html", posts=posts)


@main.route("/about")
def about_page():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return render_template("about.html", title="About", hostname=hostname, ip=ip)
