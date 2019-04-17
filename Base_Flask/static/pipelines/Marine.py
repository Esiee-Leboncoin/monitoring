from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

modele = "classification"
features = ["contains_cdi", "contains_cdd", "contains_stage",
           "contains_alternance", "contains_apprenti", "industry_id",
           "department_id", "latitude", "longitude"]
target = ["contract_id"]
data = "X.csv"

pipeline = Pipeline([
    ('features', StandardScaler()),
    ('estimator', svm.SVC())
])

