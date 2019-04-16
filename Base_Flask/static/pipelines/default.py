<<<<<<< HEAD
#Ajouter tous les imports necessaires
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler
from sklearn import neighbors



#Importer sa pipeline sans modifier le nom

pipeline = Pipeline([
    ('features', StandardScaler()),
	('estimator', neighbors.KNeighborsRegressor())
])
=======
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

modele = "classification"
features = ["Age Range", "Head Size(cm^3)"]
target = ["Brain Weight(grams)"]

pipeline = Pipeline([
    ('features', StandardScaler()),
    ('estimator', svm.SVC())
])
>>>>>>> 8089226399cb139b8d917430ab4b3d8632d32305
