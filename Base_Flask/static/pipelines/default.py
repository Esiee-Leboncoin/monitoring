from sklearn.pipeline import Pipeline

#Ajouter tous les imports necessaires
from sklearn.preprocessing import StandardScaler
from sklearn import neighbors

#Importer sa pipeline sans modifier le nom
pipeline = Pipeline([
    ('features', StandardScaler()),
    ('estimator', neighbors.KNeighborsRegressor())
])
