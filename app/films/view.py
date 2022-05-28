from flask import render_template, Blueprint
from utils import search_by_title, search_by_years, search_by_rating, search_by_genre


film_blueprint = Blueprint('film_blueprint', __name__, template_folder='templates')


@film_blueprint.route('/movie/<title_>')
def get_by_title(title_):
    film = search_by_title(title_)
    length = len(film)
    return render_template("by_title.html", title_=title_, length=length, film=film)


@film_blueprint.route('/movie/<year_from>/to/<year_to>')
def get_by_years(year_from, year_to):
    films = search_by_years(year_from, year_to)
    length = len(films)
    return render_template("by_years.html", length=length, year_from=year_from, year_to=year_to, films=films)


@film_blueprint.route('/rating/<rating>')
def get_by_rating(rating):
    films = search_by_rating(rating)
    length = len(films)
    return render_template("by_rating.html", length=length, rating=rating, films=films)

@film_blueprint.route('/genre/<genre>')
def get_by_genre(genre):
    films = search_by_genre(genre)
    length = len(films)
    return render_template("by_genre.html", length=length, genre=genre, films=films)

