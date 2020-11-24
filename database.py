from movie import Movie
import mysql.connector
import views
from difflib import SequenceMatcher


def add_movie(self, movie):
    self._last_movie_key += 1
    self.movies[self._last_movie_key] = movie
    return self._last_movie_key


def delete_movie(self, movie_key):
    if movie_key in self.movies:
        del self.movies[movie_key]


def get_movie(self, movie_key):
    movie = self.movies.get(movie_key)
    if movie is None:
        return None
    movie_ = Movie(movie.title, year=movie.year) #neden movie yerine movie_ kullandık
    return movie_


def get_movies(self):
    movies = []
    for movie_key, movie in self.movies.items():
        movie_ = Movie(movie.title, year=movie.year)
        movies.append((movie_key, movie_))
    return movies


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
    mycursor = mydb.cursor()
    mycursor.execute(statement)
    mydb.commit()
    return "congrats"


def check_user(user_name, user_password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345679",
        database="newdb")
    statement = "select * from people where user_name = '{}' and  user_password = '{}';".format(user_name,user_password)
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
