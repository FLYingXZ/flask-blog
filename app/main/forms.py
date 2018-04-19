from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired()])
    body=PageDownField("正文",validators=[DataRequired()])
    submit=SubmitField("发布")

class CommentForm(FlaskForm):
    body=PageDownField("评论",validators=[DataRequired()])
    submit=SubmitField("发表")