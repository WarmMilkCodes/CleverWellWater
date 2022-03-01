from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras
from .views import views
#import io
#import csv
#import xlwt


app = Flask(__name__)
app.secret_key = 'super secret key'

# Development vs. Production Environment
'''
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/wells'
    
    DB_HOST = 'localhost'
    DB_NAME = 'wells'
    DB_USER = 'postgres'
    DB_PASS = 'postgres'
    
    conn = psycopg2.connect(dbname=DB_NAME, 
                            user=DB_USER, 
                            password=DB_PASS, 
                            host=DB_HOST)
else:
    app.debug = False
    #DATABASE_URL = HEROKU URL HERE
    
    
    DB_HOST = NULL
    DB_NAME = NULL
    DB_USER = NULL
    DB_PASS = NULL
        
    conn = psycopg2.connect(dbname=DB_NAME, 
                        user=DB_USER, 
                        password=DB_PASS, 
                        host=DB_HOST)
    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''

if __name__ == "__main__":
    app.run()
