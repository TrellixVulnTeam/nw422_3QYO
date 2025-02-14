# Evaluate Regression Methods (Python)
# using data from the Studenmund's Restaurants case
# as described in "Marketing Data Science: Modeling Techniques
# for Predictive Analytics with R and Python" (Miller 2015)

# The original source shows how the data from the case
# might be analyzed using a simple linear model. 
# R and Python programs for analyzing the case study data 
# are provided in MDS_13_1.R and MDS_Extra_13_2.py, respectively.
# Data are in the comma-delimited text file studenmunds_restaurants.csv
# Under Python statsmodels we set up the model as follows:
# my_model = str('sales ~ competition + population + income')
# Code from this and other books by Miller is available at the
# GitHub site: https://github.com/mtpa/

# Here we use data from Studenmund's restaurants to evaluate
# regression modeling methods within a cross-validation design.
# We run the evaluation using a polynomial regression model 
# with each variable entered into the linear predictor in its
# raw and squared form. By using a polynomial form, we are 
# able to show possibilities for regularized regression.

# program revised by Thomas W. Milller (2017/09/29)

# Scikit Learn documentation for this assignment:
# http://scikit-learn.org/stable/modules/model_evaluation.html 
# http://scikit-learn.org/stable/modules/generated/
#   sklearn.model_selection.KFold.html
# http://scikit-learn.org/stable/modules/generated/
#   sklearn.linear_model.LinearRegression.html
# http://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html
# http://scikit-learn.org/stable/modules/generated/
#   sklearn.linear_model.Ridge.html
# http://scikit-learn.org/stable/modules/generated/
#   sklearn.linear_model.Lasso.html
# http://scikit-learn.org/stable/modules/generated/
#   sklearn.linear_model.ElasticNet.html
# http://scikit-learn.org/stable/modules/generated/
#   sklearn.metrics.r2_score.html

# Textbook reference materials:
# Geron, A. 2017. Hands-On Machine Learning with Scikit-Learn
# and TensorFlow. Sebastopal, Calif.: O'Reilly. Chapter 3 Training Models
# has sections covering linear regression, polynomial regression,
# and regularized linear models. Sample code from the book is 
# available on GitHub at https://github.com/ageron/handson-ml

# prepare for Python version 3x features and functions
# comment out for Python 3.x execution
# from __future__ import division, print_function
# from future_builtins import ascii, filter, hex, map, oct, zip

# seed value for random number generators to obtain reproducible results
RANDOM_SEED = 1

# although we standardize X and y variables on input,
# we will fit the intercept term in the models
# Expect fitted values to be close to zero
SET_FIT_INTERCEPT = True

# import base packages into the namespace for this program
import numpy as np
import pandas as pd

# modeling routines from Scikit Learn packages
import sklearn.linear_model 
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error, r2_score  
from math import sqrt  # for root mean-squared error calculation

# ---------------------------------------------------------
# read data for Studenmund's Restaurants
# creating data frame restdata
restdata = pd.read_csv('studenmunds_restaurants.csv')

# check the pandas DataFrame object restdata
print('\nrestdata DataFrame (first and last five rows):')
print(restdata.head())
print(restdata.tail())

print('\nGeneral description of the restdata DataFrame:')
print(restdata.info())

# ensure that floats are used for the DataFrame
restdata.competition = pd.to_numeric(restdata.competition, downcast='float')
restdata.population = pd.to_numeric(restdata.population, downcast='float')
restdata.income = pd.to_numeric(restdata.income, downcast='float')
restdata.sales = pd.to_numeric(restdata.sales, downcast='float')

print('\nGeneral description of the restdata DataFrame:')
print(restdata.info())

print('\nDescriptive statistics of the restdata DataFrame:')
print(restdata.describe())

# add quadratic terms to the DataFrame, 
#     setting the stage for polynomial regression
# think of a model such as: sales ~ competition + population + income + 
#                                   competition2 + population2 + income2
# where 2s indicate the squared (quadratic) terms

# numpy functions to define new columns with quadratic terms
restdata['competition2'] = \
    np.multiply(restdata['competition'], restdata['competition'])
restdata['population2'] = \
    np.multiply(restdata['population'], restdata['population'])
restdata['income2'] = np.multiply(restdata['income'], restdata['income'])

# check the expanded pandas DataFrame object restdata
print('\nsoaps DataFrame (first and last five rows):')
print(restdata.head())
print(restdata.tail())

print('\nGeneral description of the restdata DataFrame:')
print(restdata.info())

print('\nDescriptive statistics of the restdata DataFrame:')
print(restdata.describe())

# set up preliminary data for data for fitting the models 
# the first column is sales response
# the remaining columns are the explanatory variables
# and functions of explanatory variables
prelim_model_data = np.array([restdata.sales,\
    restdata.competition,\
    restdata.population,\
    restdata.income,\
    restdata.competition2,\
    restdata.population2,\
    restdata.income2]).T

# dimensions of the polynomial model X input and y response
# preliminary data before standardization
print('\nData dimensions:', prelim_model_data.shape)

# standard scores for the columns... along axis 0
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
print(scaler.fit(prelim_model_data))
# show standardization constants being employed
print(scaler.mean_)
print(scaler.scale_)

# the model data will be standardized form of preliminary model data
model_data = scaler.fit_transform(prelim_model_data)

# dimensions of the polynomial model X input and y response
# all in standardized units of measure
print('\nDimensions for model_data:', model_data.shape)

# --------------------------------------------------------
# specify the set of regression models being evaluated
# we set normalize=False because we have standardized
# the model input data outside of the modeling method calls
names = ['Linear_Regression', 'Ridge_Regression']

regressors = [LinearRegression(fit_intercept = SET_FIT_INTERCEPT, 
              normalize = False), 
              Ridge(alpha = 1, solver = 'cholesky', 
                    fit_intercept = SET_FIT_INTERCEPT, 
                    normalize = False, 
                    random_state = RANDOM_SEED)]
             
# tried adding Lasso and ElasticNet with little success
# these methods may have failed due to the small sample size 
# for the Studenmund's Restaurants case
# names = ['Linear_Regression', 'Ridge_Regression', 'Lasso_Regression', 
#          'ElasticNet_Regression'] 

# regressors = [LinearRegression(fit_intercept = SET_FIT_INTERCEPT), 
#               Ridge(alpha = 1, solver = 'cholesky', 
#                     fit_intercept = SET_FIT_INTERCEPT, 
#                     normalize = False, 
#                     random_state = RANDOM_SEED),
#               Lasso(alpha = 0.1, max_iter=10000, tol=0.01, 
#                     fit_intercept = SET_FIT_INTERCEPT, 
#                     random_state = RANDOM_SEED),
#               ElasticNet(alpha = 0.1, l1_ratio = 0.5, 
#                          max_iter=10000, tol=0.01, 
#                          fit_intercept = SET_FIT_INTERCEPT, 
#                          normalize = False, 
#                          random_state = RANDOM_SEED)]

# --------------------------------------------------------
# specify the k-fold cross-validation design
from sklearn.model_selection import KFold

# ten-fold cross-validation employed here
# As an alternative to 10-fold cross-validation, restdata with its 
# small sample size could be analyzed would be a good candidate
# for  leave-one-out cross-validation, which would set the number
# of folds to the number of observations in the data set.
N_FOLDS = 10

# set up numpy array for storing results
cv_results = np.zeros((N_FOLDS, len(names)))

kf = KFold(n_splits = N_FOLDS, shuffle=False, random_state = RANDOM_SEED)
# check the splitting process by looking at fold observation counts
index_for_fold = 0  # fold count initialized 
for train_index, test_index in kf.split(model_data):
    print('\nFold index:', index_for_fold,
          '------------------------------------------')
#   the structure of modeling data for this study has the
#   response variable coming first and explanatory variables later          
#   so 1:model_data.shape[1] slices for explanatory variables
#   and 0 is the index for the response variable    
    X_train = model_data[train_index, 1:model_data.shape[1]]
    X_test = model_data[test_index, 1:model_data.shape[1]]
    y_train = model_data[train_index, 0]
    y_test = model_data[test_index, 0]   
    print('\nShape of input data for this fold:',
          '\nData Set: (Observations, Variables)')
    print('X_train:', X_train.shape)
    print('X_test:',X_test.shape)
    print('y_train:', y_train.shape)
    print('y_test:',y_test.shape)

    index_for_method = 0  # initialize
    for name, reg_model in zip(names, regressors):
        print('\nRegression model evaluation for:', name)
        print('  Scikit Learn method:', reg_model)
        reg_model.fit(X_train, y_train)  # fit on the train set for this fold
        print('Fitted regression intercept:', reg_model.intercept_)
        print('Fitted regression coefficients:', reg_model.coef_)
 
        # evaluate on the test set for this fold
        y_test_predict = reg_model.predict(X_test)
        print('Coefficient of determination (R-squared):',
              r2_score(y_test, y_test_predict))
        fold_method_result = sqrt(mean_squared_error(y_test, y_test_predict))
        print(reg_model.get_params(deep=True))
        print('Root mean-squared error:', fold_method_result)
        cv_results[index_for_fold, index_for_method] = fold_method_result
        index_for_method += 1
  
    index_for_fold += 1

cv_results_df = pd.DataFrame(cv_results)
cv_results_df.columns = names

print('\n----------------------------------------------')
print('Average results from ', N_FOLDS, '-fold cross-validation\n',
      'in standardized units (mean 0, standard deviation 1)\n',
      '\nMethod               Root mean-squared error', sep = '')     
print(cv_results_df.mean())   







