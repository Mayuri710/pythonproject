from wtforms import StringField, PasswordField, RadioField, SubmitField, DateField, FloatField, DecimalField, IntegerField, FieldList, FormField, HiddenField, SelectMultipleField
from wtforms.widgets import TextArea, CheckboxInput, ListWidget
from wtforms import validators
from wtforms.validators import DataRequired, Optional
from flask_wtf import Form, FlaskForm

class AddBillForm(FlaskForm):
	billDate      = DateField('Bill Date', format='%Y-%m-%d', validators=[DataRequired()])
	dueDate       = DateField('Due Date',  format='%Y-%m-%d', validators=[DataRequired()])
	selectedWings = SelectMultipleField('Wings', choices=[],widget=ListWidget(prefix_label=False),option_widget=CheckboxInput(), validators=[DataRequired()])
	WATER_CHARGES		=DecimalField(label='WATER CHARGES'       ,places=2, validators=[DataRequired()])
	PROPERTY_TAX		=DecimalField(label='PROPERTY TAX'        ,places=2, validators=[DataRequired()])
	ELECTRICITY_CHARGES=DecimalField(label='ELECTRICITY CHARGES',places=2, validators=[DataRequired()])
	SINKING_FUNDS		=DecimalField(label='SINKING FUNDS'       ,places=2, validators=[DataRequired()])
	PARKING_CHARGES		=DecimalField(label='PARKING CHARGES'     ,places=2, validators=[DataRequired()])
	INSURANCE			=DecimalField(label='INSURANCE' ,places=2, validators=[DataRequired()])
	OTHER				=DecimalField(label='OTHER'     ,places=2, validators=[Optional()])
	submitBtn = SubmitField(label='Submit')