from wtforms import StringField, PasswordField, RadioField, SubmitField, DateField, FloatField, DecimalField, IntegerField, FieldList, FormField, HiddenField, SelectField
from wtforms.widgets import TextArea, CheckboxInput, ListWidget
from wtforms import validators
from wtforms.validators import DataRequired, Optional
from flask_wtf import Form, FlaskForm


class AddNotice(FlaskForm):
    subject  = StringField('Subject', validators=[validators.Length(min=3, max=63, message='Invalid header')])
    date    = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    body    = StringField('Descripion', widget=TextArea(), validators=[DataRequired()])
    submitBtn = SubmitField(label='Submit')


class AddBillForm(FlaskForm):
	billDate      = DateField('Bill Date', format='%Y-%m-%d', validators=[DataRequired()])
	duedate      = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
	selectedWings = SelectField('Wings', choices=[], validators=[DataRequired()])
	WATER_CHARGES	=FloatField(label='WATER CHARGES', validators=[DataRequired()])
	PROPERTY_TAX	=FloatField(label='PROPERTY TAX', validators=[DataRequired()])
	ELECTRICITY_CHARGES=FloatField(label='ELECTRICITY CHARGES', validators=[DataRequired()])
	SINKING_FUNDS =FloatField(label='SINKING FUNDS', validators=[DataRequired()])
	PARKING_CHARGES	=FloatField(label='PARKING CHARGES', validators=[DataRequired()])
	OTHER	=FloatField(label='OTHER' , validators=[Optional()])
	submitBtn = SubmitField(label='Submit')

