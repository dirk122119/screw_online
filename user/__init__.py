from flask import Flask,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect
from config import Config
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,current_user
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
#  取得啟動文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(user_id):
    from  user.UserData.model import UserRegister
    return UserRegister.query.get(int(user_id))

login.login_view = 'UserData.login'

db = SQLAlchemy(app)
migrate=Migrate(app,db)



#  很重要，一定要放這邊
from user.UserData.view import UserData
from user.ManualInput.view import ManualInput
from user.QuotationSheet.view import QuotationSheet

app.register_blueprint(UserData,url_prefix='/user')
app.register_blueprint(ManualInput,url_prefix='/Manual')
app.register_blueprint(QuotationSheet,url_prefix='/QuotationSheet')

from  user.UserData.model import UserRegister
from user.ManualInput.model import ScrewClass,AddScrewTotable,Img

class MyModeView(ModelView):
    """
    判斷是否為superuser
    """
    def is_accessible(self):
        return current_user.id


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.id

    def inaccessible_callback(self, name, **kwargs):
        flash("沒有權限")
        return redirect(url_for('UserData.login'))

admin=Admin(app,index_view=MyAdminIndexView())
admin.add_view(MyModeView(UserRegister,db.session,category="user_database"))
admin.add_view(MyModeView(ScrewClass,db.session,category="rose_database"))
admin.add_view(MyModeView(AddScrewTotable,db.session,category="table"))
admin.add_view(MyModeView(Img,db.session,category="rose_database"))
if __name__ == '__main__':
    print(pjdir)