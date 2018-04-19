from . import auth
from flask import flash, render_template, redirect, url_for
from .form import LoginForm, RegistrationFrom, PasswdChangeFrom
from app.models import User, db
from flask_login import login_user, logout_user, current_user, login_required


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if hasattr(current_user, "id"):
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        # 必须判断用户名和密码
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash(u"用户名或者密码错误！")
        else:
            flash(u"用户名或者密码错误！")
    return render_template("login.html", form=form, title="登录")


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if hasattr(current_user, "id"):
        return redirect(url_for("main.index"))
    form = RegistrationFrom()
    if form.validate_on_submit():
        # 判断用户是否已存在
        if not User.query.filter_by(name=form.username.data).first():
            user = User(email=form.email.data, name=form.username.data, nickname=form.nickname.data,
                        password=form.password.data,
                        role_id=form.authed.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash(u"用户名已存在")
    return render_template('register.html', title=u'注册', form=form)


@auth.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """
    将curren_user查询获取当前登录用户的数据内容并修改
    :return:
    """
    user = User.query.filter_by(name=current_user.name).first()
    form = PasswdChangeFrom()
    # form.old_password.data = user.password

    if form.validate_on_submit():
        if user.check_password(form.password.data):
            flash("新密码不能和老密码相同")
        else:
            user.password = form.password.data
            if form.nickname.data:
                user.nickname = form.nickname.data
            else:
                user.nickname = user.nickname
                # print(user.nickname)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main.index"))
    # 将curren_user的name信息返回到页面的用户信息
    return render_template("change.html", form=form, user=user.name)
