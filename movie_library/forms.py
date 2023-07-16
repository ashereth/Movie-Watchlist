from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField, URLField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo

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

#form for adding information about a movie that has already been added
class ExtendedMovieForm(MovieForm):
    cast = StringListField("Cast")
    series = StringListField("Series")
    tags = StringListField("Tags")
    description = TextAreaField("Description")
    video_link = URLField("Video Link")

    submit = SubmitField("Submit")

#form for user signups
class RegisterForm(FlaskForm):
    # Email() validator makes sure the email provided is a valid email
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", 
        validators=[InputRequired(),
                    Length(
                        min=4, 
                        max=20, 
                        message="Your password must be between 4 and 20 characters long."
                        )
                    ]
                )
    confirm_password = PasswordField(
        "Confirm password", 
        validators=[InputRequired(),
                    EqualTo(#validator to make sure the passwords match
                        "password", 
                        message="Please make sure your passwords match."
                        )
                    ]
                )
    submit = SubmitField("Register")


#create a form for loggin in
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")