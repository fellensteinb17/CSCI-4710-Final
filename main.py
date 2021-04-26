from flask import Flask, render_template, request, redirect, url_for,  flash
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.sql.expression import func
import os
import json
import csv
import pandas as pd
import requests
import util

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

smite_logo = os.path.join(app.config['IMAGE_FOLDER'], 'SmiteLogo.png')

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

class Items(db.Model):
	__tablename__ = 'Items'
	name = db.Column(db.String(40), primary_key=True)
	image = db.Column(db.String(255))
	mage = db.Column(db.Boolean)
	gaurdian = db.Column(db.Boolean)
	hunter = db.Column(db.Boolean)
	assassin = db.Column(db.Boolean)
	warrior = db.Column(db.Boolean)
	def __repr__(self):
		return '<Items %r >' % self.__dict__

class Boots(db.Model):
	__tablename__ = 'Boots'
	name = db.Column(db.String(40), primary_key=True)
	image = db.Column(db.String(255))
	mage = db.Column(db.Boolean)
	gaurdian = db.Column(db.Boolean)
	hunter = db.Column(db.Boolean)
	assassin = db.Column(db.Boolean)
	warrior = db.Column(db.Boolean)
	def __repr__(self):
		return '<Boots %r >' % self.__dict__

class Starters(db.Model):
	__tablename__ = 'Starters'
	name = db.Column(db.String(40), primary_key=True)
	image = db.Column(db.String(255))
	mage = db.Column(db.Boolean)
	gaurdian = db.Column(db.Boolean)
	hunter = db.Column(db.Boolean)
	assassin = db.Column(db.Boolean)
	warrior = db.Column(db.Boolean)
	def __repr__(self):
		return '<Starters %r >' % self.__dict__

@app.route('/')
def index():    
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
    with open('items.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            newitem = Items(name=row[0], image=row[1], mage=row[2], gaurdian=row[3], hunter=row[4], assassin=row[5], warrior=row[6])
            db.session.add(newitem)
            db.session.commit()

    db.create_all()
    with open('boots.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            newboot = Boots(name=row[0], image=row[1], mage=row[2], gaurdian=row[3], hunter=row[4], assassin=row[5], warrior=row[6])
            db.session.add(newboot)
            db.session.commit()

    db.create_all()
    with open('starters.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            newstarter = Starters(name=row[0], image=row[1], mage=row[2], gaurdian=row[3], hunter=row[4], assassin=row[5], warrior=row[6])
            db.session.add(newstarter)
            db.session.commit()

    return render_template('home.html', smite_logo = smite_logo)
    #query_all_gods = Gods.query.filter_by(role=' Mage').all()
    #query_all_relics = Relics.query.all()
    #return render_template('home.html', smite_logo = smite_logo, column_gods=Gods.__table__.columns.keys(), data_gods= query_all_gods, column_relics=Relics.__table__.columns.keys(), data_relics= query_all_relics)

@app.route('/random', methods=['POST'])
def random():
    if_boots = request.form.get("boots")
    if if_boots:
        boots = Boots.query.all()
    else:
        boots = "nothing"

    if_starter = request.form.get("starter")
    if if_starter:
        starters = Starters.query.all()
    else:
        starters = "nothing"

    items = Items.query.all()

    if request.form.get("damage-type") == "1":
        random_god = Gods.query.order_by(func.random()).limit(1)

    elif request.form.get("damage-type") == "2":
        random_god = Gods.query.filter_by(damage=' Magical').order_by(func.random()).limit(1)

    elif request.form.get("damage-type") == "3":
        random_god = Gods.query.filter_by(damage=' Physical').order_by(func.random()).limit(1)

    return render_template('home.html', smite_logo = smite_logo, data_god=random_god, data_items=items[0])#util.items(random_god, items, if_boots, boots, if_starter, starters))

@app.route('/About')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
