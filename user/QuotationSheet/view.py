from flask import render_template,flash,request,redirect,url_for,Blueprint,Response
from user.ManualInput.model import ScrewClass,AddScrewTotable,Img

QuotationSheet=Blueprint('QuotationSheet',__name__)

@QuotationSheet.route('/get_sheet', methods=['GET', 'POST'])
def get_sheet():
    table_list=[]
    total_price=0
    items=AddScrewTotable.query.all()
    for item in items:
        total_price=total_price+item.screwclass.ScrewPrice
        table_list.append(item)
        print(item)
    return render_template('QuotationSheet/QuotationSheet.html',table_list=table_list,total_price=total_price)