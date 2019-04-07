from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler
from sklearn import neighbors

name_pipeline = Pipeline([
    ('features', StandardScaler()),
    ('estimator', neighbors.KNeighborsRegressor())
])
