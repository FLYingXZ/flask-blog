from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, Length
from app.models import Role



class LoginForm(Form):
    username = StringField(validators=[DataRequired()], label="用户名")
    password = PasswordField(validators=[DataRequired()], label="密 码")
    submit = SubmitField(label="提交")


class RegistrationFrom(Form):
    email = StringField(u"邮箱地址", validators=[DataRequired(), Length(1, 64), Email()])
    nickname = StringField("昵称", validators=[DataRequired()])
    username = StringField(u"用户名", validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                     u"用户名必须由字母开头，字母、数字、下划线或 . 组成")])
    password = PasswordField(u"密码", validators=[DataRequired(), EqualTo('password2', message=u'两次密码不一致')])
    password2 = PasswordField(u"确认密码", validators=[DataRequired()])
    authed = SelectField(u'权限', coerce=int)
    submit = SubmitField(u"立即注册")

    # SelectFrom Data 数据需要注意,多个列表直接在init里面添加
    def __init__(self, *args, **kwargs):
        super(RegistrationFrom, self).__init__(*args, **kwargs)
        self.authed.choices = [(role.id, role.name) for role in Role.query.order_by(Role.id).all()]


class PasswdChangeFrom(Form):
    user = StringField(u"用户名", validators=None)
    nickname = StringField("昵称")
    # old_password = HiddenField(validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[DataRequired(), Length(6, 16, message="密码长度不合适，请输入6-16位密码"),
                                                 EqualTo("password2", message=u"两次密码不一致")])
    password2 = PasswordField(u"重复密码", validators=[DataRequired()])
    submit = SubmitField(u"提交")
    # def __init__(self,*args,**kwargs):
    #     super(PasswdChangeFrom,self).__init__(*args,**kwargs)
    #     self.old_password=[user.password for user in User.query.filter_by(name=current_user.name).first()]
