import functools
import uuid
import datetime
from dataclasses import asdict

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    session,
    url_for,
    request,
)
from movie_library.forms import LoginForm, RegisterForm, MovieForm, ExtendedMovieForm
from movie_library.models import User, Movie
from passlib.hash import pbkdf2_sha256


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))

        return route(*args, **kwargs)

    return route_wrapper

#base route
@pages.route("/")
@login_required#user must be logged in to see this page
def index():
    #get current user data and make a User object with it
    user_data = current_app.db.user.find_one({"email": session["email"]})
    user = User(**user_data)
    #get movie data that is in the current users list of movies and make a list of Movie objects
    movie_data = current_app.db.movie.find({"_id": {"$in": user.movies}})
    movies = [Movie(**movie) for movie in movie_data]

    return render_template(
        "index.html",
        title="Movies Watchlist",
        movies_data=movies,
    )

#route for registering users
@pages.route("/register", methods=["POST", "GET"])
def register():
    #if session already has a logged in email redirect to base route
    if session.get("email"):
        return redirect(url_for(".index"))

    form = RegisterForm()
    #if form is submitted and validated then get the data from it and save it as user
    if form.validate_on_submit():
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
        )
        #add user to the database of users
        current_app.db.user.insert_one(asdict(user))
        #flash a success message
        flash("User registered successfully", "success")
        #redirect user to login page
        return redirect(url_for(".login"))

    return render_template(
        "register.html", title="Movies Watchlist - Register", form=form
    )

#route for logging in
@pages.route("/login", methods=["GET", "POST"])
def login():
    #if user is already signed in redirect to base
    if session.get("email"):
        return redirect(url_for(".index"))
    #create form and check validation
    form = LoginForm()

    if form.validate_on_submit():
        #try to find the user in the db using the email from the form
        user_data = current_app.db.user.find_one({"email": form.email.data})
        #if couldnt find user data using the email flash message
        if not user_data:
            flash("Login credentials not correct", category="danger")
            return redirect(url_for(".login"))
        #create a user object using user_data that we got using the email
        user = User(**user_data)
        # check if the form password equals the user password
        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            #populate the session with anything that we need and redirect to base
            session["user_id"] = user._id
            session["email"] = user.email

            return redirect(url_for(".index"))

        flash("Login credentials not correct", category="danger")
    #if user couldnt be verified return to login page
    return render_template("login.html", title="Movies Watchlist - Login", form=form)

#logout route
@pages.route("/logout")
def logout():
    #clear everything from session except the theme
    del session["email"]
    del session["user_id"]

    return redirect(url_for(".login"))

#route for adding movies using the form
@pages.route("/add", methods=["GET", "POST"])
@login_required
def add_movie():
    form = MovieForm()

    if form.validate_on_submit():
        movie = Movie(
            _id=uuid.uuid4().hex,
            title=form.title.data,
            director=form.director.data,
            year=form.year.data,
        )

        current_app.db.movie.insert_one(asdict(movie))

        current_app.db.user.update_one(
            {"_id": session["user_id"]}, {"$push": {"movies": movie._id}}
        )

        return redirect(url_for(".movie", _id=movie._id))

    return render_template(
        "new_movie.html", title="Movies Watchlist - Add Movie", form=form
    )




@pages.route("/edit/<string:_id>", methods=["GET", "POST"])
@login_required#user must be logged in
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
@login_required#user must be logged in
def rate_movie(_id):
    #get the new rating
    rating = int(request.args.get("rating"))
    #update the rating of the movie with the new rating
    current_app.db.movie.update_one({"_id": _id}, {"$set": {"rating": rating}})
    return redirect(url_for(".movie", _id=_id))


#for marking a movie as watched today
@pages.get("/movie/<string:_id>/watch")
@login_required#user must be logged in
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