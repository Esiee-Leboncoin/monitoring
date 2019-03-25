import importlib
import matplotlib.pyplot as plt

def load_all_data(path):
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

def compute_performance(pipeline, modele, df):
    '''
        Permet d'appeler les bons indicateurs de performances et de récupérer
        les informations utiles selon la pipeline passé en paramètre. Retourne les
        performances associées.

        :params:
            pipeline : sortie de la pipeline
            modele : type du modèle utilisé : régression/classification)
            base : tuple des bases d'apprentissage et de test

        :type params:
            bool_type_modele: boolean
            base: tuple

        :return: les performances des différents indicateurs et graphiques
    '''
    if (modele == "régression") :
        print("Choix du type d'estimateur : Régression \n")
        perfs = compute_regression(pipeline, df)
        return perfs
        # poster les scores dans la database

    elif(modele == "classification"):
        print("Choix du type d'estimateur : Classification \n")
        perfs = compute_classification(pipeline, df)
        return perfs
        # poster les scores dans la database

    else:
        return -1

def indic_perform_reg_1(pipeline, df):
    '''
        Permet d'obtenir les résultats des indicateurs de performances d'une régression, et retourne ces derniers.

        :params:
            pipeline : sortie de la pipeline
            data : tuple des bases d'apprentissage et de test

        :return:
            rmse : score RMSE
            r2 : score R²
            cross_val : score de cross-validation
    '''
    # Pré-process ?
    df_pred = pipeline.predict(df)

    # Calcul du RMSE
    #rmse = sum(sqrt(df-pred))

    compute_R2(test[,c("Energie")], df_pred)

    # Calcul du R²
    ajusted_r2 = r2_score(df, pred)

    # Cross-Validation
    #cross_val = np.mean(cross_val_score(pipeline, df, df, cv=5))

    return rmse, r2


def get_pipeline(pipe_name):
    '''
        Selectionne et renvoie la pipeline selectionnée
    '''
