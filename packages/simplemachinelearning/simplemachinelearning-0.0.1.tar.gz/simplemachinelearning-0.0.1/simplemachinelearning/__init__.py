from simplemachinelearning.Class_Data_Modeler import DataModeler

import pandas as pd
from scipy.special import boxcox
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
# from xgboost import XGBClassifier
