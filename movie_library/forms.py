from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField, URLField
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
                            message="Please enter a valid year in the format YYYY")
                        ]
                    )


    submit = SubmitField("Add Movie")



class StringListField(TextAreaField):
    def _value(self):
        #if there is value in self.data return a multi line string for self.data
        if self.data:
            return "\n".join(self.data)
        else:
            return ""
    

    def process_formdata(self, valuelist):
        #if there is something in valuelist[0]
        if valuelist and valuelist[0]:
            #self.data is assigned to all the lines in valuelist[0]
            self.data = [line.strip() for line in valuelist[0].split("\n")]
        #if valuelist is empty set self.data to empty list
        else:
            self.data = []


class ExtendedMovieForm(MovieForm):
    cast = StringListField("Cast")
    series = StringListField("Series")
    tags = StringListField("Tags")
    description = TextAreaField("Description")
    video_link = URLField("Video Link")

    submit = SubmitField("Submit")