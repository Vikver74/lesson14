from flask import Flask
from app.films.view import film_blueprint

app = Flask(__name__)

app.register_blueprint(film_blueprint)

if __name__ == '__main__':
    app.run()
