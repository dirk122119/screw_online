from flask import render_template,flash,request,redirect,url_for,Blueprint,Response
import cv2
import numpy as np
import os
from user.AiDetect import simple_camera
from user.AiDetect import imgwrap
from user.darknet import darknet
from user.ManualInput.model import ScrewClass,AddScrewTotable,Img
from flask_login import login_user, current_user, login_required,logout_user
from user import db


AiDetect=Blueprint('AiDetect',__name__)

@AiDetect.route('/option', methods=['GET', 'POST'])
def Option_select():
    return render_template('AiDetect/AiDetect_choose.html')

@AiDetect.route('/ai_option_uk', methods=['GET', 'POST'])
def AI_DataInput_UK():
    from user.AiDetect.form import Form_AI_uk
    form=Form_AI_uk()
    table_list=[]
    items=AddScrewTotable.query.filter_by(user_name=current_user.username).all()

    for item in items:
        table_list.append(item)

    if form.validate_on_submit():
        Body_Length=form.Body_Length.data
        Body_Width=form.Body_Width.data
        Head_Width=form.Head_Width.data
        Head_Legth=form.Head_Legth.data
        Head_Label=form.Head_Label.data
        Coat=form.Coat.data
        ##========================================================##
        ##=============strings convert from form to view===============##
        ##========================================================##
        coat_dict={"classA":"白鋅","classB":"黃鋅","classC":"黑鋅"}
        label_dict={"NO":"無","SFS":"SFS","@":"@","SL":"SL","PHI":"PHI","SP":"SP","UK":"UK"}
        Headtype_dict={
            "cross":"十字",
            "square":"方型",
            'six':'六邊型',
            'star':'星型',
            'sp_a':'特殊型A',
        }
        ##========================================##
        ##=============Load YOLO cfg===============##
        ##========================================##
        cfg_file = 'user/darknet/cfg/yolov4-obj.cfg'
        data_file = 'user/darknet/cfg/obj.data'
        weight_file = 'user/darknet/yolov4-obj_last.weights'
        thre = 0.25
        show_coordinates = True
        ##=======================================================##
        ##=================get image and YOLO detect===============##
        ##=======================================================##
        img1=simple_camera.show_camera()
        coords="[(353, 28), (953, 28), (353, 628), (953, 628)]"
        pts = np.array(eval(coords), dtype = "float32")

        warped = imgwrap.four_point_transform(img1, pts)
        flash("start")
        network, class_names, class_colors = darknet.load_network(
                cfg_file,
                data_file,
                weight_file,
                batch_size=1
        )

        width = darknet.network_width(network)
        height = darknet.network_height(network)

        
        frame_rgb = cv2.cvtColor( warped, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize( frame_rgb, (width, height))
        darknet_image = darknet.make_image(width, height, 3)
        darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=thre)
        darknet.print_detections(detections, show_coordinates)
        darknet.free_image(darknet_image)
        image = darknet.draw_boxes(detections, frame_resized, class_colors)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.abspath(os.getcwd())+"/images/predict.png", image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        if not ScrewClass.query.filter_by(
            Screw_Head_Type =Headtype_dict[detections[0][0]],
            Screw_Head_length = Head_Legth,
            Screw_Head_Width = Head_Width,
            Screw_Body_Length=Body_Length,
            Screw_Body_Width=Body_Width,
            Screw_coat=coat_dict[Coat],
            Screw_label=label_dict[Head_Label]
            ).all():
            flash("找不到對應的螺絲")
            return redirect(url_for('AiDetect.AI_DataInput_UK'))
        else:
            find_screw=ScrewClass.query.filter_by(
                Screw_Head_Type =Headtype_dict[detections[0][0]],
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
            return redirect(url_for('AiDetect.AI_DataInput_UK'))

    return render_template('AiDetect/OpenCamera_uk.html',form=form,table_list=table_list)

@AiDetect.route('/ai_option_us', methods=['GET', 'POST'])
def AI_DataInput_US():
    from user.AiDetect.form import Form_AI_us
    form=Form_AI_us()
    table_list=[]
    items=AddScrewTotable.query.filter_by(user_name=current_user.username).all()

    for item in items:
        table_list.append(item)

    if form.validate_on_submit():
        Body_Length=form.Body_Length.data
        Body_Width_us=form.Body_Width_us.data
        Head_Width=form.Head_Width.data
        Head_Legth=form.Head_Legth.data
        Head_Label=form.Head_Label.data
        Coat=form.Coat.data
        ##========================================================##
        ##=============strings convert from form to view===============##
        ##========================================================##
        coat_dict={"classA":"白鋅","classB":"黃鋅","classC":"黑鋅"}
        Headwholenum_dict={"zero":"無鑿洞","one":"1個","two":"2個","three":"3個","four":"4個","five":"5個"}
        label_dict={"NO":"無","SFS":"SFS","@":"@","SL":"SL","PHI":"PHI","SP":"SP","UK":"UK"}
        Headtype_dict={
            "cross":"十字",
            "square":"方型",
            'six':'六邊型',
            'star':'星型',
            'sp_a':'特殊型A',
        }
        BodyWidth_dict={"1":"#1","2":"#2","3":"#3","4":"#4","5":"#5","6":"#6","7":"#7","8":"#8","9":"#9","10":"#10","11":"#11","12":"#12"}
        ##========================================##
        ##=============Load YOLO cfg===============##
        ##========================================##
        cfg_file = 'user/darknet/cfg/yolov4-obj.cfg'
        data_file = 'user/darknet/cfg/obj.data'
        weight_file = 'user/darknet/yolov4-obj_last.weights'
        thre = 0.25
        show_coordinates = True
        ##=======================================================##
        ##=================get image and YOLO detect===============##
        ##=======================================================##
        img1=simple_camera.show_camera()
        coords="[(353, 28), (953, 28), (353, 628), (953, 628)]"
        pts = np.array(eval(coords), dtype = "float32")

        warped = imgwrap.four_point_transform(img1, pts)
        flash("start")
        network, class_names, class_colors = darknet.load_network(
                cfg_file,
                data_file,
                weight_file,
                batch_size=1
        )

        width = darknet.network_width(network)
        height = darknet.network_height(network)

        
        frame_rgb = cv2.cvtColor( warped, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize( frame_rgb, (width, height))
        darknet_image = darknet.make_image(width, height, 3)
        darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=thre)
        darknet.print_detections(detections, show_coordinates)
        darknet.free_image(darknet_image)
        image = darknet.draw_boxes(detections, frame_resized, class_colors)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.abspath(os.getcwd())+"/images/predict.png", image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        if not ScrewClass.query.filter_by(
            Screw_Head_Type =Headtype_dict[detections[0][0]],
            Screw_Head_length = Head_Legth,
            Screw_Head_Width = Head_Width,
            Screw_Body_Length=Body_Length,
            Screw_Body_Width_us=BodyWidth_dict[Body_Width_us],
            Screw_coat=coat_dict[Coat],
            Screw_label=label_dict[Head_Label]
            ).all():
            flash("找不到對應的螺絲")
            return redirect(url_for('AiDetect.AI_DataInput_US'))
        else:
            find_screw=ScrewClass.query.filter_by(
                Screw_Head_Type =Headtype_dict[detections[0][0]],
                Screw_Head_length = Head_Legth,
                Screw_Head_Width = Head_Width,
                Screw_Body_Length=Body_Length,
                Screw_Body_Width_us=BodyWidth_dict[Body_Width_us],
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
            return redirect(url_for('AiDetect.AI_DataInput_US'))

    return render_template('AiDetect/OpenCamera_us.html',form=form,table_list=table_list)
@AiDetect.route('/test', methods=['GET', 'POST'])
def OpenCamera():

    cfg_file = 'user/darknet/cfg/yolov4-obj.cfg'
    data_file = 'user/darknet/cfg/obj.data'
    weight_file = 'user/darknet/yolov4-obj_last.weights'
    thre = 0.25
    show_coordinates = True

    img1=simple_camera.show_camera()
    flash("start")
    network, class_names, class_colors = darknet.load_network(
            cfg_file,
            data_file,
            weight_file,
            batch_size=1
    )

    width = darknet.network_width(network)
    height = darknet.network_height(network)

    
    frame_rgb = cv2.cvtColor( img1, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize( frame_rgb, (width, height))
    darknet_image = darknet.make_image(width, height, 3)
    darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thre)
    print("===========================")
    print(detections[0][0])
    print("===========================")
    darknet.print_detections(detections, show_coordinates)
    darknet.free_image(darknet_image)
    image = darknet.draw_boxes(detections, frame_resized, class_colors)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.abspath(os.getcwd())+"/images/predict.png", image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    return render_template('AiDetect/OpenCamera_uk.html',img=image)

@AiDetect.route('/ai_delete_uk/<number>',methods=['GET', 'POST'])
def Ai_DeleteItem_UK(number):
    DeleteItem=AddScrewTotable.query.filter_by(screw_number=number).first()
    ##db.session.delete(DeleteItem)
    DeleteItem.chose=True
    db.session.commit()
    return redirect(url_for('AiDetect.AI_DataInput_UK'))

@AiDetect.route('/ai_delete_us/<number>',methods=['GET', 'POST'])
def Ai_DeleteItem_US(number):
    DeleteItem=AddScrewTotable.query.filter_by(screw_number=number).first()
    ##db.session.delete(DeleteItem)
    DeleteItem.chose=True
    db.session.commit()
    return redirect(url_for('AiDetect.AI_DataInput_US'))