from flask import render_template, request, redirect, flash, url_for, current_app, abort
from os import path
from werkzeug.utils import secure_filename
from . import main
from app import db
from app.models import Post, Comment
from .forms import CommentForm, PostForm
from flask_login import current_user, login_required


# 模板静态路由
@main.route('/')
@main.route('/index')
def index():
    posts = Post.query.all()
    return render_template("index.html", title="欢迎来到Alan博客", posts=posts)


@main.route("/services")
def services():
    return render_template("service.html", title=u'服务')


# 规则匹配路由
@main.route("/user/<username>")
def user(username):
    return "User:{0}".format(username)


# 定义复杂匹配路由
@main.route("/users/<regex('[a-z]{3}'):user_id>")
def users(user_id):
    return "User:{0}".format(user_id)


# Upload
@main.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        f = request.files["file"]
        from app import basedir
        upload_path = path.join(basedir, 'static', 'uploads', secure_filename(f.filename))
        f.save(upload_path)
        return redirect(url_for(".upload"))
    return render_template("upload.html", method=request.method)


# 错误页面
@main.errorhandler(404)
# @app.route("/error")
def page_not_find(e):
    return render_template("404.html"), 404


@main.route('/posts/<int:id>', methods=["GET", "POST"])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    # user=User.query.filter(name=current_user.name).first()
    # user=current_user

    if form.validate_on_submit():
        if not hasattr(current_user, "id"):
            flash("评论功能仅供注册用户使用！")
            form.body.data = ""
        else:
            comment = Comment(body=form.body.data, post_id=post.id, author_id=post.author_id)
            db.session.add(comment)
            db.session.commit()
            # 手动清空form组件
            form.body.data = ""

    return render_template("posts/detail.html",
                           title=post.title,
                           form=form,
                           post=post,
                           comments=post.comments)


@main.route("/edit", methods=["GET", "POST"])
@main.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id=0):
    form = PostForm()

    if id == 0:
        post = Post(author_id=current_user.id)
        if post.title is None:
            post.title = ""
    else:
        post = Post.query.get_or_404(id)
        if request.method=="GET":
            form.title.data = post.title
            form.body.data = post.body

    if form.validate_on_submit():

        post.body = form.body.data
        post.title = form.title.data
        db.session.add(post)
        db.session.commit()
        # print(form.body)
        return redirect(url_for("main.post", id=post.id))
    mode = "添加新文章"
    if id > 0:
        mode = "编辑"
    # print(post.body)
    return render_template("posts/edit.html",
                           title="{0}{1}".format(mode, post.title),
                           post=post,
                           form=form)


@main.route("/shutdown")
def shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get("werkzeug.server.shutdown")

    if not shutdown:
        abort(500)
    shutdown()
    return "server is shutdown..."


@main.route("/about")
def about():
    return render_template("service.html", title="about me")
