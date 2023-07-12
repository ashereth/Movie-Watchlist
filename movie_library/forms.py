from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired, NumberRange

#create a class form to hold all the movie form data and make all of the fields required
class MovieForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    director = StringField("Director", validators=[InputRequired()])
                                                            
    year = IntegerField("Year", 
                        validators=[
                            InputRequired(), 
                            # create a range of sumbers that this feild must be within
                            NumberRange(min=1878, max=2050, 
                            #create an error message that will be displayed if the form is filled out wrong
                            message="Please enter a valid year in the format YYYY")])


    submit = SubmitField("Add Movie")

