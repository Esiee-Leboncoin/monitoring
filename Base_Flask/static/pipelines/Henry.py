from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA

modele = "regression"
features = ["Age Range", "Head Size(cm^3)"]
target = ["Brain Weight(grams)"]
data = "headbrain.csv"

pipeline = Pipeline([
    ('features', PCA()),
    ('estimator', LinearRegression())
])
