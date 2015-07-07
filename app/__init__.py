from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ysvhneosgqbxbg:zS2KC0oHr8jAoll9tmYcsTafkg@ec2-54-204-27-193.compute-1.amazonaws.com:5432/dfisbei8v04jlc'
app.config['SECRET_KEY'] ='dlsf2k34fjlkj43LK'
app.config['DEBUG'] = True

db = SQLAlchemy(app)

from app import views, models