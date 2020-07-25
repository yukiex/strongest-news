import sys
from flask import Flask, jsonify, make_response, request, Response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy import desc

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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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


@app.route("/comments", methods=["GET"])
def get_all_comments():
    comments = Comment.query.all()
    return comments_schema.jsonify(comments)


@app.route("/comment/<id>", methods=["GET"])
def get_comment(id):
    comment = Comment.query.filter_by(
        article_id=id).order_by(Comment.id).all()
    return comments_schema.jsonify(comment)


@app.route("/comment", methods=["POST"])
def post_comment():
    comment = Comment(
        user_id=int(request.form.get("user_id")),
        article_id=int(request.form.get("article_id")),
        detail=request.form.get("detail"),
    )
    db.session.add(comment)
    db.session.commit()

    response = comment_schema.jsonify(comment)
    response.headers['Location'] = '/comment/%d' % comment.id
    return response, 201


@app.route("/comment/<id>", methods=["PUT"])
def put_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    if not comment:
        # エラーハンドラーに処理を移す場合
        # ステータスコード、dict型にてメッセージ等を設定できる
        abort(404, {'code': 'Not found', 'message': 'comment not found'})

    # 更新
    comment.detail = request.form.get("detail")

    db.session.commit()

    return comment_schema.jsonify(comment)


@app.route("/comment/<id>", methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    if not comment:
        abort(404, {'code': 'Not found', 'message': 'comment not found'})

    # レコードの削除 deleteしてcommit
    db.session.delete(comment)
    db.session.commit()

    return jsonify(None), 204


@app.route("/article/<id>", methods=["GET"])
def get_article(id):
    article = Article.query.get(id)
    return article_schema.jsonify(article)


@app.route("/articles", methods=["GET"])
def get_all_articles():
    articles = Article.query.all()
    return articles_schema.jsonify(articles)


@app.route("/user/<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return users_schema.jsonify(users)


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    response = jsonify({
        "error": {
            "type": error.name,
            "message": error.description
        }
    })
    return response, error.code


# 起動
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)
