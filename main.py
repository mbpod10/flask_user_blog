from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, session
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
import os
# from seed import db, User, BlogPost, Comment

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='x',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# CONFIGURE TABLES


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    posts = relationship('BlogPost', back_populates="author")
    comments = relationship('Comment', back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")

    # comment_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = relationship("Comment", back_populates='parent_post')


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_author = relationship("User", back_populates="comments")

    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")


db.create_all()
############################################################################

user1 = User(email="m@gmail.com",
             name="Brock",
             password=generate_password_hash(
                 "123",
                 method='pbkdf2:sha256',
                 salt_length=8),
             )

db.session.add(user1)

user2 = User(email="t@gmail.com",
             name="Tipszy",
             password=generate_password_hash(
                 "123",
                 method='pbkdf2:sha256',
                 salt_length=8),
             )

db.session.add(user2)

blog1 = BlogPost(
    title="My First Post",
    subtitle="I Hate This",
    date="12/05/2020",
    body="Blah",
    img_url="https://victoria.mediaplanet.com/app/uploads/sites/102/2019/07/mainimage-26.jpg",
    author_id=1
)
db.session.add(blog1)

blog2 = BlogPost(
    title="Let's Go",
    subtitle="I Love This",
    date="12/05/2021",
    body="The woods, the woods, the bridge of souls to reach!",
    img_url="https://www.carbonbrief.org/wp-content/uploads/2020/06/yawning-lion-south-africa-1550x804.jpg",
    author_id=2
)
db.session.add(blog2)

comment1 = Comment(
    body="I really like this post!",
    author_id=2,
    post_id=1
)
db.session.add(comment1)

comment2 = Comment(
    body="Reallly Good!",
    author_id=2,
    post_id=1
)

db.session.add(comment2)
db.session.commit()

##########################################################################
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return function(*args, **kwargs)
    return wrapper


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()

    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("That User Already Exists. Please Log In!")
            return redirect(url_for('login'))
        else:
            new_user = User(
                name=form.name.data,
                email=form.email.data,
                password=generate_password_hash(
                    form.password.data,
                    method='pbkdf2:sha256',
                    salt_length=8),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('get_all_posts'))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(password=form.password.data, pwhash=user.password):
                login_user(user)
                return redirect(url_for('get_all_posts'))
            else:
                flash("Incorrect Password")
        else:
            flash("User Does Not Exists")
    return render_template("login.html", form=form)

# @login_required


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                body=form.body.data,
                author_id=current_user.id,
                post_id=post_id
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("show_post", post_id=post_id))
        else:
            flash("Please Log In To Comment")
            return redirect(url_for("show_post", post_id=post_id))

    return render_template("post.html", post=requested_post, form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=['POST', 'GET'])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            date=date.today().strftime("%B %d, %Y"),
            author_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


# @app.route("/comment/<int:post_id>", methods=['GET', 'POST'])
# def make_comment(post_id):
#     pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
