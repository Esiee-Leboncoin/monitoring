import matplotlib.pyplot as plt
from IPython.display import display_html

def create_histo(collec_pipe_name):

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

def mycfm(y_true, y_pred):
    """
    Rend une jolie matrice de confusion (cas binaire) et les principaux scores associés

    Arguments :
    -----------
    y_true: array
         les vraies classes
    y_pred: array
         les classes prédites
    """
    CC = pd.crosstab(y_true, y_pred, rownames=['True'], colnames=['Predicted'], margins=True)
    try:
        display_html(CC)
    except:
        print(CC)

    C = np.array(CC)
    score = np.sum(np.diag(C)) / len(y_true) - 1
    precision = np.diag(C) / C[:,-1]
    print()
    print('{s:{c}<{n}}{num:2.3}'.format(s='Score', n=15, c='', num=score))
