import pandas as pd
# import fancyimpute as fi

from scipy.special import boxcox

from simplemachinelearning.Class_Data_Explorer import DataExplorer


class DataPreprocessor(DataExplorer):
    def __init__(self, train_data_set, test_data_set):
        super().__init__(train_data_set, test_data_set)

    # Deleting outliers lower and to the right of the trend
    def drop_outliers_target_less_y_attribute_greater_x(self, target, y, attribute, x):
        self._train_data_set = self._train_data_set.drop(self._train_data_set[(self._train_data_set[attribute] > x) &
                                                         (self._train_data_set[target] < y)].index)

    # Deleting outliers lower and to the right of the trend
    def drop_outliers_target_less_y_attribute_less_x(self, target, y, attribute, x):
        self._train_data_set = self._train_data_set.drop(self._train_data_set[(self._train_data_set[attribute] < x) &
                                                         (self._train_data_set[target] < y)].index)

    # Deleting outliers lower and to the right of the trend
    def drop_outliers_target_greater_y_attribute_greater_x(self, target, y, attribute, x):
        self._train_data_set = self._train_data_set.drop(self._train_data_set[(self._train_data_set[attribute] > x) &
                                                                              (self._train_data_set[target] > y)].index)

    # Deleting outliers lower and to the right of the trend
    def drop_outliers_target_greater_y_attribute_less_x(self, target, y, attribute, x):
        self._train_data_set = self._train_data_set.drop(self._train_data_set[(self._train_data_set[attribute] < x) &
                                                                              (self._train_data_set[target] > y)].index)

    #  method that drops all the rows with missing data. This is not recommended to be used at all but is used to
    #  test how accurate a simple KNN algorithm is
    def drop_all_na(self):
        self._train_data_set = self._train_data_set.dropna()

        if not self._test_data_set.empty:
            self._test_data_set = self._test_data_set.dropna()
        else:
            print("no test data set")

    def drop_attribute(self, attribute):
        self._train_data_set = self._train_data_set.drop(columns=[attribute])

        if not self._test_data_set.empty:
            self._test_data_set = self._test_data_set.drop(columns=[attribute])
        else:
            print("no test data set")

    def box_cox_trans_attribute(self, attribute, lamda):  # boxcox transformation of an attribute in train_x
        self._train_data_set[attribute] = boxcox(self._train_data_set[attribute], lamda)

        if not self._test_data_set.empty:
            self._test_data_set[attribute] = boxcox(self._test_data_set[attribute], lamda)
        else:
            print("no test data set")

    def box_cox_target(self, lamda):
        self._y_train = boxcox(self._y_train, lamda)

    def normalise_attribute(self, attribute):  # normalises all column of an attribute
        mean = self._train_data_set[attribute].mean()
        std = self._train_data_set[attribute].std()

        self._train_data_set[attribute] = (self._train_data_set[attribute] - mean) / std

        if not self._test_data_set.empty:
            self._test_data_set[attribute] = (self._test_data_set[attribute] - mean) / std
        else:
            print("no test data set")

    #  method that one hot encodes a column
    def one_hot_encode_attribute(self, attribute):
        #  define the data set as the original data set combined with the one hot encoded column of the inputted
        # attribute

        # concat adds the new columns to the data set
        # prefix adds the string attribute to the column head
        self._train_data_set = pd.concat([self._train_data_set, pd.get_dummies(self._train_data_set[attribute],
                                                                               prefix=attribute)], axis=1, sort=False)
        #  drops the column that has the sting value of the attribute to be one hot encoded
        self._train_data_set = self._train_data_set.drop(columns=[attribute])

        if not self._test_data_set.empty:
            self._test_data_set = pd.concat(
                [self._test_data_set, pd.get_dummies(self._test_data_set[attribute], prefix=attribute)],
                axis=1, sort=False)
            self._test_data_set = self._test_data_set.drop(columns=[attribute])
        else:
            print("no test data set")

    #  if a value within an attribute is only in test or train after one hot encoding, delete it
    def delete_unnecessary_one_hot_encoded_columns(self):
        #  list of the missing columns in train after one hot encoding
        missing_cols_in_train = set(self._test_data_set.columns) - set(self._train_data_set.columns)
        for x in missing_cols_in_train:
            #  deletes the missing columns
            self._test_data_set = self._test_data_set.drop(columns=[x])
        #  print the name of the columns that werre deleted
        print('The missing columns in train are:', missing_cols_in_train)

        missing_cols_in_test = set(self._train_data_set.columns) - set(self._test_data_set.columns)
        for x in missing_cols_in_test:
            self._train_data_set = self._train_data_set.drop(columns=[x])
        print('The missing columns in test are: ', missing_cols_in_test)

    def impute_mode(self, attribute):
        self._train_data_set[attribute] = self._train_data_set[attribute].fillna(
            self._train_data_set[attribute].mode()[0])

        if not self._test_data_set.empty:
            self._test_data_set[attribute] = self._train_data_set[attribute].fillna(
                self._test_data_set[attribute].mode()[0])
        else:
            print("no test data set")

    def impute_median(self, attribute):
        self._train_data_set[attribute] = self._train_data_set[attribute].fillna(
            self._train_data_set[attribute].median())

        if not self._test_data_set.empty:
            self._test_data_set[attribute] = self._train_data_set[attribute].fillna(
                self._test_data_set[attribute].median())
        else:
            print("no test data set")

    def impute_mean(self, attribute):
        self._train_data_set[attribute] = self._train_data_set[attribute].fillna(self._train_data_set[attribute].mean())

        if not self._test_data_set.empty:
            self._test_data_set[attribute] = self._test_data_set[attribute].fillna(
                self._train_data_set[attribute].mean())
        else:
            print("no test data set")

    def impute_none(self, attribute):
        self._train_data_set[attribute] = self._train_data_set[attribute].fillna("None")

        if not self._test_data_set.empty:
            self._test_data_set[attribute] = self._test_data_set[attribute].fillna("None")
        else:
            print("no test data set")

    #  can also apply this to the test data set without any data leakage!
    def impute_zero(self, attribute):  # fill na with 0
        self._train_data_set[attribute] = self._train_data_set[attribute].fillna(0)

        if not self._test_data_set.empty:
            self._test_data_set[attribute] = self._test_data_set[attribute].fillna(0)
        else:
            print("no test data set")

    def switch_na_to_median_other_attribute(self, attribute, second_discrete_attribute):
        # fill in the missing value by grouping by second_discrete_attribute and findin the mean of each group and
        # assigning the missing value to this)
        self._train_data_set[attribute] = self._train_data_set[attribute].fillna(self._train_data_set.groupby(
            second_discrete_attribute)[attribute].mean()[0])

        if not self._test_data_set.empty:
            #  apply to test_X by using the median of train_X to prevent data leakage
            self._test_data_set[attribute] = self._test_data_set[attribute].fillna(
                self._train_data_set.groupby(second_discrete_attribute)[attribute].mean()[0])
        else:
            print("no test data set")

    def convert_attribute_to_categorical(self, attribute):
        self._train_data_set[attribute] = self._train_data_set[attribute].astype(str)
        if not self._test_data_set.empty:
            self._test_data_set[attribute] = self._test_data_set[attribute].astype(str)
        else:
            print("no test data set")

    # imputes the missing attributes using KNN from fancy impute using the 3 closes complete columns
    # found to be extremely ineffienct hence not used in final model
    '''
    def impute_knn(self, number_of_nearest_neighbours):
        knn_impute = fi.KNN(k=number_of_nearest_neighbours).complete(self._data_set)
        self._data_set = pd.DataFrame(knn_impute, columns=self._data_set.columns.copy())
    '''