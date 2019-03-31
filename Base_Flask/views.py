# Imports
from flask import Flask, render_template, url_for, request, session, redirect

import config
from utils import bdd, graph

# Initialisation et chargment du fichier Config
app = Flask(__name__)
app.config.from_object(config)

#Initialisation de la base de donnée
mongo = bdd.MongoDB("database_pipeline")

# Route principale de l'application Flask
@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        return render_template('main.html',
            username = session['username'],
            all_last_scores = mongo.find_all_last(last=True))

    return render_template('index.html')

# Route d'inscription des utilisateurs
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = mongo.find("users", {'name' : request.form['username']})
        
        if len(existing_user) == 0:
            mongo.insert_one("users", {'name' : request.form['username'], 'password' : request.form['pass']})
            session['username'] = request.form['username']
            return redirect('/')

        return redirect('/error_register')

    return render_template('register.html')

# Route de connexion des utilisateurs
@app.route('/login',methods=['POST'])
def login():
    login_user = mongo.find("users", {'name' : request.form['username']})

    if len(login_user) != 0 :
        if (request.form['pass'].encode('utf-8') == login_user[0]['password'].encode('utf-8')):
            session['username'] = request.form['username']
            return redirect('/')

    return redirect('/error_login')

# Route d'erreur d'inscription
@app.route('/error_register')
def error_register():
    return render_template('error_register.html')

# Route d'erreur de connexion
@app.route('/error_login')
def error_login():
    return render_template('error_login.html')

# Route de déconnexion de l'utilisateur
@app.route('/deco')
def deconnection():
    del session['username']
    return redirect('/')
