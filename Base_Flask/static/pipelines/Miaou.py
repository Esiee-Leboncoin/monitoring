from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

modele = "classification"
features = ["petal_length", "petal_width"]
target = ["species"]
data = "iris.csv"

pipeline = Pipeline([
    ('features', StandardScaler()),
    ('estimator', svm.SVC())
])


