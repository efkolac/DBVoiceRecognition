from flask import Flask, session
import views
import mysql.connector
from flask_login import LoginManager
from user import get_user
from flask_mail import Mail, Message

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
    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": "itudatabase21@gmail.com",
        "MAIL_PASSWORD": "2-nh7@XM*x,MDKL"
    }

    app.config.update(mail_settings)
    mail = Mail(app)
    app.config.from_object("settings")
    #app.config['MYSQL_HOST'] = 'localhost'
    #app.config['MYSQL_USER'] = 'root'
    #app.config['MYSQL_PASSWORD'] = '12345679'
    #app.config['MYSQL_DB'] = 'dbdeneme'
    #statement = "insert into content values (12,3232,32312,7)";
    #mycursor = mydb.cursor()
    #mycursor.execute(statement)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/add_text", view_func=views.add_text_page, methods=["GET", "POST"])
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/register", view_func=views.register_page, methods=["GET", "POST"])
    app.add_url_rule("/texts", view_func=views.texts_page, methods=["GET", "POST"])
    app.add_url_rule("/texts/<int:text_key>", view_func=views.text_page, methods=["GET", "POST"])
    app.add_url_rule("/audio", view_func=views.audio_add_page, methods=["GET", "POST"])
    app.add_url_rule("/contact_us", view_func=views.contact_us_page, methods=["GET", "POST"])
    app.add_url_rule("/update_page", view_func=views.update_page, methods=["GET", "POST"])
    app.add_url_rule("/delete_text", view_func=views.delete_text_page, methods=["GET", "POST"])

    #app.add_url_rule("/result", view_func=views.result)
    #lm.init_app(app)
    #lm.login_view = "login_page"

    return app


if __name__ == "__main__":
    app = create_app()
    app.secret_key = "123"
    port = app.config.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port)