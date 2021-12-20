from flask_wtf import FlaskForm as Form
from wtforms import StringField,FloatField,SubmitField, validators,ValidationError
from wtforms import BooleanField
from flask import flash
from wtforms.fields.core import SelectField



class Form_AI_uk(Form):
    '''
    手動輸入要找的螺絲資料
    '''

    Body_Length=FloatField(u'身長(mm)', validators=[
        validators.DataRequired()
    ])

    Body_Width=FloatField(u'身直徑(mm)', validators=[
        validators.DataRequired()
    ])

    Head_Width=FloatField(u'頭寬(mm)', validators=[
        validators.DataRequired()
    ])

    Head_Legth=FloatField(u'頭長(mm)', validators=[
        validators.DataRequired()
    ])

    Head_Label=SelectField('標籤',choices=
    [
        ('NO','無標籤'),
        ('SFS','SFS'),
        ('@','@'),
        ('SL','SL'),
        ('PHI','PHI'),
        ('SP','SP'),
        ('UK','UK'),
    ])

    Coat=SelectField('鍍膜種類',choices=[('classA','白鋅'),('classB','黃鋅'),('classC','黑鋅')])


    submit = SubmitField(u'查詢')

    def validate_Head_Width(self,field):
        if field.data>200:
            raise ValidationError('超過200mm')
        if field.data<1:
            raise ValidationError('小於1mm')
    def validate_Head_Legth(self,field):
        if field.data>200:
            raise ValidationError('超過200mm')
        if field.data<1:
            raise ValidationError('小於1mm')
    def validate_Body_Length(self,field):
        if field.data>200:
            raise ValidationError('超過200mm')
        if field.data<1:
            raise ValidationError('小於1mm')
    def validate_Body_Width(self,field):
        if field.data>200:
            raise ValidationError('超過200mm')
        if field.data<1:
            raise ValidationError('小於1mm')


class Form_AI_us(Form):
    '''
    手動輸入要找的螺絲資料
    '''

    Body_Length=FloatField(u'身長(mm)', validators=[
        validators.DataRequired()
    ])

    Body_Width_us=SelectField('身直徑(番數)',choices=
    [
        ('1','#1'),('2','#2'),('3','#3'),('4','#4'),('5','#5'),('6','#6'),('7','#7'),('8','#8'),('9','#9'),('10','#10'),('11','#11'),('12','#12')
    ])

    Head_Width=FloatField(u'頭寬(mm)', validators=[
        validators.DataRequired()
    ])

    Head_Legth=FloatField(u'頭長(mm)', validators=[
        validators.DataRequired()
    ])

    Head_Label=SelectField('標籤',choices=
    [
        ('NO','無標籤'),
        ('SFS','SFS'),
        ('@','@'),
        ('SL','SL'),
        ('PHI','PHI'),
        ('SP','SP'),
        ('UK','UK'),
    ])

    Coat=SelectField('鍍膜種類',choices=[('classA','白鋅'),('classB','黃鋅'),('classC','黑鋅')])


    submit = SubmitField(u'查詢')

    def validate_Head_Width(self,field):
        if field.data>200:
            raise ValidationError('超過200mm')
        if field.data<1:
            raise ValidationError('小於1mm')
    def validate_Head_Legth(self,field):
        if field.data>200:
            raise ValidationError('超過200mm')
        if field.data<1:
            raise ValidationError('小於1mm')
    def validate_Body_Length(self,field):
        if field.data>200:
            raise ValidationError('超過200mm')
        if field.data<1:
            raise ValidationError('小於1mm')
    