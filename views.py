from datetime import datetime
from flask import render_template,current_app, request, redirect, url_for, session
import speech_recognition as sr
from database import *
from server import *


def home_page():
    return render_template("home.html")


def update_page():
    if request.method == "GET":
        p_name = session['username']
        p_mail = session['email']

        return render_template("update_profile.html", place_n=p_name, place_m=p_mail)

    return render_template("update_profile.html")


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

        user_id = 10
        save_content(r.recognize_google(audio),uploaded_file.filename, user_id)
        print("audio ekleme calisti")
        return render_template("audio.html", file_name=uploaded_file.filename, content=r.recognize_google(audio))


def login_page():
    # Output message if something goes wrong...
    msg = 'this is for variable msg'
    if request.method == 'POST':
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        print("it is in post part of login")
        account = check_user(email, password)

        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_type'] = account[6]
            session['id'] = account[0] #account id
            session['email'] = account[3]
            print("id",session['id'])
            print("account",account)
            session['username'] = account[1] #account name
            # Redirect to home page
            return render_template("home.html",auth = "user")
        else:
            print("user does not exist")
        # If account exists in accounts table in out database
    return render_template('login.html')


def logout_page():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('user_type', None)
# Redirect to login page
    day_name = "dayssss"
    return render_template("home.html")


def register_page():
    if request.method == "GET":
        print("in register get")
        return render_template("register.html")
    else:
        park = request.form.get('type')  # returns on is checked, returns none otherwise
        print("park is", park)
        name = request.form["name"]
        email = request.form["email"]
        pw = request.form["password"]
        pwr = request.form["password-repeat"]
        user_type = request.form["user"]
        if pw != pwr or check_user(name, email):
            print("either pw is not right or user is already registered")
            return render_template("register.html")
        register_user(name, email, pw, user_type)
        account = check_user(email, pw)

        print("account is ", account)
        session['loggedin'] = True
        session['id'] = account[0]  # account id
        session['user_type'] = account[6]
        session['username'] = account[1]  # account name
        return render_template("home.html")


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
    for text in texts:
        print("text", text[1])
    #print("texts", texts)
    return render_template("texts.html", texts=texts)


def text_page(text_key):
    if request.method == "GET":
        text = get_text(text_key)
        print("text",text)
        return render_template("text.html", text=text)
    else:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
            sound = uploaded_file.filename
            r = sr.Recognizer()
            with sr.AudioFile(sound) as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
        user_id = session['id']
        save_content(r.recognize_google(audio),uploaded_file.filename, user_id)
        print("audio ekleme calisti")
        text = get_text(text_key)
        text_info = text[0][1]
        text_title = text[0][2]
        result = compare(text_info, r.recognize_google(audio))
        return render_template("results.html", title=text_title, result=result)


def contact_us_page():
    if request.method == "GET":
        return render_template("ContactUs.html")
    else:
        name = request.form['name']
        email = request.form["email"]
        message = request.form["message"]
        all_message = name + email + message
        return render_template("ContactUs.html")
