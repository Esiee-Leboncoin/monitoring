# Imports
import pymongo
from flask import Flask, render_template, url_for, request, session, redirect

import config
from utils import bdd, graph, forms

import numpy as np

import matplotlib.pyplot as plt

# Initialisation et chargment du fichier Config
app = Flask(__name__)
app.config.from_object(config)

#Initialisation de la base de donnee
mongo = bdd.MongoDB("database_pipeline")

#app.config['MONGO_URI'] = 'mongodb://localhost:27017/database_pipeline'


# Route principale de l'application Flask
@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:

        form = forms.FirstGraphSelection(request.form)
        form2 = forms.SecondGraphSelection(request.form)
        form3 = forms.ThirdGraphSelection(request.form)
        form4 = forms.FourthGraphSelection(request.form)

        users = mongo.db.users

        graphJSON = users.find_one({'name' : session['username']})["up-left-graph"]
        graphJSON2 = users.find_one({'name' : session['username']})["up-right-graph"]
        graphJSON3 = users.find_one({'name' : session['username']})["down-left-graph"]
        graphJSON4 = users.find_one({'name' : session['username']})["down-right-graph"]

        up_left_collection = users.find_one({'name' : session['username']})["up-left-collection"]
        up_right_collection = users.find_one({'name' : session['username']})["up-right-collection"]
        down_left_collection = users.find_one({'name' : session['username']})["down-left-collection"]
        down_right_collection = users.find_one({'name' : session['username']})["down-right-collection"]

        if up_left_collection:
            graphJSON = mongo.get_graph_JSON(up_left_collection, 'RMSE', 'rgb(139, 205, 249)', False)
            users.update({'name' : session['username']}, {'$set': { "up-left-graph": graphJSON } })
        if up_right_collection:
            graphJSON2 = mongo.get_graph_JSON(up_right_collection, 'RMSE', 'rgb(147, 9, 4)', False)
            users.update({'name' : session['username']}, {'$set': { "up-right-graph": graphJSON2 } })
        if down_left_collection:
            graphJSON3 = mongo.get_graph_JSON(down_left_collection, 'RMSE', 'rgb(0, 117, 74)', False)
            users.update({'name' : session['username']}, {'$set': { "down-left-graph": graphJSON3 } })
        if down_right_collection:
            graphJSON4 = mongo.get_graph_JSON(down_right_collection, 'RMSE', 'rgb(160, 90, 4)', False)
            users.update({'name' : session['username']}, {'$set': { "down-right-graph": graphJSON4 } })

        if form.validate():
            graphJSON = mongo.get_graph_JSON(form.myField.data, 'RMSE', 'rgb(139, 205, 249)', False)
            users.update({'name' : session['username']}, {'$set': { "up-left-graph": graphJSON, "up-left-collection": form.myField.data } })
            up_left_collection = form.myField.data
        if form2.validate():
            graphJSON2 = mongo.get_graph_JSON(form2.myField2.data, 'RMSE', 'rgb(147, 9, 4)', False)
            users.update({'name' : session['username']}, {'$set': { "up-right-graph": graphJSON2, "up-right-collection": form2.myField2.data  } })
            up_right_collection = form2.myField2.data
        if form3.validate():
            graphJSON3 = mongo.get_graph_JSON(form3.myField3.data, 'RMSE', 'rgb(0, 117, 74)', False)
            users.update({'name' : session['username']}, {'$set': { "down-left-graph": graphJSON3, "down-left-collection": form3.myField3.data  } })
            down_left_collection = form3.myField3.data
        if form4.validate():
            graphJSON4 = mongo.get_graph_JSON(form4.myField4.data, 'RMSE', 'rgb(160, 90, 4)', False)
            users.update({'name' : session['username']}, {'$set': { "down-right-graph": graphJSON4, "down-right-collection": form4.myField4.data  } })
            down_right_collection = form4.myField4.data

        return render_template('graphs.html', up_left_pipeline = up_left_collection, up_right_pipeline = up_right_collection, down_left_pipeline = down_left_collection, down_right_pipeline = down_right_collection, form=form, form2=form2, form3=form3, form4=form4, username = session['username'], graphJSON=graphJSON, graphJSON2=graphJSON2, graphJSON3=graphJSON3, graphJSON4=graphJSON4, graphJSON_RMSE=0, graphJSON_R2=0, graphJSON_Cross_val=0)

    return render_template('index.html')

# Route afin d'analyser une pipeline
@app.route('/analysis/<pipeline>', methods=['POST', 'GET'])
def analysis(pipeline):
    if 'username' in session:

        pipelineForm = forms.PipelineToAnalyse(request.form)

        if pipelineForm.validate():
            pipelineName = pipelineForm.pipelineToAnalyse.data
            return redirect(url_for('analysis', pipeline=pipelineName))

        elif pipeline != "select_a_pipeline":
            pipeline_score = mongo.db[pipeline].find().sort([("Time", pymongo.DESCENDING)]).limit(1)[0]['RMSE']
            graphJSON_RMSE = mongo.get_graph_JSON(pipeline, 'RMSE', 'rgb(139, 205, 249)', True)
            graphJSON_R2 = mongo.get_graph_JSON(pipeline, 'R2', 'rgb(147, 9, 4)', True)
            graphJSON_Cross_val = mongo.get_graph_JSON(pipeline, 'Cross_val', 'rgb(0, 117, 74)', True)
            return render_template('analysis.html', username = session['username'], pipeline=pipeline, pipeline_score=round(pipeline_score,1), graphJSON_RMSE=graphJSON_RMSE, graphJSON_R2=graphJSON_R2, graphJSON_Cross_val=graphJSON_Cross_val, graphJSON=0, graphJSON2=0, graphJSON3=0, graphJSON4=0)

        return render_template('analysis.html', username = session['username'], pipeline=pipeline, pipelineForm=pipelineForm)

    return render_template('index.html')

# Route historique
@app.route('/history', methods=['POST', 'GET'])
def history():
    if 'username' in session:

        return render_template('history.html', username = session['username'])

    return render_template('index.html')

# Route afin d'ajouter une nouvelle pipeline
@app.route('/add_pipeline', methods=['POST', 'GET'])
def add_pipeline():
    if 'username' in session:

        return render_template('add_pipeline.html', username = session['username'])

    return render_template('index.html')


# Route d'inscription des utilisateurs
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['pass'], 'up-left-graph' : 0, 'up-left-collection' : 0, 'up-right-graph' : 0, 'up-right-collection' : 0, 'down-left-graph' : 0,'down-left-collection' : 0, 'down-right-graph' : 0, 'down-right-collection' : 0})
            session['username'] = request.form['username']
            return redirect('/')

        return redirect('/error_register')

    return render_template('register.html')

# Route de connexion des utilisateurs
@app.route('/login',methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user :
        if (request.form['pass'].encode('utf-8') == login_user['password'].encode('utf-8')):
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

# Route de deconnexion de l'utilisateur
@app.route('/deco')
def deconnection():
    del session['username']
    return redirect('/')


#Route de l'editeur de texte
@app.route('/editor', methods=['POST', 'GET'])
def editor():
    edit_status = "new"
    if edit_status == "new":
        with open("static/pipelines/default.py", 'r') as f:
            default = f.read()

        if request.method == 'POST':
            editordata = request.form.get("editordata")
            filename = request.form.get("filename")
            if filename[-3:] != ".py":
                filename += ".py"

            with open("static/pipelines/{}".format(filename), 'w') as f:
                f.write(editordata)

        return render_template('editor.html', default = default)

    if edit_status == "edit":
        with open("static/pipelines/default.py", 'r') as f:
            default = f.read()

        if request.method == 'POST':
            editordata = request.form.get("editordata")
            filename = request.form.get("filename")
            if filename[-3:] != ".py":
                filename += ".py"

            with open("static/pipelines/{}".format(filename), 'w') as f:
                f.write(editordata)

        return render_template('editor.html', default = default)
