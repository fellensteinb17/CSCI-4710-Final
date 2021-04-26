from flask import Flask, render_template, request, redirect, url_for,  flash
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.sql.expression import func
import os
import json
import csv
import pandas as pd
import requests

# get current app directory
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# define SQLAlchemy URL, a configuration parameter
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'smite.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

IMAGE_FOLDER = os.path.join('static', 'images')

app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

class Gods(db.Model):
	__tablename__ = 'Gods'
	image = db.Column(db.String(255))
	name = db.Column(db.String(20), primary_key=True)
	pantheon = db.Column(db.String(20))
	damage = db.Column(db.String(10))
	role = db.Column(db.String(10))
	def __repr__(self):
		return '<Gods %r >' % self.__dict__

class Relics(db.Model):
	__tablename__ = 'Relics'
	image = db.Column(db.String(255))
	name = db.Column(db.String(20), primary_key=True)
	def __repr__(self):
		return '<Relics %r >' % self.__dict__

@app.route('/', methods=['GET', 'POST'])
def index():    
    smite_logo = os.path.join(app.config['IMAGE_FOLDER'], 'SmiteLogo.png')

    db.drop_all()
    db.create_all()
    with open('smite_gods.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            newgod = Gods(image=row[0], name=row[1], pantheon=row[2], damage=row[3], role=row[4])
            db.session.add(newgod)
            db.session.commit()

    #db.drop_all()
    db.create_all()
    with open('relics.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            newrelic = Relics(image=row[0], name=row[1])
            db.session.add(newrelic)
            db.session.commit()

    db.create_all()

    if request.method == 'GET':
        return render_template('home.html', smite_logo = smite_logo)
        
    elif request.method =='POST':
        if request.form.get("damage-type") == "1":
            random_god = Gods.query.order_by(func.random()).limit(1)
            return render_template('home.html', smite_logo = smite_logo, data_god=random_god)

        elif request.form.get("damage-type") == "2":
            random_god = Gods.query.filter_by(damage=' Magical').order_by(func.random()).limit(1)
            return render_template('home.html', smite_logo = smite_logo, data_god=random_god)

        elif request.form.get("damage-type") == "3":
            random_god = Gods.query.filter_by(damage=' Physical').order_by(func.random()).limit(1)
            return render_template('home.html', smite_logo = smite_logo, data_god=random_god)
    #query_all_gods = Gods.query.filter_by(role=' Mage').all()
    #query_all_relics = Relics.query.all()
    #return render_template('home.html', smite_logo = smite_logo, column_gods=Gods.__table__.columns.keys(), data_gods= query_all_gods, column_relics=Relics.__table__.columns.keys(), data_relics= query_all_relics)


@app.route('/About')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
