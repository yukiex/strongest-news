import sys
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

# 準備
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
    'user': 'user',
    'password': 'password',
    'host': 'mysql-db',
    'db_name': 'database'
})
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# モデルとスキーマの定義
# articlesテーブル
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    detail = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'detail', 'type',
                  'img_url', 'created_at', 'updated_at')


articles_schema = ArticleSchema(many=True)
article_schema = ArticleSchema()


# commentsテーブル
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=False)
    article_id = db.Column(db.Integer, primary_key=False)
    detail = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'article_id',
                  'detail', 'created_at', 'updated_at')


comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()


# usersテーブル
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'created_at', 'updated_at')


users_schema = UserSchema(many=True)
user_schema = UserSchema()


# ルーティング設定
@app.route("/")
def hello():
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    message = "Hello World from Flask in a uWSGI Nginx Docker container with Python {} (default)".format(
        version
    )
    return message


@app.route("/comments")
def comment_page():
    comments = Comment.query.all()
    return comments_schema.jsonify(comments)


@app.route("/articles")
def articles_page():
    articles = Article.query.all()
    return articles_schema.jsonify(articles)


@app.route("/users")
def users_page():
    users = User.query.all()
    return users_schema.jsonify(users)


# 起動
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)
