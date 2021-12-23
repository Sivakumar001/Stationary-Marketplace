from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange, ValidationError
from market.sqlmodels import Users

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = Users.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! please try a new username")
    
    def validate_email_address(self, email_id_to_check):
        email = Users.query.filter_by(email_id = email_id_to_check.data).first()
        if email:
            raise ValidationError("Email already exists! please try another email")
        

    username = StringField(label='User Name', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])

    password_1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password_2 = PasswordField(label='Confirm Password', validators=[EqualTo('password_1'), DataRequired()])
    
    budget = IntegerField(label='Budget')
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[Length(min=2,max=30), DataRequired()])
    password_1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label="Login")

class PurchaseItemForm(FlaskForm):
    purchase = SubmitField(label="Purchase")

class SellItemForm(FlaskForm):
    sell = SubmitField(label="Sell")

class ProfileForm(FlaskForm):
    add_budget = IntegerField(label="Add Budget",
    validators=
            [DataRequired(message="Enter integers only"),
             NumberRange(min=500, max=10000, message="enter between 500 to 10,000"),
            ])
    password_1 = PasswordField(label="Verify Password", validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label="submit")