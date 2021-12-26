from flask import render_template,flash,request,redirect,url_for,Blueprint
from user import app
from user import db
from flask_login import login_user, current_user, login_required,logout_user

UserData=Blueprint('UserData',__name__)

@UserData.route('/')
##@login_required
def home():
    return render_template('UserData/base_off.html')

@UserData.route('/aidetect')
def base_on():
    return render_template('UserData/base.html')

@UserData.route('/manual_input')
def base_off():
    return render_template('UserData/base_off.html')

@UserData.route('/register', methods=['GET','POST'])
def register():
    from user.UserData.form import FormRegister
    from user.UserData.model import UserRegister
    form = FormRegister()
    if form.is_submitted():
        user = UserRegister(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return 'Success Thank You'
    print(form.validate_on_submit())
    return render_template('UserData/register.html', form=form)

@UserData.route('/login',methods=['GET', 'POST'])
def login():
    from user.UserData.model import UserRegister
    from user.UserData.form import FormLogin
    form = FormLogin()
    if form.is_submitted():
        #  當使用者按下login之後，先檢核帳號是否存在系統內。
        user = UserRegister.query.filter_by(email=form.email.data).first()
        if user:
            #  當使用者存在資料庫內再核對密碼是否正確。
            if user.check_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(url_for('UserData.home'))
            else:
                #  如果密碼驗證錯誤，就顯示錯誤訊息。
                flash('Wrong Email or Password')
        else:
            #  如果資料庫無此帳號，就顯示錯誤訊息。
            flash('Wrong Email or Password')
    return render_template('UserData/login.html', form=form)


@UserData.route('/logout')
def logout():
    logout_user()
    flash('Log Out See You.')
    return redirect(url_for('UserData.login'))


@UserData.route('/userinfo')
def userinfo():
    return 'Here is UserINFO'

@UserData.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    from user.UserData.form import FormChangePWD
    form = FormChangePWD()
    if form.is_submitted():
        return 'Change'
    return render_template('UserData/changepassword.html', form = form)

@UserData.route('/resetpassword', methods=['GET', 'POST'])
def reset_password():
    from user.UserData.form import FormResetPasswordMail
    from user.UserData.model import UserRegister
    form = FormResetPasswordMail()
    if form.is_submitted():
        if not UserRegister.query.filter_by(email=form.get_email.data).first():
            flash("找不到對應的email")
            return render_template('UserData/resetpasswordemail.html', form=form)
        else:
            user=UserRegister.query.filter_by(email=form.get_email.data).first()
            print("user----------->"+user.username)
            user.password = form.password.data
            db.session.commit()
            return redirect(url_for('UserData.login'))
    return render_template('UserData/resetpasswordemail.html', form=form)


def next_is_valid(url):
    """
    為了避免被重新定向的url攻擊，必需先確認該名使用者是否有相關的權限，
    舉例來說，如果使用者調用了一個刪除所有資料的uri，那就GG了，是吧 。
    :param url: 重新定向的網址
    :return: boolean
    """
    return True
