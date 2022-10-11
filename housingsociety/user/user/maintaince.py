from flask import Blueprint
from housingsociety.models import Member
from flask import Flask,render_template,request,url_for,redirect, session,flash,make_response,Response
from housingsociety import db
from datetime import datetime
from housingsociety.user import views
from housingsociety.models import Notice,Bill,Paydetails
from sqlalchemy import __ge__
import io
import xlwt
from sqlalchemy import extract  
import pdfkit,smtplib

maintaince_blueprint = Blueprint('maintaince',__name__)
@maintaince_blueprint.route('/MainBill', methods=['GET', 'POST'])
def userbill():
    if request.method == 'GET':
        flatno = session.get('flat_num')
        todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        details = Bill.query.filter_by(flatno_id=flatno).filter(Bill.due_date >= todays_datetime).all()
        totalsum = 0
        for row in details:
            totalsum += row.water_charges+row.property_tax+row.elec_charges+row.sinking_fund+row.parking_charges+row.other
            session['total'] = totalsum
       
    return render_template('user/maintaince.html',details=details,totalsum=totalsum)
    

@maintaince_blueprint.route('/Payment', methods=['GET', 'POST'])
def paybill():
    msg = None
    if request.method == 'POST':
        flatno = session.get('flat_num')
        amount = session.get('total')
        user_name = session.get('user_name')
        email = session.get('email')
        name='test'
        cardno = '4555 4585 5258 2368'
        cvv = '526'
        billdetails = Bill.query.filter_by(flatno_id=flatno).first()
        if billdetails:
            date_of_bill = billdetails.bill_date
            bill_id = billdetails.bill_num
            paydate=datetime.now()
            
            if request.form.get('name')==name and request.form.get('cardno')==cardno and request.form.get('ccv')==cvv:
                entry = Paydetails(name=user_name, flatno_id=flatno, amount=amount, paydate=paydate, bill_num_id=bill_id, billdate = date_of_bill)
                db.session.add(entry)
                db.session.commit()
                message = f'Payment done successul with amount of {amount}'
                server = smtplib.SMTP("smtp.gmail.com",587)
                server.starttls()
                server.login("djangopro3031@gmail.com","django@3031")
                server.sendmail("djangopro3031@gmail.com", email, message)
                return render_template('user/ahome.html')
            else:
                msg = 'Invalid User'
                return render_template('user/payment.html',msg=msg)
    return render_template('user/payment.html')


@maintaince_blueprint.route('/uhistory', methods=['GET', 'POST'])
def history():
    if request.method == "GET":
        flatno = session.get('flat_num')
        if flatno is not None:
            st=Paydetails.query.filter_by(flatno_id= flatno)
            return render_template('user/paymenthistory.html',st=st)
    return render_template('user/payinvoice.html')

@maintaince_blueprint.route('/downloadinvoice/<id>',methods = ['GET', 'POST'])
def receipt(id):
    invoice = Paydetails.query.get(id)
    flatno = session.get('flat_num')
    billdetails = Bill.query.filter_by(flatno_id=flatno).first()
    html = render_template("user/payinvoice.html",invoice=invoice,billdetails=billdetails)
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False,configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=invoice.pdf"
    return response