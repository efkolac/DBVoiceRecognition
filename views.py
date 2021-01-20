from flask import render_template, request, session
import speech_recognition as sr
from database import *


def home_page():
    #database_puffer(100)
    return render_template("home.html")


def update_page():
    if request.method == "GET":
        p_name = session['username']
        p_mail = session['email']
        print("üst upgrade")
        return render_template("update_profile.html", place_n=p_name, place_m=p_mail)
    else:
        first_name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_id = session['id']
        update_user(first_name, email, password, user_id)
        return render_template("update_profile.html", place_n=first_name, place_m=email)


def show_student_page():
    student_list  = get_users("student")
    print("list is ", student_list)
    return render_template("studentlist.html", words=student_list)


def show_teacher_page():
    teacher_list = get_users("teacher")
    return render_template("teacherlist.html", words=teacher_list)


def texts_page():
    texts = get_texts()
    if len(texts) > 20:
        texts = texts[:20]
    print("in text page", texts)
    return render_template("texts.html", texts=texts)


def text_page(text_key):
    if request.method == "GET":
        text = get_text(text_key)
        text_title = text[0][2]
        text_content = text[0][1]
        print("text page", text)
        return render_template("text.html", text_title=text_title, text_content=text_content)
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
        save_content(r.recognize_google(audio), uploaded_file.filename, user_id)
        print("audio ekleme calisti")
        text = get_text(text_key)
        text_info = text[0][1]
        text_title = text[0][2]
        max_val = get_max_val(session['id'], text_title)[0][0]
        result = compare(text_info, r.recognize_google(audio)) * 100
        words = wrong_words(text_info, r.recognize_google(audio))
        save_score(result, user_id, text_title)
        records = get_pre_scores(user_id, text_title)
        tries = len(records)
        return render_template("results.html", title=text_title, result=result, records=records, words=words, max=max_val, tries=tries)


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
        account = check_user(email, password)

        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_type'] = account[4]
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
        return render_template("register.html", msg = "")
    else:
        park = request.form.get('type')  # returns on is checked, returns none otherwise
        print("park is", park)
        name = request.form["name"]
        email = request.form["email"]
        pw = request.form["password"]
        pwr = request.form["password-repeat"]
        user_type = request.form["user"]
        if user_type != "student" or user_type != "teacher":
            return render_template("register.html", msg="select a proper role")
        if pw != pwr or check_user(name, email):
            print("either pw is not right or user is already registered")
            return render_template("register.html", msg="either pw is not right or user is already registered")
        account = register_user(name, email, pw, user_type)

        session['loggedin'] = True
        session['id'] = account[0]  # account id
        session['user_type'] = account[4]
        session['username'] = account[1]  # account name
        return render_template("home.html")


def add_text_page():
    if request.method == "GET":
        return render_template("add_text.html")

    else:
        content = request.form["content"]
        title = request.form["title"]
        a = check_text(title)
        if a:
            update_text(title, content)
            return render_template("add_text.html")
        else:
            save_text(title, content)
            return render_template("add_text.html")


def contact_us_page():
    if request.method == "GET":
        return render_template("ContactUs.html")
    else:
        name = request.form['name']
        email = request.form["email"]
        message = request.form["message"]
        all_message = name + email + message
        return render_template("ContactUs.html")


def delete_text_page():
    if request.method == "GET":
        return render_template("delete_text.html")
    else:
        option = request.form.get('optradio')
        selection = request.form['title']
        print("option is ", option)
        if option == "text":
            delete_article(selection)
        elif option == "user":
            print("its in user")
            delete_audio_on_id(selection)
            delete_score_on_id(selection)
            delete_user(selection)
        elif option == "audio":
            delete_audio(selection)
        elif option == "score":
            delete_score(selection)
        else:
            print("error unknow type")
        return render_template("delete_text.html")
