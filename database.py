import mysql.connector
from difflib import SequenceMatcher
from essential_generators import DocumentGenerator
import random


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
    statement = "select * from people where email = '{}' and  user_password = '{}';".format(email, user_password)
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


def wrong_words(texts, audio_text):
    audio = audio_text.split()
    text = texts.split()
    mylist = []
    for i in range(len(audio)):
        if text[i] in audio:
            print("this is in org text", text[i])
        else:
            mylist.append(text[i])
    print("wrong words are ", mylist)
    return mylist


def register_user(name, email, pw, degree):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "insert into people (user_name, user_password, email, user_type)values ('{}','{}','{}','{}');".format(name, pw, email, degree)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    account = check_user(email, pw)

    return account


def save_score(grade, user_id, content_title):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "insert into scores (grade, user_id, content_title)values ('{}','{}','{}');".format(grade, user_id, content_title)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "score saved"


def get_pre_scores(user_id, content_title):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "select * from scores where (user_id = '{}' and content_title ='{}');".format(user_id, content_title)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    text = mycursor.fetchall()
    return text


def update_user(name, email, password, user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "update people set user_name = '{}', user_password = '{}', email = '{}' where (id = '{}');".format(name, password, email, user_id)
    #statement = "delete from people where (id = '{}');".format(18)

    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "succesful"


def update_text(title, content):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "update texts set data_content = '{}' where (data_title = '{}');".format(content, title)

    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "succesful"


def check_text(title):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "select * from texts where data_title = '{}' ".format(title)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    account = mycursor.fetchone()
    return account


def delete_article(title):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "delete from texts where (data_title = '{}');".format(title)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "succesful"


def delete_user(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "delete from people where (id = '{}');".format(id)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "succesful"


def delete_audio(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "delete from content where (id = '{}');".format(id)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "succesful"


def delete_score(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "delete from scores where (id = '{}');".format(id)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "succesful"


def database_puffer(i):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    gen = DocumentGenerator()
    while i:
        user_id = i + 10
        grade = random.random() * 100
        content_title = "Virgat"
        statement = "insert into scores (grade, user_id, content_title)values ('{}','{}','{}');".format(grade, user_id, content_title)
        mycursor = mydb.cursor()
        mycursor.execute(statement)
        mydb.commit()
        i = i - 1
    return "score saved"


def get_users(type_of_user):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "select * from people where (user_type = '{}');".format(type_of_user)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    text = mycursor.fetchall()
    print("list is ", text)
    return text


def get_max_val(user_id, title):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "select max(grade) from scores where (content_title = '{}' and user_id = '{}');".format(title, user_id)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    text = mycursor.fetchall()
    print("list is ", text)
    return text


def delete_audio_on_id(user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "delete from content where (user_id = '{}');".format(user_id)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "succesful"


def delete_score_on_id(user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "delete from scores where (user_id = '{}');".format(user_id)
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "succesful"