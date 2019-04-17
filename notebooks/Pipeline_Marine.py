from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

modele = "classification"
features = ["contains_cdi", "contains_cdd", "contains_stage", "contains_vie",
           "contains_alternance", "contains_apprenti", "department_id", "industry_id",
           "latitude", "longitude"]
target = ["contract_id"]
data = "X.csv"

pipeline = Pipeline([
    ('features', StandardScaler()),
    ('estimator', svm.SVC())
])

