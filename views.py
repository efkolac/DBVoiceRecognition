from datetime import datetime
from movie import Movie
from flask import render_template,current_app, request, redirect, url_for, session
import speech_recognition as sr
from database import *
import flask_mysqldb


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def movies_page():
    db = current_app.config["db"]
    if request.method == "GET":
        movies = db.get_movies()
        return render_template("movies.html", movies=sorted(movies))
    else:
        form_movie_keys = request.form.getlist("movie_keys")
        for form_movie_key in form_movie_keys:
            db.delete_movie(int(form_movie_key))
        return redirect(url_for("movies_page"))


def movie_page(movie_key):
    db = current_app.config["db"]
    movie = db.get_movie(movie_key)
    return render_template("movie.html", movie=movie)


def movie_add_page():
    if request.method == "GET":
        return render_template(
            "movie_edit.html", min_year=1887, max_year=datetime.now().year
        )
    else:
        form_title = request.form["title"]
        form_year = request.form["year"]
        movie = Movie(form_title, year=int(form_year) if form_year else None)
        db = current_app.config["db"]
        movie_key = db.add_movie(movie)
        return redirect(url_for("movie_page", movie_key=movie_key))


def audio_add_page():

    if request.method == "GET":
        return render_template("audio.html")
    else:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
            print("name of the file that uploaded",uploaded_file.filename)
            print("type of the file name", type(uploaded_file))
            sound = uploaded_file.filename
            r = sr.Recognizer()
            with sr.AudioFile(sound) as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                try:
                    print("type of the file", type(r.recognize_google(audio)))
                    print("str[0]", r.recognize_google(audio)[0])
                    print("Converted Audio Is : \n" + r.recognize_google(audio))
                except Exception as e:
                    print("Error {} : ".format(e))

        user_id = 7
        save_content(r.recognize_google(audio),uploaded_file.filename, user_id)
        print("audio ekleme calisti")
        return render_template("audio.html", file_name=uploaded_file.filename, content=r.recognize_google(audio))


def login_page():
    # Output message if something goes wrong...
    msg = 'this is for variable msg'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        account = check_user(username,password)

        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['degree'] = account[6]
            session['id'] = account[0] #account id
            print("id",session['id'])
            print("account",account)
            session['username'] = account[1] #account name
            # Redirect to home page
            return render_template("home.html", day=session['username'])
        else:
            print("user does not exist")

        # If account exists in accounts table in out database
    return render_template('login.html', msg='')


def logout_page():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('degree', None)
# Redirect to login page
    day_name = "dayssss"
    return render_template("home.html", day=day_name)


def add_text_page():
    if request.method == "GET":
        return render_template("data_add.html")

    else:
        title = request.form["title"]
        data = request.form["data"]
        save_text(title,data)
        return render_template("data_add.html")


def profile_page():
    user_id = session['id']
    info = retrieve_user(user_id)
    name = info[1]
    password = info[2]
    return render_template("profile.html",name = name, password = password)


def texts_page():
    texts = get_texts()
    print("texts", texts)
    return render_template("texts.html", texts=texts)




