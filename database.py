from movie import Movie
import mysql.connector
import views
from difflib import SequenceMatcher


def save_content(content_info, content_title, user_id):
    statement ="insert into content (content_info, content_title,user_id) values ('{}','{}','{}');"\
    .format(content_info,content_title,user_id)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb"
    )
    print(mydb)
    print("info is ",content_info,content_title,user_id)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "congrats"


def check_user(email, user_password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "select * from people where email = '{}' and  user_password = '{}';".format(email,user_password)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    account = mycursor.fetchone()
    return account


def save_text(title, data):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "insert into texts (data_content, data_title)values ('{}','{}');".format(data, title)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "text saved"


def retrieve_user(user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "select * from people where (id = '{}');".format(user_id)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    user = mycursor.fetchone()
    return user


def get_texts():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "select * from texts"
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    texts = mycursor.fetchall()
    return texts


def get_text(text_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "select * from texts where (id = '{}');".format(text_id)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    text = mycursor.fetchall()
    return text


def compare(text, audio_text):
    print("text in compare",text)
    print("audio in compare",audio_text)
    result = SequenceMatcher(None, text, audio_text).ratio()
    return result


def register_user(name, email, pw, degree):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "insert into people (user_name, user_password, email, user_type)values ('{}','{}','{}','{}');".format(name, email, pw, degree)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "user saved"
