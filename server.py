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
    app.config.from_object("settings")
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
    return app


if __name__ == "__main__":
    app = create_app()
    app.secret_key = "123"
    port = app.config.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port)
