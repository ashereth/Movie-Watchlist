import uuid
from movie_library.models import Movie
from dataclasses import asdict
import datetime
from flask import (Blueprint, 
                   render_template, 
                   session, 
                   redirect, 
                   request, 
                   current_app, 
                   url_for,
                   abort,
                   )
from movie_library.forms import MovieForm, ExtendedMovieForm

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



@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
def edit_movie(_id: str):
    #get movie class data
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
    #create a form using our extended form class passing our movie object
    form = ExtendedMovieForm(obj=movie)
    if form.validate_on_submit():
        #populate all the fields for the movie class
        movie.title = form.title.data
        movie.description = form.description.data
        movie.year = form.year.data
        movie.cast = form.cast.data
        movie.series = form.series.data
        movie.tags = form.tags.data
        movie.video_link = form.video_link.data
        #update the movie passing it as a dictionary so that mongodb can use it
        current_app.db.movie.update_one(
            {"_id": movie._id},
            {"$set": asdict(movie)}
              )
        return redirect(url_for(".movie", _id=movie._id))
    return render_template("movie_form.html", movie=movie, form=form)



#route for displaying a given movies details
@pages.get("/movie/<string:_id>")
def movie(_id: str):
    #create a Movie class using the info that we get from a given movie using .find_one(_id)
    movie = Movie(**current_app.db.movie.find_one({"_id": _id}))
    return render_template("movie_details.html", movie=movie)

#route for changing rating of a movie
@pages.get("/movie/<string:_id>/rate")
def rate_movie(_id):
    #get the new rating
    rating = int(request.args.get("rating"))
    #update the rating of the movie with the new rating
    current_app.db.movie.update_one({"_id": _id}, {"$set": {"rating": rating}})
    return redirect(url_for(".movie", _id=_id))


#for marking a movie as watched today
@pages.get("/movie/<string:_id>/watch")
def watch_today(_id):
    #update the last_watched parameter with todays date
    current_app.db.movie.update_one(
        {"_id": _id}, 
        {"$set": {"last_watched": datetime.datetime.today()}})
    return redirect(url_for(".movie", _id=_id))


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