from housingsociety import db,app
from flask_wtf import Form, FlaskForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Member(db.Model):
    name = db.Column(db.String(80), nullable=False)
    flatno = db.Column(db.Integer, nullable=False ,primary_key=True)
    mobile = db.Column(db.String(80), nullable=False)
    email=db.Column(db.String(80), nullable=False)
    password=db.Column(db.String(80), nullable=False)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'flat_no': self.flatno}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            flat_no = s.loads(token)['flat_no']
        except:
            return None
        return Member.query.get(flat_no)

class Notice(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    subject = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(250), nullable=False) 

class Bill(db.Model):
    bill_num = db.Column(db.Integer,primary_key=True)
    flatno_id = db.Column(db.Integer,db.ForeignKey('member.flatno'),nullable=False)
    bill_date = db.Column(db.DateTime,nullable=False)
    water_charges = db.Column(db.Float,nullable=False)
    property_tax = db.Column(db.Float,nullable=False)
    elec_charges = db.Column(db.Float,nullable=False)
    sinking_fund = db.Column(db.Float,nullable=False)
    parking_charges = db.Column(db.Float,nullable=False)
    other = db.Column(db.Float,nullable=False)
    due_date = db.Column(db.DateTime,nullable=False)

class Paydetails(db.Model):
    pay_id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    flatno_id=db.Column(db.Integer,db.ForeignKey('member.flatno'),nullable=False)
    amount=db.Column(db.Float,nullable=False)
    paydate=db.Column(db.DateTime,nullable=False)
    bill_num_id = db.Column(db.Integer,db.ForeignKey('bill.bill_num'),nullable=False)
    billdate=db.Column(db.DateTime,nullable=False)

class Complaint(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email=db.Column(db.String(50), nullable=False)
    complaintdate=db.Column(db.DateTime,nullable=False)
    flatno_id= db.Column(db.Integer,db.ForeignKey('member.flatno'),nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)

