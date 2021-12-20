from flask import render_template,flash,request,redirect,url_for,Blueprint,Response
from flask_login import login_user, current_user, login_required,logout_user
from user.ManualInput.model import ScrewClass,AddScrewTotable,Img
from werkzeug.utils import secure_filename
from user import db

ManualInput=Blueprint('ManualInput',__name__)
@ManualInput.route('/option', methods=['GET', 'POST'])
def Option_select():
    return render_template('ManualInput/ManualInput_choose.html')

@ManualInput.route('/option_uk', methods=['GET', 'POST'])
def DataInput_UK():
    from user.ManualInput.form import FormManualInput_uk
    form=FormManualInput_uk()
    table_list=[]
    items=AddScrewTotable.query.filter_by(user_name=current_user.username).all()

    for item in items:
        table_list.append(item)

    if form.validate_on_submit():
        Body_Length=form.Body_Length.data
        Body_Width=form.Body_Width.data
        Head_Width=form.Head_Width.data
        Head_Legth=form.Head_Legth.data
        Head_Whole_Num=form.Head_Whole_Num.data
        Headtype=form.Headtype.data
        Head_Label=form.Head_Label.data
        Coat=form.Coat.data

        coat_dict={"classA":"白鋅","classB":"黃鋅","classC":"黑鋅"}
        Headwholenum_dict={"zero":"0","one":"1","two":"2","three":"3","four":"4","five":"5"}
        label_dict={"NO":"無","SFS":"SFS","@":"@","SL":"SL","PHI":"PHI","SP":"SP","UK":"UK"}
        Headtype_dict={
            "cross":"十字",
            "square":"方型",
            'six':'六邊型',
            'star':'星型',
            'sp_a':'特殊型A',
        }


        if not ScrewClass.query.filter_by(
            Screw_Head_Type =Headtype_dict[Headtype],
            Screw_Head_wholenum = Headwholenum_dict[Head_Whole_Num],
            Screw_Head_length = Head_Legth,
            Screw_Head_Width = Head_Width,
            Screw_Body_Length=Body_Length,
            Screw_Body_Width=Body_Width,
            Screw_coat=coat_dict[Coat],
            Screw_label=label_dict[Head_Label]
            ).all():
            flash("找不到對應的螺絲")
            flash(Headtype_dict[Headtype])
            flash(Headwholenum_dict[Head_Whole_Num])
            flash( Head_Legth)
            flash(Head_Width)
            flash(Body_Length)
            flash(Body_Width)
            flash(coat_dict[Coat])
            flash(label_dict[Head_Label])
            return redirect(url_for('ManualInput.DataInput_UK'))
        else:
            find_screw=ScrewClass.query.filter_by(
                Screw_Head_Type =Headtype_dict[Headtype],
                Screw_Head_wholenum = Headwholenum_dict[Head_Whole_Num],
                Screw_Head_length = Head_Legth,
                Screw_Head_Width = Head_Width,
                Screw_Body_Length=Body_Length,
                Screw_Body_Width=Body_Width,
                Screw_coat=coat_dict[Coat],
                Screw_label=label_dict[Head_Label]
            ).first()
            add_item=AddScrewTotable(user_name=current_user.username,screw_number=find_screw.number)
            if not AddScrewTotable.query.filter_by(screw_number=find_screw.number).all():
                db.session.add(add_item)
                db.session.commit()
                flash("加入"+str(find_screw.number))
            else:
                flash("以存在"+str(find_screw.number))
            return redirect(url_for('ManualInput.DataInput_UK'))

    return render_template('ManualInput/ManualInput_uk.html',form=form,table_list=table_list)

@ManualInput.route('/option_us', methods=['GET', 'POST'])
def DataInput_US():
    from user.ManualInput.form import FormManualInput_us
    form=FormManualInput_us()
    table_list=[]
    items=AddScrewTotable.query.filter_by(user_name=current_user.username).all()

    for item in items:
        table_list.append(item)

    if form.validate_on_submit():
        Body_Length=form.Body_Length.data
        Body_Width=form.Body_Width_us.data
        Head_Width=form.Head_Width.data
        Head_Legth=form.Head_Legth.data
        Head_Whole_Num=form.Head_Whole_Num.data
        Headtype=form.Headtype.data
        Head_Label=form.Head_Label.data
        Coat=form.Coat.data

        coat_dict={"classA":"白鋅","classB":"黃鋅","classC":"黑鋅"}
        Headwholenum_dict={"zero":"0","one":"1","two":"2","three":"3","four":"4","five":"5"}
        label_dict={"NO":"無","SFS":"SFS","@":"@","SL":"SL","PHI":"PHI","SP":"SP","UK":"UK"}
        BodyWidth_dict={"1":"#1","2":"#2","3":"#3","4":"#4","5":"#5","6":"#6","7":"#7","8":"#8","9":"#9","10":"#10","11":"#11","12":"#12"}
        Headtype_dict={
            "cross":"十字",
            "square":"方型",
            'six':'六邊型',
            'star':'星型',
            'sp_a':'特殊型A',
        }


        if not ScrewClass.query.filter_by(
            Screw_Head_Type =Headtype_dict[Headtype],
            Screw_Head_wholenum = Headwholenum_dict[Head_Whole_Num],
            Screw_Head_length = Head_Legth,
            Screw_Head_Width = Head_Width,
            Screw_Body_Length=Body_Length,
            Screw_Body_Width_us=BodyWidth_dict[Body_Width],
            Screw_coat=coat_dict[Coat],
            Screw_label=label_dict[Head_Label]
            ).all():
            flash(Headtype_dict[Headtype])
            flash(Headwholenum_dict[Head_Whole_Num])
            flash( Head_Legth)
            flash(Head_Width)
            flash(Body_Length)
            flash(Body_Width)
            flash(coat_dict[Coat])
            flash(label_dict[Head_Label])

            return redirect(url_for('ManualInput.DataInput_US'))
        else:
            find_screw=ScrewClass.query.filter_by(
                Screw_Head_Type =Headtype_dict[Headtype],
                Screw_Head_wholenum = Headwholenum_dict[Head_Whole_Num],
                Screw_Head_length = Head_Legth,
                Screw_Head_Width = Head_Width,
                Screw_Body_Length=Body_Length,
                Screw_Body_Width_us=BodyWidth_dict[Body_Width],
                Screw_coat=coat_dict[Coat],
                Screw_label=label_dict[Head_Label]
            ).first()
            add_item=AddScrewTotable(user_name=current_user.username,screw_number=find_screw.number)
            if  not AddScrewTotable.query.filter_by(screw_number=find_screw.number).all():
                db.session.add(add_item)
                db.session.commit()
                flash("加入"+str(find_screw.number))
            else:
                flash("以存在"+str(find_screw.number))
            return redirect(url_for('ManualInput.DataInput_US'))

    return render_template('ManualInput/ManualInput_us.html',form=form,table_list=table_list)

@ManualInput.route('/manual_delete_uk/<number>',methods=['GET', 'POST'])
def Manual_DeleteItem_UK(number):
    DeleteItem=AddScrewTotable.query.filter_by(screw_number=number).first()
    ##db.session.delete(DeleteItem)
    DeleteItem.chose=True
    db.session.commit()
    return redirect(url_for('ManualInput.DataInput_UK'))

@ManualInput.route('/manual_delete_us/<number>',methods=['GET', 'POST'])
def Manual_DeleteItem_US(number):
    DeleteItem=AddScrewTotable.query.filter_by(screw_number=number).first()
    ##db.session.delete(DeleteItem)
    DeleteItem.chose=True
    db.session.commit()
    return redirect(url_for('ManualInput.DataInput_US'))

@ManualInput.route('/upload',methods=['GET', 'POST'])
def UploadImg():
    if request.method =='POST':
        pic = request.files['pic']
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
    return render_template('ManualInput/UploadImg.html')


@ManualInput.route('check/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)

