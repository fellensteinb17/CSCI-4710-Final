from flask import Flask, render_template, request, redirect, url_for,  flash
import os
import json
import pandas as pd
import requests

IMAGE_FOLDER = os.path.join('static', 'images')


app = Flask(__name__)


app.config['IMAGE_FOLDER'] = IMAGE_FOLDER



@app.route('/')
def main():
    
    smite_logo = os.path.join(app.config['IMAGE_FOLDER'], 'SmiteLogo.png')

    return render_template('home.html', smite_logo = smite_logo)
    
@app.route('/About')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
