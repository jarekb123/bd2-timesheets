import os

SECRET_KEY = 'secret-key' # do zmiany
DEBUG = True

# ustawienia polaczenia z baza danych

DB_USERNAME = 'root'
DB_PASSWORD = ''
DB_NAME = 'bd2_project'
DB_HOST = os.getenv('IP', '127.0.0.1')
DB_URI = "mysql+pymsql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True