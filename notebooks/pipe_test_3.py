from sklearn import neighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def get_name():
    return "caribou.py"

pipeline = Pipeline([
    ('features', StandardScaler()),
    ('estimator', neighbors.KNeighborsRegressor())   
])