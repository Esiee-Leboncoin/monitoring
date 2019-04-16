from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

modele = "classification"
features = ["Age Range", "Head Size(cm^3)"]
target = ["Brain Weight(grams)"]
data = "headbrain.csv"

pipeline = Pipeline([
    ('features', StandardScaler()),
    ('estimator', svm.SVC())
])
