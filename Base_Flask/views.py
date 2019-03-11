# Imports
from flask_pymongo import PyMongo
from flask import Flask, render_template, url_for, request, session, redirect

import matplotlib.pyplot as plt


# Configuration de l'application Flask avec la base de données Mongo
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'database_pipeline'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/database_pipeline'
app.config.update(SECRET_KEY='yoursecretkey')

mongo = PyMongo(app)

###FAIRE FICHIER DE FONCTIONS ? 

# 
def create_histo(collec_pipe_name):
    
    # Récupérer les indices de performances
    docs = list(mongo.db[collec_pipe_name].find())

    # REGRESSION
    if(docs[0]['R2'] != None):
        # Initialisation listes
        all_indices = ['R2', 'RMSE', 'Cross_val']
        all_graphs = []

        for j in all_indices :
            indice_liste = []
            date_liste = []
            for i in docs :
                indice_liste.append(i[j])
                date_liste.append(i['Time'])

            graph_indice = get_graph(date_liste, indice_liste, collec_pipe_name, j)
            all_graphs.append(graph_indice)

    # CLASSIFICATION
    elif (docs[0]['Confu'] != None):
        print('Classif')
        return 0

    return all_graphs


#
def get_graph(date_liste, indice_liste, collec_pipe_name, type_indice):

    graph = plt.plot(date_liste, indice_liste)

    fig, ax = plt.subplots()
    ax.plot(date_liste, indice_liste)
    fig.savefig("static/" + str(collec_pipe_name) + "_" + str(type_indice) + ".png")
    return graph

### TEST
print(create_histo("collection_pipeline_1"))


def get_last_scores(collec_pipe_name):
    if(collec_pipe_name != 'users'):
        docs = list(mongo.db[collec_pipe_name].find().sort([('Time', -1)]))
        last_doc = docs[0]
        
        all_indices = ['Time','R2', 'RMSE', 'Cross_val']
        
        #last_scores = []
        #for j in all_indices :
        #    last_scores.append(last_doc[j])

        last_scores = dict()
        for j in all_indices:
            last_scores[j] = last_doc[j]

        print(last_scores)

        return last_scores

    return "Bug collec users"


### TEST
get_last_scores("collection_pipeline_1")
print("Last_scores : ", get_last_scores("collection_pipeline_1"))




def get_collections():
    all_collec = mongo.db.collection_names()
    return all_collec


### TEST
print(get_collections())


def get_all_last_scores():
    all_last_scores = dict()
    for x in get_collections():
        if (x != 'users'):
            all_last_scores[x] = get_last_scores(x)

    return all_last_scores

### TEST
print(get_all_last_scores())



# Route principale de l'application Flask
@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        return render_template('main.html', username = session['username'], all_last_scores = get_all_last_scores())

    return render_template('index.html')


# Route d'inscription des utilisateurs
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['pass']})
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

# Route de déconnexion de l'utilisateur
@app.route('/deco')
def deconnection():
    del session['username']
    return redirect('/')
