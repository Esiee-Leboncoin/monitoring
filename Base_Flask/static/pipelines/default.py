#Imports
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA

#Remplir ces différents champs obligatoires
modele = "regression"
features = ["Age Range", "Head Size(cm^3)"]
target = ["Brain Weight(grams)"]
data = "headbrain.csv"

#Remplacer par sa pipeline en conservant le nom "pipeline" obligatoire.
pipeline = Pipeline([
    ('features', PCA()),
    ('estimator', LinearRegression())
])

