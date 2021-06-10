# from flask_login import UserMixin
# from flask import Flask
# from sqlalchemy.orm import relationship
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# db = SQLAlchemy(app)


# class User(UserMixin, db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     name = db.Column(db.String(1000))

#     posts = relationship('BlogPost', back_populates="author")
#     comments = relationship('Comment', back_populates="comment_author")


# class BlogPost(db.Model):
#     __tablename__ = "blog_posts"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     subtitle = db.Column(db.String(250), nullable=False)
#     date = db.Column(db.String(250), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     img_url = db.Column(db.String(250), nullable=False)

#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     author = relationship("User", back_populates="posts")

#     # comment_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     comments = relationship("Comment", back_populates='parent_post')


# class Comment(db.Model):
#     __tablename__ = "comments"
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text, nullable=False)

#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     comment_author = relationship("User", back_populates="comments")

#     post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
#     parent_post = relationship("BlogPost", back_populates="comments")


# # db.create_all()

#---------------------------------------------------------------------------#
# user1 = User(email="mbpod10@gmail.com",
#              name="Brock",
#              password=generate_password_hash(
#                  "123",
#                  method='pbkdf2:sha256',
#                  salt_length=8),
#              )

# db.session.add(user1)

# user2 = User(email="t@gmail.com",
#              name="Tipszy",
#              password=generate_password_hash(
#                  "123",
#                  method='pbkdf2:sha256',
#                  salt_length=8),
#              )

# db.session.add(user2)

# blog1 = BlogPost(
#     title="My First Post",
#     subtitle="I Hate This",
#     date="12/05/2020",
#     body="Blah",
#     img_url="https://victoria.mediaplanet.com/app/uploads/sites/102/2019/07/mainimage-26.jpg",
#     author_id=1
# )
# db.session.add(blog1)

# blog2 = BlogPost(
#     title="Let's Go",
#     subtitle="I Love This",
#     date="12/05/2021",
#     body="The woods, the woods, the bridge of souls to reach!",
#     img_url="https://www.carbonbrief.org/wp-content/uploads/2020/06/yawning-lion-south-africa-1550x804.jpg",
#     author_id=2
# )
# db.session.add(blog2)

# comment1 = Comment(
#     body="I really like this post!",
#     author_id=2,
#     post_id=1
# )
# db.session.add(comment1)

# comment2 = Comment(
#     body="Reallly Good!",
#     author_id=2,
#     post_id=1
# )

# db.session.add(comment2)
# db.session.commit()

#---------------------------------------------------------------------------#
