from flask import Blueprint, render_template, session, redirect, request
from movie_library.forms import MovieForm

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

#base route
@pages.route("/")
def index():
    return render_template(
        "index.html",
        title="Movies Watchlist",
    )

#route for adding movies using the form
@pages.route("/add", methods=["GET", "POST"])
def add_movie():
    #create a form that is a MovieForm class
    form = MovieForm()

    if request.method == "POST":
        pass
    return render_template(
        "new_movie.html", 
        title="Movies Watchlist - Add Movie", 
        form=form
        )



#route for choosing theme if this route gets called the theme switches
@pages.route("/toggle-theme")
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