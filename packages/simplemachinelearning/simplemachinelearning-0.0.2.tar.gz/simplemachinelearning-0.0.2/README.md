# Machine Learning Supervised Learning Project #

## Outline of Project ##
The objective of this project is to load in any data set within a CSV file, expore pre-process and then build a supervised
learning model. Both classification and regression models can be built

## Description of the file structure ##

* The code is all contained in the main directory
* main.py is where the main program is executed and calls methods from the DataModeler class.
* Class_Data_Loader.py contains the class DataLoader that loads in the data from a CSV file and stores it as an object
* Class_Data_Explorer.py contains the class DataExplorer that inherits DataLoader. It's purpose is to print and 
plot various properties of the data so that it can be analysed
* Class_Data_Preprocessor contains the class DataPreprocessor that pre-processes the data
using various methods such as normalising and one-hot encoding
* Class_Data_Modeler contains Data_Modeler which models the data and performs cross
validation
* Data_In contains various data sets and main examples to build a model for the particular data set
* Data_Out contains all various plots that the code produces saved as a pdf file

This was done by using inheritance where DataModeler -> DataPreprocessor -> DataExploror -> DataLoader and the arrow 
 is a symbol indicating 'inherited from'. 

## Packages Required: ##
Environment set up in python 3.5 and runs with following packages:
* numpy        
* pandas       
* matplotlib   
* seaborn
* sklearn
* scipy

## Example of the code ##

Car_Insurance within the Directory Data_In contains a data set to predict whether there will be a sale (Yes/No) of car 
insurance. There are 10 attributes in the data set including: Veh_Mileage, Credit_Score, Licesnse_Length, Veh_Value, 
Price, Age, Marital_Status, Tax, Date. There are 50,000 entries. Car_Insurance_Main_Example.py within Car_Insurance 
contains the example code to explore, pre-process and build a knn and SVM model for that particular data set.

House_Prices within the Directory Data_In contains data to predict house prices from the Kaggle competition: 'House 
Prices: Advanced Regression Techniques' where details of the data set can be found [here.](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) 
The sale price of 1459 houses were predicted using a data set of 1460 houses along with 79 attributes. The model used a 
Lasso model with alpha = 0.01 and box cox transformations for all the attributes where lambda = 0.1 
House_Prices_Main_Example.py within House_Prices contains the example code for this data set.

DfBL within the Directory Data_In contains data involving inspections on a sample of road-going vehicles. It categorises 
the vehicles into three types; heavy goods vehicles, light goods vehicles and personnel; the 10 most common
 manufacturers and finally grades the vehicles on a 100-point scale where 100 is perfect and 0 represents a vehicle in 
 hazardous condition. DfBL_Main_Example within DfBL analysis the DfBL data set contains the attributes: VehicleID, 
 FinancialYear, VehicleType, Manufacturer and ConditionScore for 30305 Vehicles.

Iris within the Directory Data_In contains a data set that predicts weather an Iris flower is either an Iris setosa or 
Iris virginica classified as +1 or -1 respectively. The first four columns are attributes describing sepal length, 
sepal width, petal length, and petal width in cm. There were 100 samples which were split into 70-30 for the train and 
test set respectively. Iris_Main_Example.py within Iris contains the example code to build a model for the data set.

To run these example codes simply copy and paste any Main_Example.py into main.py and run.
## How to run the code ##
Ensure all the packages are installed, set the working directory to Machine-Learning-Project and run main.py. If 
there are any problems please email me at: <nickolastheodoulou@hotmail.com>.

