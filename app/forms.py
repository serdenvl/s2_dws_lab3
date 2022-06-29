from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, FileField, SelectField, FloatField
from wtforms.validators import NumberRange, NoneOf, InputRequired

from app.task1 import Task1Function, Task1Orientation


class UploadForm(FlaskForm):
    upload = FileField(
        label='Load image',
        validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Upload')


class RetouchForm(FlaskForm):
    class Meta:
        csrf = False

    function = SelectField(
        label='Select function: ',
        choices=[f.name for f in Task1Function],
        default=Task1Function.cos.name
    )

    orientation = SelectField(
        label='Select argument: ',
        choices=[o.name for o in Task1Orientation],
        default=Task1Orientation.vertical.name
    )

    period = FloatField(
        label='Select period: ',
        default=100,
        validators=[
            InputRequired(),
            NumberRange(min=0, message='period must be a number greater than zero'),
            NoneOf(values=[0], message='period must be a number greater than zero')])

    period_type = SelectField(
        choices=['px', '%'],
        default='%'
    )

    submit = SubmitField(label='Retouch')
