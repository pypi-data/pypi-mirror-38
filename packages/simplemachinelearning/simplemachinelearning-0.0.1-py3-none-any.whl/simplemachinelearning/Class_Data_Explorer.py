import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from scipy import stats

from simplemachinelearning.Class_Data_Loader import DataLoader


class DataExplorer(DataLoader):
    def __init__(self, train_data_set, test_data_set):
        super().__init__(train_data_set, test_data_set)

    # method that prints the number of different values in a given column
    def attribute_value_count(self, attribute):
        #  first counts the number of different values in each column then sorts it in ascending order
        my_attribute_count = self._train_data_set[attribute].value_counts().sort_index()
        print("The count of the different variables in the attribute: ", attribute, ' is\n', my_attribute_count)

    # method that creates a bar graph to show the distribution of an attribute
    def bar_graph_attribute(self, attribute):
        #  first counts the number of different values in each column then sorts it in ascending order
        column_count = self._train_data_set[attribute].value_counts().sort_index()
        # set the y axis to the values within the series object as a percentage
        y = column_count.values * 100 / column_count.sum()
        x = column_count.index  # set the x axis to the index of the series object
        width_of_bar = 1 / 1.5
        plt.subplots(figsize=(16, 8))  # changes the size of the fig
        plt.bar(x, y, width_of_bar, color="#2b8cbe", edgecolor='black')  # plots the bar graph
        plt.xlabel(column_count.name, fontsize=15)  # sets the xlabel to the name of the series object
        plt.ylabel('Percent', fontsize=15)
        plt.xticks(x, rotation=90)  # rotates ticks by 90deg so larger font can be used
        plt.tick_params(labelsize=12)  # increases font of the ticks
        #  file name defined by attribute user input and type of graph
        plt.title('Bar graph showing the count of ' + str(attribute))
        plt.savefig('Data_Out/' + attribute + '_bar_graph_percentage.pdf', index=False, bbox_inches='tight')
        plt.show()

    def line_graph_percentage_difference(self, attribute):
        #  counts the number of attributes and store
        attribute_list_count = self._train_data_set[attribute].value_counts().sort_index()

        #  define the list of attributes in ascending order
        attribute_list = attribute_list_count.index

        # define empty numpy array to store the y coordinates which will be the percentage difference
        y = np.zeros(attribute_list_count.count() - 1)
        #  define empty list to store the ticks which will be combined from attribute_list of size attribute_list - 1
        my_x_ticks = [0] * (attribute_list_count.count() - 1)

        # for loop to calculate the percentage difference and the value of the x ticks
        for i in range(0, attribute_list_count.count() - 1):
            y[i] = ((attribute_list_count.values[i + 1] - attribute_list_count.values[i]) /
                    attribute_list_count.values[i]) * 100

            my_x_ticks[i] = str(attribute_list.values[i]) + " to " + str(attribute_list.values[i + 1])

        x = attribute_list_count[:-1].index  # drops the final column in the series object and sets x to the index
        plt.grid()
        plt.plot(x, y, c="g", alpha=0.5, marker="s")
        #  plt.title('Bar graph of ' + str(column_count.name) + ' Against ' + str(' Sample Size'), fontsize=20)
        plt.xlabel(attribute, fontsize=12)  # sets the xlabel to the name of the series object
        plt.ylabel('Percentage Change', fontsize=12)
        plt.xticks(x, my_x_ticks, rotation=90)  # rotates ticks by 90deg so larger font can be used
        plt.tick_params(labelsize=12)  # increases font of the ticks

        #  file name defined by attribute user input and type of graph
        plt.savefig('Data_Out/'+attribute + '_line_graph_percentage_difference.pdf', index=False, bbox_inches='tight')
        plt.show()

    # method that prints the number of different values in each column then sorts it in ascending order per
    # classification
    def attribute_value_count_by_classification(self, attribute, target):
        my_attribute_classification_count = pd.crosstab(self._train_data_set[attribute], self._train_data_set[target])
        print("The classification count of the different variables in the attribute: ", attribute, ' is\n',
              my_attribute_classification_count)

    def bar_graph_attribute_by_classification(self, attribute, target):
        plt.subplots(figsize=(16, 8))  # changes the size of the fig
        #  Computes a cross-tabulation of user inputted attribute to plot target true and false count
        my_attribute_true_false_matrix = pd.crosstab(self._train_data_set[attribute], self._train_data_set[target])

        #  counts number of false for inputted attribute
        my_attribute_0_count = my_attribute_true_false_matrix[self._train_data_set[target].unique()[0]].values
        #  counts number of true for inputted attribute
        my_attribute_1_count = my_attribute_true_false_matrix[self._train_data_set[target].unique()[1]].values
        x = my_attribute_true_false_matrix.index  # set the x axis to index of user inputted attribute

        width = 0.5  # the width of the bars
        #  creates the 2 bars, bottom indicates which bar goes below the current bar
        attribute_0_bars = plt.bar(x, my_attribute_0_count, width, edgecolor='black')
        attribute_1_bars = plt.bar(x, my_attribute_1_count, width, bottom=my_attribute_0_count, edgecolor='black', )

        # plt.grid()
        plt.ylabel('Count', fontsize=18)
        plt.xlabel(attribute, fontsize=18)
        plt.yticks(fontsize=18)
        plt.xticks(x, rotation=90, fontsize=18)  # rotates ticks by 30deg so larger font can be used
        #  create the legend

        legend_label_true = target, ': True'
        legend_label_false = target, ': False'

        plt.legend((attribute_0_bars[0], attribute_1_bars[0]), (legend_label_false, legend_label_true))
        plt.title('Bar graph showing the count of ' + str(attribute), fontsize=18)
        plt.savefig('Data_Out/' + attribute + '_bar_graph_attribute_by_classification.pdf', index=False,
                    bbox_inches='tight')
        plt.show()

    # method that prints a summary of the distribution of the data
    def describe_attribute(self, attribute):
        description_of_attribute = self._train_data_set[attribute].describe()
        print("A summary of the distribution for the attribute", attribute, ' is\n', description_of_attribute)

    #  method that prints the percentage of missing data of train and test
    def train_missing_data_ratio_print(self):

        self._train_data_set.replace('?', np.NaN)
        #  define the percentage as the number of missing values in each column/ number of entries * 100
        missing_data_train = ((self._train_data_set.isnull().sum() / (len(self._train_data_set))) * 100)

        #  sorts percent_of_missing_data_in_each_column into descending order to be printed
        missing_data_train = missing_data_train.drop(
            missing_data_train[missing_data_train == 0].index).sort_values(
            ascending=False)[:self._train_data_set.shape[1]]

        #  redefines percent_of_missing_data_in_each_column as a DataFrame with the column head 'Missing Ratio'
        missing_data_train = pd.DataFrame({'Missing Ratio': missing_data_train})
        #  rename the column heading
        missing_data_train = missing_data_train.rename(columns={
            missing_data_train.columns[0]: "Percentage of missing values in train"})
        #  print the data fame
        print(missing_data_train.head(20))

    def test_missing_data_ratio_print(self):

        #  define the percentage as the number of missing values in test
        missing_data_test = ((self._test_data_set.isnull().sum() / (len(self._test_data_set))) * 100)
        #  sorts percent_of_missing_data_in_each_column into descending order to be printed
        missing_data_test = missing_data_test.drop(
            missing_data_test[missing_data_test == 0].index).sort_values(
            ascending=False)[:self._test_data_set.shape[1]]
        #  redefines percent_of_missing_data_in_each_column as a DataFrame with the column head 'Missing Ratio'
        missing_data_test = pd.DataFrame({'Missing Ratio': missing_data_test})
        #  rename the column heading
        missing_data_test = missing_data_test.rename(columns={
            missing_data_test.columns[0]: "Percentage of missing values in test"})
        #  print the data fame
        print(missing_data_test.head(20))

    #  method that p
    def missing_data_ratio_bar_graph(self):
        #  define the percentage as the number of missing values in each column/ number of entries * 100
        percent_of_missing_data_in_each_column = ((self._train_data_set.isnull().sum() /
                                                   (len(self._train_data_set))) * 100)

        #  sorts percent_of_missing_data_in_each_column into descending order to be printed
        percent_of_missing_data_in_each_column = percent_of_missing_data_in_each_column.drop(
            percent_of_missing_data_in_each_column[percent_of_missing_data_in_each_column == 0].index).sort_values(
                ascending=False)[:self._train_data_set.shape[1]]

        plt.xticks(rotation='90', fontsize=14)
        # use seaborn package to plot the bar graph
        sns.barplot(x=percent_of_missing_data_in_each_column.index, y=percent_of_missing_data_in_each_column)
        plt.xlabel('Attribute', fontsize=15)
        plt.ylabel('Percent of missing values', fontsize=15)
        plt.title('Percent missing data by feature', fontsize=15)
        plt.savefig('Data_Out/percentage_of_missing_data.pdf', index=False, bbox_inches='tight')  # save the plot
        plt.show()

    # method that produces a heatmap of the attributes
    def heat_map(self):
        correlation_matrix = self._train_data_set.corr()  # correlation matrix
        plt.subplots(figsize=(12, 9))  # size of fig
        z_text = np.around(correlation_matrix, decimals=1)  # Only show rounded value (full value on hover)
        sns.heatmap(z_text, vmax=.8, square=True, annot=True, fmt='.1f', annot_kws={'size': 7})  # creates the heatmap
        plt.show()

    def box_plot(self, continuous_attribute, categorical_attribute):
        #  sort the dataset into acending order of the attribute to be plotted
        self._train_data_set = self._train_data_set.sort_values([categorical_attribute]).reset_index(drop=True)
        data_in = pd.concat([self._train_data_set[continuous_attribute], self._train_data_set[categorical_attribute]],
                            axis=1)  # defines the data
        plt.subplots(figsize=(16, 8))  # changes the size of the fig

        fig = sns.boxplot(x=categorical_attribute, y=continuous_attribute, data=data_in)
        fig.set_xlabel(categorical_attribute, fontsize=12)
        fig.set_ylabel(continuous_attribute, fontsize=12)
        fig.axis(ymin=0, ymax=self._train_data_set[continuous_attribute].values.max())  # defines the y axis
        plt.xticks(rotation=90)  # rotates the x ticks so that they are easier to read when the strings are longer
        plt.tick_params(labelsize=12)

        #  file name defined by attribute user input and type of graph
        plt.savefig('Data_Out/' + categorical_attribute + '_' + continuous_attribute + '_boxplot.pdf', index=False,
                    bbox_inches='tight')
        plt.show()

    def scatter_plot(self, my_y_attribute, my_x_attribute):
        x = self._train_data_set[my_x_attribute].values
        # defines the sold price so that it can be loaded into the function each time rather than loading the whole
        # train matrix
        y = self._train_data_set[my_y_attribute].values
        plt.subplots(figsize=(16, 8))  # changes the size of the fig
        plt.scatter(x, y, c="g", alpha=0.5, marker="s")  # scatter plot of the sold price and user chosen attribute
        plt.title('Scatter Graph of ' + str(my_y_attribute) + ' against ' + str(my_x_attribute))
        plt.xlabel(my_x_attribute)
        plt.ylabel(my_y_attribute)
        # save the plot
        plt.savefig('Data_Out/'+my_y_attribute+'_'+my_x_attribute+'scatter_plot.pdf', index=False, bbox_inches='tight')
        plt.show()

    def scatter_plot_by_classification(self, my_y_attribute, my_x_attribute, target):
        #  create empty list to store colour with target true being blue and target false being red
        list_colour_corresponding_to_target = ['Null'] * len(self._train_data_set)

        for i in range(0, len(self._train_data_set)):

            # if a value in the target is false then set the colour to red
            if self._train_data_set[target].values[i] == 0:
                list_colour_corresponding_to_target[i] = "r"

            # if a value in the target is true then set the colour to blue
            elif self._train_data_set[target].values[i] == 1:
                list_colour_corresponding_to_target[i] = "b"
            else:
                print("Error")
                break

        plt.scatter(self._train_data_set[my_x_attribute].values, self._train_data_set[my_y_attribute].values,
                    color=list_colour_corresponding_to_target)

        plt.xlabel(my_x_attribute)
        plt.ylabel(my_y_attribute)

        #  create the legend

        legend_label_true = target, ': True'
        legend_label_false = target, ': False'

        # plot empty lists with the desired size and label to create the legend (not possible any other way)
        plt.scatter([], [], c=['r'], alpha=1, label=legend_label_false)
        plt.scatter([], [], c=['b'], alpha=1, label=legend_label_true)
        plt.title('Scatter Graph of ' + str(my_y_attribute) + ' against ' + str(my_x_attribute))

        plt.legend(loc=0, scatterpoints=1, frameon=False, labelspacing=0, prop={'size': 9})
        plt.savefig('Data_Out/' + my_y_attribute + '_' + my_x_attribute + 'scatter_plot_by_classification.pdf',
                    index=False, bbox_inches='tight')
        plt.show()

    def histogram_and_q_q(self, attribute):
        # define a new data set with the attributes missing dropped so that the NaN values are ignored
        my_data_set = self._train_data_set.dropna()

        x_sigma = my_data_set[attribute].values.std()  # standard deviation
        x_max = my_data_set[attribute].values.max()  # max value
        x_min = my_data_set[attribute].values.min()  # min value
        n = my_data_set[attribute].shape[0]  # number of data points

        # formula to give the number of bins for any dataset
        number_bins = (x_max - x_min) * n ** (1 / 3) / (3.49 * x_sigma)
        number_bins = int(number_bins)  # floors the double to int
        # values being plotted into the histogram
        attribute_being_plotted = my_data_set[attribute].values

        # defined y to find y max to place the text
        # plt.subplots(figsize=(16, 8))  # changes the size of the fig
        y, i, _ = plt.hist(attribute_being_plotted, density=True, bins=number_bins, facecolor='paleturquoise',
                           alpha=0.75, edgecolor='black', linewidth=1.2,
                           label='Histogram: (Skewness: ' + "{0:.3f}".format(my_data_set[attribute].skew()) +
                                 ' and Kurtosis: ' + "{0:.3f}".format(my_data_set[attribute].kurt()) + ')')

        x = np.linspace(x_min, x_max, len(attribute_being_plotted))

        # Get the fitted parameters used by the function for the normal distribution
        (mu, sigma) = stats.norm.fit(my_data_set[attribute])
        normal_distribution = stats.norm.pdf(x, mu, sigma)  # define the norml distribution in terms of x, mu and sigma
        plt.plot(x, normal_distribution, 'k', linewidth=2,
                 label='Normal distribution: ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma))

        plt.legend(loc='best')  # adds the legend
        plt.ylabel('Probability')
        plt.xlabel(attribute)
        plt.title('Histogram of ' + str(attribute))
        plt.show()

        stats.probplot(my_data_set[attribute], plot=plt)  # Q-Q plot
        plt.title('Quantile-Quantile plot of ' + str(attribute))
        plt.show()

#  function that plots a triple stacked bar graph of attribute as the x coordinate and sub-attribute as the
    # attribute to be stacked within the bar (Needs to be generalised!
    def triple_stacked_bar_graph(self, attribute, sub_attribute):
        #  Computes a cross-tabulation of two user inputted attributes
        attribute_and_sub_attribute_matrix = pd.crosstab(self._train_data_set[attribute], self._train_data_set[
            sub_attribute])

        #  defines the y values of the three sub attributes as the three columns in column_count matrix
        sub_attribute_one_count = attribute_and_sub_attribute_matrix[
            self._train_data_set[sub_attribute].unique()[0]].values
        sub_attribute_two_count = attribute_and_sub_attribute_matrix[
            self._train_data_set[sub_attribute].unique()[1]].values
        sub_attribute_three_count = attribute_and_sub_attribute_matrix[
            self._train_data_set[sub_attribute].unique()[2]].values

        x = attribute_and_sub_attribute_matrix.index  # set the x axis to the year which is the intex of
        #  attribute_and_sub_attribute_matrix

        width = 0.35  # the width of the bars

        #  creates the 3 bars, bottom indicates which bar goes below the current bar
        sub_attribute_one_bar = plt.bar(x, sub_attribute_one_count, width)
        sub_attribute_two_bar = plt.bar(x, sub_attribute_two_count, width, bottom=sub_attribute_one_count, )
        sub_attribute_three_bar = plt.bar(x, sub_attribute_three_count, width, bottom=sub_attribute_two_count +
                                                                                      sub_attribute_one_count, )

        plt.grid()
        plt.ylabel('Number Of Samples', fontsize=14)
        plt.xlabel(attribute, fontsize=14)
        plt.xticks(x, rotation=30)  # rotates ticks by 30deg so larger font can be used
        #  create the legend of each bar by the corresponding sub_attribute which is the ith unique value in the
        #  column VehicleType within self._data_set
        plt.legend((sub_attribute_one_bar[0], sub_attribute_two_bar[0], sub_attribute_three_bar[0]),
                   (self._train_data_set.VehicleType.unique()[0], self._train_data_set.VehicleType.unique()[1],
                    self._train_data_set.VehicleType.unique()[2]))

        plt.savefig('Data_Out/' + attribute + '_triple_stacked_bar_graph.pdf', index=False, bbox_inches='tight')
        plt.show()
