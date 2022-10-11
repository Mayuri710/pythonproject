from flask import Blueprint
from housingsociety.models import Complaint, Member
from flask import Flask,render_template,request,url_for,redirect, session,flash,Response,jsonify
import random
from datetime import  datetime
import smtplib
from housingsociety.models import Notice,Bill,Paydetails,Complaint
from housingsociety.admin.form import AddNotice
from housingsociety.admin.form import AddBillForm
import re,string
import xlwt
import io
from flask_mail import Message
from housingsociety import db, mail


register_blueprint = Blueprint('register',__name__)

@register_blueprint.route('/adminhome',methods = ['GET', 'POST'])
def admin_home():
    return render_template('admin/ahome.html')

@register_blueprint.route('/adminlogin',methods = ['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username= request.form.get('username')
        password= request.form.get('password')
        if username!= 'admin' or password != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = username
            return render_template('admin/ahome.html')
    return render_template('admin/alogin.html', error=error)

@register_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('user/ahome.html')

@register_blueprint.route('/member',methods = ['GET', 'POST'])
def addmember():
    msg = ''
    if(request.method=='POST'):
        name = request.form.get('name')
        flatno = request.form.get('flat_no')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        password=''.join(random.sample(string.ascii_lowercase, 8))
        if not name or not flatno or not mobile or not email:
            msg = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'^(\+\d{1,3}[- ]?)?\d{10}$', mobile):
            msg = 'Invalid Mobile Number !'
        elif not re.match(r'^[a-zA-Z][a-zA-Z ]+[a-zA-Z]$', name):
            msg = 'Alphabet Only'
        else:
            entry = Member(name=name,flatno=flatno,mobile=mobile,email=email,password=password)
            db.session.add(entry)
            db.session.commit()
            message = "your registration done successfully your password is " + password
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login("djangopro3031@gmail.com","django@3031")
            server.sendmail("djangopro3031@gmail.com", email, message)
    return render_template('admin/member/addmember.html',msg = msg)

@register_blueprint.route('/view')
def View():
    all_data = Member.query.all()
    return render_template('admin/member/membertable.html', member = all_data)

@register_blueprint.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Member.query.get(request.form.get('id'))
 
        my_data.name = request.form['name']
        my_data.email = request.form['email']
 
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('register.View'))

#This route is for deleting our employee
@register_blueprint.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Member.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('register.View'))

@register_blueprint.route('/Notice', methods=['GET', 'POST'])
def addNotice():
    msg=''
    noticeForm = AddNotice(request.form)
    if  not noticeForm.validate_on_submit():
        for error in noticeForm.errors.values():
            flash(str(error[0]))
    else:
        addnotices = Notice(subject=noticeForm.subject.data,date=noticeForm.date.data,description=noticeForm.body.data)
        db.session.add(addnotices)
        db.session.commit()
        msg="Notice added"
        noticeForm = AddNotice(formdata=None)
    return render_template('admin/notice/addnotice.html', noticeForm=noticeForm,msg=msg)
def mailmsg(email):
    msg = Message('Maintenaince Bill',
                  sender='noreply@demo.com',
                  recipients=[email])
    msg.body = f'''Your MaintanceBill for this month is added.Please fill before duedate'''
    mail.send(msg)
@register_blueprint.route('/Bill', methods=['GET', 'POST'])
def addBill():
    msg=''
    billForm = AddBillForm(request.form)
    if True or billForm.validate_on_submit():
        billForm.selectedWings.choices =[(flat.flatno)for flat in Member.query.all()]
        if(request.method=='POST'):
            flat_no = Member.query.filter_by(flatno=billForm.selectedWings.data).first()
            email = flat_no.email
            addbill = Bill(flatno_id=billForm.selectedWings.data,bill_date=billForm.billDate.data, 
                            water_charges =billForm.WATER_CHARGES.data,property_tax = billForm.PROPERTY_TAX.data, 
                            elec_charges = billForm.ELECTRICITY_CHARGES.data,sinking_fund = billForm.SINKING_FUNDS.data,
                            parking_charges = billForm.PARKING_CHARGES.data, other = billForm.OTHER.data, due_date=billForm.duedate.data)
            db.session.add(addbill)
            db.session.commit()
            mailmsg(email)
            billForm = AddBillForm(formdata=None)
            msg="Bill added"
    return render_template('admin/bill/addbill.html', billForm=billForm,msg=msg)

@register_blueprint.route('/download/report', methods=['GET', 'POST'])
def download_report():
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    billpayed = Paydetails.query.filter(Paydetails.paydate <= todays_datetime)
    #output in bytes
    output = io.BytesIO()
  #create WorkBook object
    workbook = xlwt.Workbook('datetimes.xlsx', {'default_date_format':
                                                  'dd/mm/yy'})
  #add a sheet
    
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'
    sh = workbook.add_sheet('Employee Report')
    #add headers
    sh.write(0, 0, 'Name')
    sh.write(0, 1, 'Amount')
    sh.write(0, 2, 'Payment date')
    
    idx = 0
    for row in billpayed:
        sh.write(idx+1, 0, row.name)
        sh.write(idx+1, 1, row.amount)
        sh.write(idx+1, 2,row.paydate,date_format)
        idx += 1
    workbook.save(output)
    output.seek(0)
    
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=billreport.xls"})

@register_blueprint.route('/download', methods=['GET', 'POST'])
def index():
    all_data = Paydetails.query.all()
    return render_template('downloadexcel.html', member = all_data)

@register_blueprint.route('/range', methods=['GET', 'POST'])
def range():
    if(request.method=='POST'):
        From = request.form.get('From')
        to = request.form.get('to')
        query =  Paydetails.query.filter(Paydetails.paydate.between(From,to)).all()
        return jsonify({'htmlresponse': render_template('response.html', query=query)})
    return render_template('response.html')


@register_blueprint.route('/viewcomplaint')
def ComplaintView():
    all_data = Complaint.query.all()
    return render_template('admin/viewcomplaint.html', row = all_data)

@register_blueprint.route('/complaint/<id>/')
def replycomplaint(id):
    row = Complaint.query.get(id)
    return render_template('admin/viewcomplaint.html',row=row)

@register_blueprint.route('/sendreply', methods = ['GET', 'POST'])
def sendreply():
    if request.method == 'POST':
        my_data = Complaint.query.get(request.form.get('id'))
        subject = my_data.subject
        email = my_data.email
        msg = Message(subject,
                    sender='noreply@demo.com',
                    recipients=[email])
        msg.body = request.form.get('reply')
        mail.send(msg)
        return redirect(url_for('register.ComplaintView'))

 

