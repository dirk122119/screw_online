from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, validators, PasswordField,ValidationError
from wtforms import BooleanField
from wtforms.fields.html5 import EmailField


from user.UserData.model import UserRegister


class FormRegister(Form):
    """依照Model來建置相對應的Form
    password2: 用來確認兩次的密碼輸入相同
    """
    username = StringField(u'使用者帳號', validators=[
        validators.DataRequired(),
        validators.Length(5, 30)
    ])
    email = EmailField(u'Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    password = PasswordField(u'密碼', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ])
    password2 = PasswordField(u'密碼驗證', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField(u'regist')
    """
    無法驗證
    
    def validate_email(self, field):
        if UserRegister.query.filter_by(email=field.data).first():
            raise ValidationError('Email 已被註冊')

    def validate_username(self, field):
        if UserRegister.query.filter_by(username=field.data).first():
            raise ValidationError('使用者名稱已被註冊')
    """

class FormLogin(Form):
    """
    使用者登入使用
    以email為主要登入帳號，密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """

    email = EmailField(u'Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])

    password = PasswordField(u'PassWord', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField(u'Keep Logged in')

    submit = SubmitField(u'Log in')

class FormChangePWD(Form):
    """
    使用者變更密碼
    舊密碼、新密碼與新密碼確認
    """
    #  舊密碼
    password_old = PasswordField('PassWord_old', validators=[
        validators.DataRequired()
    ])
    #  新密碼
    password_new = PasswordField('PassWord_new', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password_new_confirm', message='PASSWORD NEED MATCH')
    ])
    #  新密碼確認
    password_new_confirm = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Change Password')


class FormResetPassword(Form):
    """使用者申請遺失密碼"""
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password_confirm', message='PASSWORD NEED MATCH')
    ])
    password_confirm = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Reset Password')



class FormResetPasswordMail(Form):
    """應用於密碼遺失申請時輸入郵件使用"""
    get_email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email(),
    ])
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password_confirm', message='PASSWORD NEED MATCH')
    ])
    password_confirm = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Send Confirm')

    def validate_email(self, field):
        """
        驗證是否有相關的EMAIL在資料庫內，若沒有就不寄信
        """
        if not UserRegister.query.filter_by(email=field.data).first():
            raise ValidationError('No Such EMAIL, Please Check!')
