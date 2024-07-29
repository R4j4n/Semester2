from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# reading countries list
data = pd.read_csv("iris.csv")

# selecting data to plot
x = data.iloc[:, 1:4]

y = data.iloc[:, 4:5]

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

# Print X_test for reference
print(X_test)

# Gaussian Naive Bayes
gnb = GaussianNB()
params_gnb = {"var_smoothing": np.logspace(0, -9, num=100)}
grid_search_gnb = GridSearchCV(
    estimator=gnb, param_grid=params_gnb, cv=5, n_jobs=-1, scoring="accuracy"
)
grid_search_gnb.fit(X_train.values, y_train.values.ravel())

# Best hyperparameters and model
best_gnb = grid_search_gnb.best_estimator_
print(f"Best parameters for GaussianNB: {grid_search_gnb.best_params_}")

# Predictions
y_pred_gnb = best_gnb.predict(X_test.values)
print(
    f"GaussianNB: Number of mislabeled points out of a total {X_test.shape[0]} points: {(y_test.values.ravel() != y_pred_gnb).sum()}"
)
print(best_gnb.predict(np.array([[3.2, 5.9, 2.3]])))

from sklearn import tree


# Decision Tree Classifier
clf = tree.DecisionTreeClassifier()
params_tree = {
    "max_depth": [3, 5, 7, 10, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "criterion": ["gini", "entropy"],
}
grid_search_tree = GridSearchCV(
    estimator=clf, param_grid=params_tree, cv=5, n_jobs=-1, scoring="accuracy"
)
grid_search_tree.fit(X_train.values, y_train.values.ravel())

# Best hyperparameters and model
best_tree = grid_search_tree.best_estimator_
print(f"Best parameters for DecisionTreeClassifier: {grid_search_tree.best_params_}")

# Predictions
y_pred_tree = best_tree.predict(X_test.values)
print(
    f"DecisionTreeClassifier: Number of mislabeled points out of a total {X_test.shape[0]} points: {(y_test.values.ravel() != y_pred_tree).sum()}"
)
print(best_tree.predict(np.array([[3.2, 5.9, 2.3]])))
