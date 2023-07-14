import uuid
from movie_library.models import Movie
from dataclasses import asdict
from flask import (Blueprint, 
                   render_template, 
                   session, 
                   redirect, 
                   request, 
                   current_app, 
                   url_for,
                   abort,
                   )
from movie_library.forms import MovieForm

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

#base route
@pages.route("/")
def index():
    #get movie data from db and create a list of movie classes from them
    movie_data = current_app.db.movie.find({})
    movies = [Movie(**movie) for movie in movie_data]
    return render_template(
        "index.html",
        title="Movies Watchlist",
        movies_data=movies
    )

#route for adding movies using the form
@pages.route("/add", methods=["GET", "POST"])
def add_movie():
    #create a form that is a MovieForm class
    form = MovieForm()

    #checks if the form has been run and checks validation
    # if validation fails the errors for the fields get passed
    if form.validate_on_submit():
        #create a movie class from models.py and populate it with the form values
        movie = Movie(
            _id= uuid.uuid4().hex,
            title= form.title.data,
            director= form.director.data,
            year= form.year.data
            )
        #add the movie to mongodb as a dictionary
        # (all the default values will be included for the other fields)
        current_app.db.movie.insert_one(asdict(movie))

        return redirect(url_for(".index"))


    return render_template(
        "new_movie.html", 
        title="Movies Watchlist - Add Movie", 
        form=form
        )


#route for displaying a given movies details
@pages.get("/movie/<string:_id>")
def movie(_id: str):
    #create a Movie class using the info that we get from a given movie using .find_one(_id)
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
    return render_template("movie_details.html", movie=movie)


#route for choosing theme if this route gets called the theme switches
@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme is None:# set the default theme if it doesn't exist
        session["theme"] = "light"  
    elif current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
    # return the current page after switching themes
    return redirect(request.args.get("current_page"))