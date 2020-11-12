from flask import Flask
import views
import mysql.connector
from flask_mysql_connector import MySQL


def create_app():
    app = Flask(__name__)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="dbdeneme"
    )
    print(mydb)
    app.config.from_object("settings")
    #app.config['MYSQL_HOST'] = 'localhost'
    #app.config['MYSQL_USER'] = 'root'
    #app.config['MYSQL_PASSWORD'] = '12345679'
    #app.config['MYSQL_DB'] = 'dbdeneme'
    statement = "insert into content values (12,3232,32312)";
    mycursor = mydb.cursor()
    mycursor.execute(statement)

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/movies", view_func=views.movies_page)
    app.add_url_rule("/movies/<int:movie_key>", view_func=views.movie_page)
    app.add_url_rule("/new-movie", view_func=views.movie_add_page, methods=["GET", "POST"])
    app.add_url_rule("/audio", view_func=views.audio_add_page, methods=["GET", "POST"])

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port)