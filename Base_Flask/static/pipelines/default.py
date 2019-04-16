#Ajouter tous les imports necessaires
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler
from sklearn import neighbors



#Importer sa pipeline sans modifier le nom

pipeline = Pipeline([
    ('features', StandardScaler()),
	('estimator', neighbors.KNeighborsRegressor())
])
