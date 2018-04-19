# _*_ coding:utf-8 _*_
from flask import Flask
from werkzeug.routing import BaseConverter
from flask_pagedown import PageDown
from functools import reduce
from flask_bootstrap import Bootstrap
from flask_gravatar import Gravatar
# from flask_nav.elements import *
from flask_login import LoginManager
import pymysql
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_wtf.csrf import CSRFProtect
from config import config

basedir = path.abspath(path.dirname(__file__))


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# app.secret_key = 12345
bootstrap = Bootstrap()
csrf = CSRFProtect()
pagedown = PageDown()
db = SQLAlchemy()
# manager=Manager()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'
login_manager.login_message='请先登录再进行操作'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    pagedown.init_app(app)
    Gravatar(app, size=64)
    login_manager.init_app(app)
    app.url_map.converters['regex'] = RegexConverter
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(main_blueprint, static_folder="static")

    # 自定义函数,仅仅支持GBK
    def read_md(filename):
        with open(filename) as md_file:
            content = reduce(lambda x, y: x + y, md_file.readlines())
        return content

    # 将函数传递到jinja模板
    @app.context_processor
    def inject_methods():
        return dict(read_md=read_md)

    def jinja2_encode(txt):
        return txt.encode()

    @app.context_processor
    def encode_methods():
        return dict(jinja2_encode=jinja2_encode)

    # 将上下文处理器传递到jinja模板
    @app.template_test("current_link")
    def is_current_link(link):
        from flask import request
        return link == request.path

    # jinja 模板过滤器注册
    @app.template_filter("md")
    def markdown_to_html(html):
        from markdown import markdown
        return markdown(html)

    return app
