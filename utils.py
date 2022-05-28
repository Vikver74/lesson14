import sqlite3
from flask import jsonify


def execute_sql_request(sql_query):
    with sqlite3.connect('data/netflix.db') as connection:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return result


def search_by_title(title):
    sql_query = f"""
                SELECT title, country, release_year, listed_in, description
                FROM netflix 
                WHERE title LIKE '%{title}%'
                ORDER BY release_year DESC LIMIT 1
                """
    result = execute_sql_request(sql_query)
    film = {}
    if len(result) > 0:
        film = {
                    "title": result[0][0],
                    "country": result[0][1],
                    "release_year": result[0][2],
                    "genre": result[0][3],
                    "description": result[0][4]
                }
    return film


def search_by_years(year_from, year_to):
    sql_query = f"""
                SELECT title, release_year
                FROM netflix 
                WHERE release_year BETWEEN '{year_from}' AND '{year_to}'
                LIMIT 100
                """
    result = execute_sql_request(sql_query)
    films = []
    if len(result) > 0:
        for record in result:
            films.append({"title": record[0], "release_year": record[1]})
    return films


def search_by_rating(rating):
    film_rating = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    sql_query = f"""
                SELECT title, rating, description
                FROM netflix 
                WHERE rating IN ({film_rating[rating]})
                LIMIT 100
                """
    result = execute_sql_request(sql_query)
    films = []
    if len(result) > 0:
        for record in result:
            films.append({"title": record[0], "rating": record[1], "description": record[2]})
    return films


def search_by_genre(genre):
    sql_query = f"""
                SELECT title,  description
                FROM netflix 
                WHERE listed_in LIKE '%{genre}%'
                ORDER BY release_year DESC LIMIT 10
                """
    result = execute_sql_request(sql_query)
    films = []
    if len(result) > 0:
        for record in result:
            films.append({"title": record[0], "description": record[1]})
    return films


def search_by_actors(actor1, actor2):
    actors = [actor1, actor2]
    sql_query = f"""
                SELECT title, netflix.cast FROM netflix
                WHERE netflix.cast LIKE '%{actor1}%' AND netflix.cast LIKE '%{actor2}%'
                """
    result = execute_sql_request(sql_query)

    all_actors_list = []
    for record in result:
        all_actors_list.extend(record[0].split(', '))

    target_actors = set()
    for item in all_actors_list:
        if not (item in actors):
            if all_actors_list.count(item) > 2:
                target_actors.add(item)

    return list(target_actors)


def search_by_type_year_genre(type_, year, genre):
    sql_query = f"""
                SELECT title, description
                FROM netflix 
                WHERE type = '{type_}' AND release_year = '{year}' AND listed_in LIKE '%{genre}%'
                """
    result = execute_sql_request(sql_query)
    data_json = []
    for item in result:
        data_json.append({'title': item[0], 'description': item[1]})
    return jsonify(data_json)
