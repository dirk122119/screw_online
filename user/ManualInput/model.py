from user import db

class ScrewClass(db.Model):
    """
    
    """
    __tablename__ = u'ScrewClass'
    id = db.Column(db.Integer,primary_key=True)
    number = db.Column(db.String(80))
    ##=====Head=====##
    Screw_Head_Type = db.Column(db.String(80))
    Screw_Head_wholenum = db.Column(db.String(80))
    Screw_Head_length = db.Column(db.Float(10))
    Screw_Head_Width = db.Column(db.Float(10))
    ##=====Body=====##
    Screw_Body_Length = db.Column(db.Float(10))
    Screw_Body_Width = db.Column(db.Float(10))
    Screw_Body_Width_us=db.Column(db.String(80))
    ##=====price=====##
    ScrewPrice = db.Column(db.Integer)

    ##=====coat=====##
    Screw_coat = db.Column(db.String(80))
    ##=====coat=====##
    Screw_label = db.Column(db.String(80))

    db_ScrewClass_AddScrewTotable = db.relationship(u'AddScrewTotable', backref=u'screwclass',lazy=True, primaryjoin="ScrewClass.number==AddScrewTotable.screw_number")
    db_ScrewClass_Img=db.relationship(u'Img',backref=u'screwclass',lazy=True, primaryjoin="ScrewClass.number==Img.Img_number")

    def __repr__(self):
        return '編號:%s' % (self.number)
    def __init__(self) -> None:
        super().__init__()

class AddScrewTotable(db.Model):
    """
    建立螺絲種類與估價使用者
    """
    __tablename__ = u'AddScrewTotable'
    id = db.Column(db.Integer, primary_key=True)
    screw_number = db.Column(db.String(80), db.ForeignKey(u'ScrewClass.number'), nullable=False)
    user_name = db.Column(db.String(80), db.ForeignKey(u'UserRegister.username'), nullable=False)
    chose=db.Column(db.Boolean,default=False,nullable=False)
    def __init__(self,user_name,screw_number):
        self.user_name=user_name
        self.screw_number=screw_number

class Img(db.Model):
    __tablename__ = u'Img'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    Img_number=db.Column(db.String(80), db.ForeignKey(u'ScrewClass.number'), nullable=False)

