from simplemachinelearning.Class_Data_Preprocessor import DataPreprocessor

import pandas as pd

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso


class DataModeler(DataPreprocessor):
    def __init__(self, train_data_set, test_data_set):
        super().__init__(train_data_set, test_data_set)

    def classification_model(self, model, parameters, number_of_folds):
        my_model = model(**parameters)  # unpack the dictionary and pass it in as the argument for the model
        x_train = self._train_data_set
        y_train = self._y_train.values.ravel()
        x_test = self._test_data_set
        y_test = self._y_test.values.ravel()

        my_model.fit(x_train, y_train)  # fit the knn classifier to the data

        # define the predicted value of y and true value of y to create a prediction matrix
        y_pred = my_model.predict(x_test)

        # print percent of correct predictions
        print('For', model, 'with', parameters, ' the percentage accuracy is', my_model.score(x_test, y_test))
        print(my_model.score(x_train, y_train))
        # print confusion matrix
        print('The confusion matrix for', model, 'with', parameters, 'is: \n', pd.crosstab(y_test, y_pred,
                                                                                           rownames=['True'],
                                                                                           colnames=['Predicted'],
                                                                                           margins=True))

        # Applying K-Fold cross validation

        # can add n_jobs =-1 to set all CPU's to work
        percent_accuracies = cross_val_score(estimator=my_model, X=x_train, y=y_train, cv=number_of_folds) * 100

        print('For', model, 'with', parameters, ' the percentage accuracy of each ', number_of_folds, '-fold is:',
              percent_accuracies)

    # Create a function called lasso
    # Takes in a list of alphas. Outputs a dataframe containing the coefficients of lasso regressions from each alpha.
    def lasso_compare_alpha(self, alphas):
        df = pd.DataFrame()  # Create an empty data frame
        df['Feature Name'] = self._train_data_set.columns  # Create a column of feature names
        for alpha in alphas:  # For each alpha value in the list of alpha values,
            #  Robustscaler() makes the lasso more robust on outliers
            # Create a lasso regression with that alpha value,
            lasso = make_pipeline(RobustScaler(), Lasso(alpha=alpha, random_state=1))
            lasso.fit(self._train_data_set, self._y_train)  # Fit the lasso regression
            column_name = 'Alpha = %f' % alpha  # Create a column name for that alpha value
            df[column_name] = lasso.steps[1][1].coef_  # Create a column of coefficient values
        return df  # Return the data frame

    def regression_model_submission(self, model, target, tuned_parameters):
        x_train = self._train_data_set
        y_train = self._y_train
        x_test = self._test_data_set

        optimised_model = make_pipeline(RobustScaler(), model(**tuned_parameters))

        my_model = optimised_model
        my_model.fit(x_train, y_train)

        y_pred = my_model.predict(x_test)  # Make predictions using the testing set
        y_pred = pd.DataFrame(data=y_pred, columns={target})
        y_pred = pd.concat([self._test_y_id, y_pred], axis=1)
        y_pred.to_csv('Data_Out/linear_model_optimised.csv', index=False)  # export predictions as csv

        # print cross validation scores
        scores = cross_validate(my_model, self._train_data_set, self._y_train, cv=10,
                                scoring=('explained_variance', 'neg_mean_absolute_error', 'r2',
                                         'neg_mean_squared_error'))

        # print the scores for test
        print('For', model, 'the mean of the explained_variance scores is: ', scores['test_explained_variance'].mean(),
              'with standard deviation ', scores['test_explained_variance'].std())

        print('For', model, 'the mean of the neg_mean_absolute_error scores is: ',
              scores['test_neg_mean_absolute_error'].mean(), 'with standard deviation ',
              scores['test_neg_mean_absolute_error'].std())

        print('For', model, 'the mean of the neg_mean_squared_error scores is: ',
              scores['test_neg_mean_squared_error'].mean(), 'with standard deviation ',
              scores['test_neg_mean_squared_error'].std())

        print('For', model, 'mean of the R^2 scores is: ', scores['test_r2'].mean(), 'with standard deviation ',
              scores['test_r2'].std())

    def regression_model_grid_search(self, model, model_parameters, n_folds):
        x = self._train_data_set
        y = self._y_train

        my_model = GridSearchCV(estimator=model(), param_grid=model_parameters, cv=n_folds)
        my_model.fit(x, y)

        #  Mean cross-validated score of the best_estimator
        print('For', model, ' the best score is best score:', my_model.best_score_)
        print(model, 'best parameters:', my_model.best_params_)

    def classification_model_grid_search(self, model, grid_parameters, number_of_folds):

        # calls the function to perform the grid search for user inputted parameters
        my_model = GridSearchCV(model(), grid_parameters, cv=number_of_folds,
                                scoring='f1_macro', n_jobs=-1)

        # fits the knn models to sample data
        my_model.fit(self._train_data_set, self._y_train)

        y_true, y_pred = self._y_test, my_model.predict(self._test_data_set)
        print(classification_report(y_true, y_pred))  # prints a summary of the grid search

        print('The best parameters for the model is', my_model.best_params_)  # prints the best parameters found

        print('The results are:', my_model.cv_results_)  # prints all the results

        # prints the scoring for each model in the grid
        for param, score in zip(my_model.cv_results_['params'], my_model.cv_results_['mean_test_score']):
            print(param, score)
