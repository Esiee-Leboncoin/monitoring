from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.preprocessing import StandardScaler

modele = "classification"
features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
target = ["species"]
data = "iris.csv"

pipeline = Pipeline([
    ('features', StandardScaler()),
    ('estimator', svm.SVC())  
])