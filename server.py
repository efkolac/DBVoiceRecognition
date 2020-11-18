from flask import Flask
import views
import mysql.connector
from flask_login import LoginManager
from user import get_user

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb"
    )
    print(mydb)
    app.config.from_object("settings")
    #app.config['MYSQL_HOST'] = 'localhost'
    #app.config['MYSQL_USER'] = 'root'
    #app.config['MYSQL_PASSWORD'] = '12345679'
    #app.config['MYSQL_DB'] = 'dbdeneme'
    #statement = "insert into content values (12,3232,32312,7)";
    #mycursor = mydb.cursor()
    #mycursor.execute(statement)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
#   app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/movies", view_func=views.movies_page)
    app.add_url_rule("/movies/<int:movie_key>", view_func=views.movie_page)
    app.add_url_rule("/new-movie", view_func=views.movie_add_page, methods=["GET", "POST"])
    app.add_url_rule("/audio", view_func=views.audio_add_page, methods=["GET", "POST"])
    lm.init_app(app)
    lm.login_view = "login_page"
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port)