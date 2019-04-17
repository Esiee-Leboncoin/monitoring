from utils import bdd

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support

from os import listdir
from os.path import isfile, join
import importlib.util
from apscheduler.schedulers.background import BackgroundScheduler
import time
import os
import random

from . import bdd

class autoperform():
    def __init__(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.job, 'interval', minutes=1)
        scheduler.start()

    def job(self):
        all_pipes = get_all_pipes_names("static/pipelines")
        try :
            l.remove("default")
        except:
            pass
        for pipe in all_pipes:
            pipeline, modele, features, target, data = get_pipelines("static/pipelines/", pipe)
            data = load_data("static/data/{}".format(data))
            # Code à utiliser simplement pour la présentation
            data = data.sample(n=int(len(data)/3*2), random_state = random.randint(0,len(data)))
            data.reset_index(drop = True, inplace = True)
            # Code à utiliser simplement pour la présentation
            compute_performance(pipeline, modele, df=data, features=features ,target=target)


def save(pipe_name, path, contenu):
    '''
        Permet d'ajouter la pipeline passé en paramètre dans le path du dossier
        passé en paramètre.
    '''
    if pipe_name[-3:] != ".py":
        pipe_name += ".py"

    with open(path+pipe_name, 'w+') as f:
        f.write(contenu)

def delete(pipe_name, path):
    '''
        Permet de supprimé la pipeline passé en paramètre (contenu dans le path du dossier
        passé en paramètre).
    '''
    os.remove(path+pipe_name+".py")

def txt(pipe_name, path):
    '''
        Renvoie le contenu texte du fichier contenant la pipeline passé en paramètre
        (contenu dans le path du dossier passé en paramètre).
    '''
    with open(path+pipe_name+".py", 'r') as f:
        return f.read()


def add_metadata_property(obj, name):
    '''
        Permet d'ajouter un atribut à un objet existant
    '''
    setattr(obj, "name", name)


def load_data(path):
    '''
        Ouvre et lis le fichier passer en parmètre, reconnais seulement les types de
        fichier supportés par pandas : CSV, JSON, HTML, Local clipboard, MS Excel,
        HDF5 Format, feather Format, Parquet Format, Msgpack, Stata, SAS, Python Pickle
        Format, SQL, Google Big Query. Retourne les données lu.

        :params:
            path: path of the file

        :type params:
            path: string

        :return: object containing the data loaded in memory, or return -1 if type
                 not recognize.
    '''
    #On récupère le nom de l'extension du fichier
    type = path.split(".")[-1]

    #Selection de la bonne fonction de pandas à utiliser
    func_to_call = 'read_{}'.format(type)

    #Récupération de l'attribut de la fonction pour l'appeler
    try :
        func = getattr(pd, func_to_call)
    except :
        print("Pas de fonction disponible dans pandas pour lire les données")
        return -1

    #Lecture des données
    try :
        return func(path)
    except :
        print("Incorrect path")
        return -1


def descript_df(dataframe):
    '''
        Permet de faire une description rapide du dataframe de sortie. Retourne une
        description rapide des données.

        :params:
            dataframe: de faire une description rapide du dataframe de sortie

        :type params:
            dataframe: pandas.dataframe

        :return: description rapide des données
        :rtype: string
    '''
    print('Matrice de corrélation : \n')
    corr = dataframe.corr()
    corr_color = plt.matshow(corr, cmap=plt.cm.Reds)

    # Pour chaque colonne, montrer la répartition des valeurs (vérifier les valeurs aberrantes)
    # Kde et Histogramme
    i = 1
    for column in dataframe:
        i += 1
        plt.figure(i, figsize=(15,3))
        plt.subplot(121)
        dataframe[column].plot.kde()
        plt.title('Répartition de ' + column + ' : ')
        plt.subplot(122)
        dataframe[column].hist()
        plt.title('Histogramme de ' + column + ' : ')

    display = corr
    return display


def compute_performance(pipeline, modele, df,  features, target, BDD=True):
    '''
        Permet d'appeler les bons indicateurs de performances et de récupérer
        les informations utiles selon la pipeline passé en paramètre. Retourne les
        performances associées.

        :params:
            pipeline : object de type pipeline
            modele : type du modèle utilisé : régression/classification)
            features : colonnent à utiliser pour la régréssion
            target : colonne à prédire
            BDD : booléen, pour True les résultats sont stockés dans la BDD pour
                  False ils ne sont pas sauvegardés

        :type params:
            bool_type_modele: boolean
            base: tuple

        :return: les performances des différents indicateurs et graphiques
    '''
    if (modele == "regression") :
        print("Choix du type d'estimateur : Régression \n")
        result = compute_regression(pipeline, df, features, target)

    elif(modele == "classification"):
        print("Choix du type d'estimateur : Classification \n")
        result = compute_classification(pipeline, df, features, target)
    else:
        return -1

    if BDD == True:

        if pipeline.name[-3:] == ".py":
                    pipeline.name = pipeline.name[:-3]

        result['Time'] = datetime.datetime.now()
        result["_id"] = pipeline.name + "." + str(result['Time'])
        result["Type"] = modele
        mongo = bdd.MongoDB("database_pipeline")
        mongo.insert_one(pipeline.name, result)

    return result


def compute_regression(pipeline, df, features, target):
    '''
        Permet d'obtenir les résultats des indicateurs de performances d'une régression par crossvalidation,
        et retourne ces derniers.

        :params:
            pipeline : object de type pipeline
            df : tuple des bases d'apprentissage et de test
            features : colonnent à utiliser pour la régréssion
            target : colonne à prédire
            BDD : booléen, pour True les résultats sont stockés dans la BDD pour
                  False ils ne sont pas sauvegardés
        :return:
            r2 : score R2
            variance : variance gloable expliquée par le modèle
            rmse : root mean squared error
            intervalle_10 : une liste de 10 intervalles de confiances pris dans la list triés
                            des intervalles de confiances.
            intervalle_mean : moyenne de tous les intervalles de confiance
    '''

    # Calcul interval de confiance par bootstrap
    pred = bootstrap(pipeline, df, features, target, 200)
    inter_every_x = [2 * np.std(pred[i]) for i in pred.keys()]

    min_inter = min(inter_every_x)
    max_inter = min(inter_every_x)
    med_inter = np.median(inter_every_x)

    # Calcul de la variance globale expliqué, de r2 et du RMSE
    # par Cross-Validation
    scoring = {"variance" : "explained_variance",
               "r2" : "r2",
               "mse" : "neg_mean_squared_error"}
    result = cross_validate(pipeline, df[features], df[target], cv=5, scoring=scoring)
    variance = np.mean(result["test_variance"])
    r2 = np.mean(result["test_r2"])
    rmse = np.mean(np.sqrt(np.absolute(result["test_mse"])))

    result = {"r2": r2, "variance": variance, "rmse": rmse, "min_inter" : min_inter, "max_inter" : max_inter, "med_inter": med_inter}

    return result

def compute_classification(pipeline, df, features, target):
    '''
        Permet d'obtenir les résultats des indicateurs de performances d'une classification par crossvalidation,
        et retourne ces derniers.

        :params:
            pipeline : object de type pipeline
            df : tuple des bases d'apprentissage et de test
            features : colonnes à utiliser pour la régréssion
            target : colonne à prédire

        :return:
            Accuracy : score accuracy
            F1 : f1 score
            Precision : ratio TP/(TP+FP)
            Recall : ratio TP/(TP+FN)
    '''

    # Critères de scoring
    scoring = {"accuracy" : "accuracy",
               "f1_score" : "f1_macro",
               "precision" : "precision_macro",
               "recall" : "recall_macro"}

    # Cross Validation
    result = cross_validate(pipeline, df[features], df[target], cv=7, scoring=scoring)

    accuracy = np.mean(result["test_accuracy"])
    f1_score = np.mean(result["test_f1_score"])
    precision = np.mean(result["test_precision"])
    recall = np.mean(result["test_recall"])


    # Calcul de la Matrice de confusion
    #matrice_confu = pd.crosstab(base[3], pred, rownames=['True'], colnames=['Predicted'], margins=True)
    #C = np.array(matrice_confu)
    #score = np.sum(np.diag(C)) / len(base[3]) - 1
    #score_precision = (np.diag(C) / C[:,-1])[:-1]

    result = {"Accuracy" : accuracy, "F1" : f1_score, "Precision" : precision, "Recall" : recall}

    return result


def bootstrap(pipeline, data, features, target, n):
    '''
        Effectue un boostrap de la pipeline sur les données passées en paramètre.

        :params:
            pipeline : pipeline
            data : dataframe
            features : colonnent à utiliser pour la régréssion
            target : colonne à prédire
            n : nombres boostrap à faire

        :return:
            pred : dictionnaire contenant les valeurs bootstrap sous forme de liste pour chaque echantillons.
    '''
    length = len(data)
    keys = range(length)
    pred = {key: list() for key in keys}

    for b in range(n):
        #Random choice
        np.random.seed(b)
        index = np.random.choice(range(length), int(length/0.7))
        index_test = data.index.difference(index)
        train = data.loc[index]
        test = data.loc[index_test]

        #Fit des données
        pipeline.fit(train[features], train[target])

        #Prédiction et score sur la base de test
        for i, p in zip(index_test, pipeline.predict(test[features])):
            pred[i].append(p[0])

    return pred


def get_all_pipes_names(path):
    '''
        Liste  tous les fichiers (avec extensions) contenus dans le dossier passé en paramètre.

        :return: liste contenant les noms des fichiers sans l'extension
    '''
    l = [f for f in listdir(path) if isfile(join(path, f))]
    return l


def get_pipelines(path, pipe_name):
    '''
        Charge la pipeline dont le nom du fichier est passé en paramètre (avec extension). Et lui
        rajoute un atribut name contenant son nom.

        :params:
            path: lien du dossier
            pipe_file : nom du fichier de la pipeline.

        :type params:
            pipe_name: str

        :return:
            pipeline: objet contenant la pipeline
            modele: régression ou classification
            features: liste des features
            target: liste des target
            data: nom du fichier (str) cotenant les données
    '''
    if pipe_name[-3:] != ".py":
        pipe_name += ".py"

    spec = importlib.util.spec_from_file_location("module.name", path+pipe_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


    #import de la pipeline
    pipeline = module.pipeline
    modele = module.modele
    features = module.features
    target = module.target
    data = module.data

    # Ajout d'un nom à la pipeline
    add_metadata_property(pipeline, pipe_name)
    return pipeline, modele, features, target, data
