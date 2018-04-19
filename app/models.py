from . import db, login_manager
from flask_login import UserMixin
# import datetime
from datetime import datetime
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash
import bleach


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    users = db.relationship("User", backref='roles')

    @staticmethod
    def seed():
        db.session.add_all(map(lambda r: Role(name=r), ["Guest", "Administrator"]))
        db.session.commit()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    nickname = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    posts = db.relationship("Post", backref='author')
    commnets = db.relationship("Comment", backref='comment')

    @staticmethod
    def on_created(target, value, oldvalue, initiator):
        target.role = Role.query.filter_by(name="Guest").first()

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.event.listen(User.name, "set", User.on_created)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=True)
    body = db.Column(db.String(5000), nullable=True)
    body_html = db.Column(db.String(5000), nullable=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship("Comment", backref="posts")
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))


db.event.listen(Post.body, "set", Post.on_body_changed)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
