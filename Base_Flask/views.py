# Imports
import pymongo
from flask import Flask, render_template, url_for, request, session, redirect, flash

import config
from utils import bdd, graph, forms, pipelines

import numpy as np

import matplotlib.pyplot as plt
import os
from werkzeug.utils import secure_filename
import threading
import dateutil.parser as parser
import re

# Initialisation et chargment du fichier Config
app = Flask(__name__)
app.config.from_object(config)

#Initialisation de la base de donnee
mongo = bdd.MongoDB("database_pipeline")
threading.Thread(None, pipelines.autoperform())
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

        forms.UpdateGraph(form)

        if up_left_collection:
            graphJSON = mongo.get_graph_type(up_left_collection,'rgb(139, 205, 249)')
            users.update({'name' : session['username']}, {'$set': { "up-left-graph": graphJSON } })
        if up_right_collection:
            graphJSON2 = mongo.get_graph_type(up_right_collection,'rgb(147, 9, 4)')
            users.update({'name' : session['username']}, {'$set': { "up-right-graph": graphJSON2 } })
        if down_left_collection:
            graphJSON3 = mongo.get_graph_type(down_left_collection,'rgb(0, 117, 74)')
            users.update({'name' : session['username']}, {'$set': { "down-left-graph": graphJSON3 } })
        if down_right_collection:
            graphJSON4 = mongo.get_graph_type(down_right_collection,'rgb(160, 90, 4)')
            users.update({'name' : session['username']}, {'$set': { "down-right-graph": graphJSON4 } })

        if form.validate():
            selected_collection = form.myField.data
            graphJSON = mongo.get_graph_type(selected_collection,'rgb(139, 205, 249)')
            users.update({'name' : session['username']}, {'$set': { "up-left-graph": graphJSON, "up-left-collection": selected_collection } })
            up_left_collection = selected_collection
        if form2.validate():
            selected_collection = form2.myField2.data
            graphJSON2 = mongo.get_graph_type(selected_collection,'rgb(147, 9, 4)')
            users.update({'name' : session['username']}, {'$set': { "up-right-graph": graphJSON2, "up-right-collection": selected_collection  } })
            up_right_collection = selected_collection
        if form3.validate():
            selected_collection = form3.myField3.data
            graphJSON3 = mongo.get_graph_type(selected_collection,'rgb(0, 117, 74)')
            users.update({'name' : session['username']}, {'$set': { "down-left-graph": graphJSON3, "down-left-collection": selected_collection  } })
            down_left_collection = selected_collection
        if form4.validate():
            selected_collection = form4.myField4.data
            graphJSON4 = mongo.get_graph_type(selected_collection,'rgb(160, 90, 4)')
            users.update({'name' : session['username']}, {'$set': { "down-right-graph": graphJSON4, "down-right-collection": selected_collection  } })
            down_right_collection = selected_collection

        return render_template('graphs.html', up_left_pipeline = up_left_collection, up_right_pipeline = up_right_collection, down_left_pipeline = down_left_collection, down_right_pipeline = down_right_collection, form=form, form2=form2, form3=form3, form4=form4, username = session['username'], graphJSON=graphJSON, graphJSON2=graphJSON2, graphJSON3=graphJSON3, graphJSON4=graphJSON4, graphJSON_RMSE=0, graphJSON_R2=0, graphJSON_Variance=0, active_item="active_home")

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
            if mongo.db[pipeline].find_one({'Type' : 'regression'}):
                pipeline_score = mongo.db[pipeline].find().sort([("Time", pymongo.DESCENDING)]).limit(1)[0]['RMSE']
                graphJSON_RMSE = mongo.get_graph_JSON(pipeline, 'RMSE', 'rgb(139, 205, 249)', True)
                graphJSON_R2 = mongo.get_graph_JSON(pipeline, 'R2', 'rgb(147, 9, 4)', True)
                graphJSON_Variance = mongo.get_graph_JSON(pipeline, 'Variance', 'rgb(0, 117, 74)', True)
            else:
                pipeline_score = mongo.db[pipeline].find().sort([("Time", pymongo.DESCENDING)]).limit(1)[0]['Accuracy']*100
                graphJSON_RMSE = mongo.get_graph_JSON(pipeline, 'F1', 'rgb(139, 205, 249)', True)
                graphJSON_R2 = mongo.get_graph_JSON(pipeline, 'Precision', 'rgb(147, 9, 4)', True)
                graphJSON_Variance = mongo.get_graph_JSON(pipeline, 'Recall', 'rgb(0, 117, 74)', True)
            return render_template('analysis.html', username = session['username'], pipeline=pipeline, pipeline_score=round(pipeline_score,1), graphJSON_RMSE=graphJSON_RMSE, graphJSON_R2=graphJSON_R2, graphJSON_Variance=graphJSON_Variance, graphJSON=0, graphJSON2=0, graphJSON3=0, graphJSON4=0, active_item="active_analysis")

        return render_template('analysis.html', username = session['username'], pipeline=pipeline, pipelineForm=pipelineForm, active_item="active_analysis")

    return render_template('index.html')

# Route historique
@app.route('/history', methods=['POST', 'GET'])
def history():
    if 'username' in session:
        #all_collections = mongo.db.collection_names()
        #if ("users" in all_collections):
        #    all_collections.remove("users")
        #for c in all_collections:
        #    pipeline_list = mongo.db[c].find().sort([("Time", pymongo.DESCENDING)])
        pipeline_list = mongo.db["pipe_romain"].find().sort([("Time", pymongo.DESCENDING)])
        pipeline_info = []
        for elt in pipeline_list:
            if elt["Type"] == "classification":
                pipeline_info.append([" ID : "+str(elt["_id"])," | Pipeline Type : " +str(elt["Type"])," Accuracy : "+str(elt["Accuracy"])," | Precision : " +str(elt["Precision"])," | F1 : " +str(elt["F1"])," | Recall : "+ str(elt["Recall"])])
            elif elt["Type"] == "regression":
                pipeline_info.append([" ID : "+str(elt["_id"])," | Pipeline Type : " +str(elt["Type"])," R2 : "+str(elt["R2"])," | Variance : " +str(elt["Variance"])," | RMSE : " +str(elt["RMSE"])," | Med : "+ str(elt["med_inter"])])
        return render_template('history.html', username = session['username'],pipeline_info = pipeline_info, active_item="active_history")

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


#Route de l'édition des pipelines
@app.route('/add_pipeline', methods=['POST', 'GET'])
def add_pipeline():
    if 'username' in session:

        formeditor = forms.PipelineSelectEditor(request.form)
        default = pipelines.txt("default", "static/pipelines/")

        if request.method == 'POST':
            if formeditor.validate():
                pipe_name = formeditor.pipToEdit.data

                if formeditor.display.data == True:
                    pipeline = pipelines.txt(pipe_name, "static/pipelines/")
                    return render_template('add_pipeline.html', pipe_name = pipe_name, default = pipeline, formeditor = formeditor,
                                            username = session['username'], active_item="active_add")

                if formeditor.delete.data == True:
                    if pipe_name == "default":
                        flash("Vous ne pouvez pas supprimer cette pipeline")
                        return render_template('add_pipeline.html', pipe_name = "default", default = default, formeditor = formeditor,
                                                username = session['username'], active_item="active_add")
                    pipelines.delete(pipe_name, "static/pipelines/")
                    forms.UpdateEditor(formeditor)
                    flash("Pipeline supprimé")
                    return render_template('add_pipeline.html', pipe_name = "default", default = default, formeditor = formeditor,
                                            username = session['username'], active_item="active_add")

            #Enregistre seulement la pipeline
            if request.form.get('Enregistrer'):

                editordata = request.form.get("editordata")
                pipe_name = request.form.get("pipe_name")

                pipelines.save(pipe_name, "static/pipelines/", editordata)
                forms.UpdateEditor(formeditor)
                flash("Pipeline {} importée".format(pipe_name))

                if pipe_name[-3:] == ".py":
                    pipe_name = pipe_name[:-3]

                return render_template('add_pipeline.html',  pipe_name = pipe_name, default = editordata, formeditor = formeditor,
                                        username = session['username'], active_item="active_add")

            #Enregistre seulement la pipeline puis effectue les caluls de performance dessus
            if request.form.get('Test'):

                editordata = request.form.get("editordata")
                pipe = request.form.get("pipe_name")

                pipelines.save(pipe_name, "static/pipelines/", editordata)
                forms.UpdateEditor(formeditor)
                flash("Pipeline {} importée".format(pipe_name))

                if 'file' not in request.files:
                    flash('Pas de fichier')

                else:
                    file = request.files['file']

                    if file.filename == '':
                        flash('Fichier sans extension')

                    elif file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save("static/data/{}".format(filename))
                        flash('Fichier importé')

                        #Calcul des performances
                        try:
                            pipeline, modele, features, target, data = pipelines.get_pipelines("static/pipelines/", pipe)
                            data = pipelines.load_data("static/data/{}".format(filename))
                            pipelines.compute_performance(pipeline, modele, df=data, features=features ,target=target)
                        except Exception as e:
                            flash(e)
                    else:
                        flash('Fichier non pris en charge')

                    return render_template('add_pipeline.html',  pipe_name = pipe, default = editordata, formeditor = formeditor,
                                            username = session['username'], active_item="active_add")

        return render_template('add_pipeline.html', pipe_name = "default", default = default, formeditor = formeditor,
                                username = session['username'], active_item="active_add")

    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
