from flask import Blueprint
from housingsociety.models import Member
from flask import Flask,render_template,request,url_for,redirect, session,flash,make_response
import random
import re
import smtplib
from housingsociety import db, mail
from housingsociety.models import Notice,Paydetails,Complaint
import pdfkit
from datetime import date
from flask_mail import Message
from flask_mail import Mail

userlogin_blueprint = Blueprint('userlogin',__name__)
@userlogin_blueprint.route('/',methods = ['GET', 'POST'])
def home():
    return render_template('user/ahome.html')

@userlogin_blueprint.route('/loginuser',methods = ['GET', 'POST'])
def user_login():
    msg= None
    if request.method == 'POST': 
        email = request.form["email"]
        password = request.form["password"]
        login = Member.query.filter_by(email=email,password=password).first()
        if login:
            session['flat_num'] = login.flatno
            session['user_name'] = login.name
            session['email'] = login.email

            return redirect(url_for("userlogin.home"))
        else:
             msg = 'Invalid User'
    return render_template('user/login.html',msg = msg)

@userlogin_blueprint.route('/logoutuser')
def logout():
    session.pop('flat_num', None)
    return render_template('user/ahome.html')


@userlogin_blueprint.route('/noticeview')
def getnotice():
    unote = Notice.query.all()
    return render_template('user/viewnotice.html',unote=unote)

@userlogin_blueprint.route('/viewdetail/<id>/')
def viewnotice(id):
    unote = Notice.query.get(id)
    return render_template('user/viewnotice.html',unote=unote)
   
@userlogin_blueprint.route('/downloadpdf',methods = ['GET', 'POST'])
def noticepdf():
    notepdf = Notice.query.get(request.form.get('id'))
    html = render_template("user/notice_details_pdf.html",notepdf=notepdf)
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False,configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=notice.pdf"
    return response

@userlogin_blueprint.route('/complaint',methods = ['GET', 'POST'])
def complaint():
    msg = ''
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        flatno_id =  session.get('flat_num')
        complaintdate = date.today()
        if not name  or not subject or not message or not email:
            msg = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        else:
            if flatno_id:
                entry = Complaint(name=name,email=email,complaintdate=complaintdate,flatno_id=flatno_id,subject=subject,message=message)
                db.session.add(entry)
                db.session.commit()
                message1 = "Received your complaint. We will soon take soon action. Thank you."
                server = smtplib.SMTP("smtp.gmail.com",587)
                server.starttls()
                server.login("djangopro3031@gmail.com","django@3031")
                server.sendmail("djangopro3031@gmail.com", email, message1)
    return render_template('user/complaint.html',msg = msg)

@userlogin_blueprint.route('/changepassword',methods = ['GET', 'POST'])
def changepassword():
    msg= None
    smsg= None
    if request.method == 'POST': 
        flatno =  session.get('flat_num')
        my_data = Member.query.filter_by(flatno = flatno).first()
        if flatno :
            newpassword = request.form['rpass']
            compassword = request.form['crpass']
            if newpassword != compassword:
                msg='password doesnt match'
            else:
                my_data.password = newpassword
                db.session.commit()
                smsg = 'password change'
    return render_template('user/resetpass.html',msg=msg,smsg=smsg)
   
def sendmail(flatno):
    token = flatno.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[flatno.email])
    msg.body = f'''To reset your password, visit the following link:
                {url_for('userlogin.reset_token', token=token, _external=True)}
                        If you did not make this request then simply ignore this email and no changes will be made.
                        '''
    mail.send(msg)

@userlogin_blueprint.route('/reset',methods = ['GET', 'POST'])
def resetpassword():
    msg= None
    if request.method == 'POST': 
        email = request.form["email"]
        flatno  = Member.query.filter_by(email=email).first()
        if flatno :
            sendmail( flatno )
            msg = 'Please Check Your Email To reset Your Paasword'
    return render_template('user/reset_password.html',msg=msg)

@userlogin_blueprint.route('/reset/<token>',methods = ['GET', 'POST'])
def reset_token(token):
    flatno = Member.verify_reset_token(token)
    if flatno is None:
        flash('that is invaild token')
        return redirect(url_for('userlogin.resetpassword'))
    if request.method == 'POST': 
        flatno.password = request.form['password']
        db.session.commit()
        return redirect(url_for('userlogin.user_login'))
    return render_template('user/changepassword.html')
