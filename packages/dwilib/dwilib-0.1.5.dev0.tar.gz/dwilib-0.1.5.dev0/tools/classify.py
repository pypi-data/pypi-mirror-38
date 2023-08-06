#!/usr/bin/python3

"""Classify."""

from sklearn import svm
from sklearn import datasets

clf = svm.SVC()
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf.fit(X, y)
print(clf)

result = clf.predict(X)
print(y)
print(result)
