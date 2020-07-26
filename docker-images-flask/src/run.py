import sys
from flask import Flask, jsonify, make_response, request, Response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy import desc
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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

# sessionを使う際にSECRET_KEYを設定
app.config['SECRET_KEY'] = 'secret_key'

# ログインモジュール
login_manager = LoginManager()
login_manager.init_app(app)


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


class ArticleTitleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'img_url', 'created_at')


articles_schema = ArticleSchema(many=True)
article_schema = ArticleSchema()
article_titles_schema = ArticleTitleSchema(many=True)


# commentsテーブル
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, primary_key=False)
    article_id = db.Column(db.Integer, primary_key=False)
    detail = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'article_id',
                  'detail', 'created_at', 'updated_at')


comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()


# userテーブル
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    e_mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'e_mail', 'password', 'created_at', 'updated_at')


users_schema = UserSchema(many=True)
user_schema = UserSchema()


# ログイン周辺
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=["POST"])
def login():
    user = User.query.filter_by(e_mail=request.form.get("e_mail")).filter_by(
        password=request.form.get("password")).first()
    if user is not None:
        login_user(user)
        return 'Login Successfully'
    else:
        return 'Login Failed', 401


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logout Successfully'


@app.route("/login/check", methods=["GET"])
@login_required
def check_login():
    user = User.query.get(current_user.id)
    return user_schema.jsonify(user)


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
        name=request.form.get("name"),
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


@app.route("/articles/latest", methods=["GET"])
def get_latest_articles():
    articles = Article.query.order_by(desc(Article.created_at)).limit(9)
    return article_titles_schema.jsonify(articles)


@app.route("/articles/title", methods=["GET"])
def get_all_article_titles():
    articles = Article.query.all()
    return article_titles_schema.jsonify(articles)


@app.route("/articles/title/<page>", methods=["GET"])
def get_article_titles(page):
    articles = Article.query.order_by(
        Article.id).limit(9).offset(9 * (int(page)-1))
    return article_titles_schema.jsonify(articles)


@app.route("/user/profile", methods=["GET"])
@login_required
def get_user(id):
    user = User.query.get(current_user.id)
    return user_schema.jsonify(user)


# @app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return users_schema.jsonify(users)

# Usage: /search?keyword=example
@app.route("/search", methods=["GET"])
def get_search_article():
    keyword = request.args.get('keyword', '')
    articles = Article.query.filter(Article.title.like('%{}%'.format(keyword)))
    return article_titles_schema.jsonify(articles)

# Usage: /category?type=エンタがビタミン
@app.route("/category", methods=["GET"])
def get_category_article():
    _type = request.args.get('type', '')
    articles = Article.query.filter(Article.type.like('%{}%'.format(_type)))
    return article_titles_schema.jsonify(articles)


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
