## Data pipeline

Web scraping documentation can be found in scraping/Readme.md.

The processing directory contains scripts for turning raw data into files for use in analysis and modeling. Please see the Readme in 
this directory for more information.

## iPython Notebooks

The following notebooks are included:

* Model to Predict Player Salaries.ipynb: Shows the development of a series of models, including regression and classification. Includes
some feature engineering for player salaries and to clean/normalize input variables. Depends on Observations.csv (the creation of this file is documented in 
processing/Readme.md). The cleaned and normalized observations are written out to ModelInput.csv.

* Regression with statsmodels.ipynb: This uses the statsmodels package to create regression models for team wins and player salaries. Shown
in the notebook are the final models, after iteratively testing different subsets of predictor variables. Variables with low statistical
significance were eliminated. Depends on ModelInput.csv.

* Explore Observations.ipynb - Various analysis of the inputs to the model. Correlations and plots of variables vs. adjusted salaries.

* Explore Salaries.ipynb - Analysis of player salaries

* Predict Team Wins: Use scikit-learn to create regression model on all team-level statistics.

* LogLinearRegression Model.ipynb: This notebook contains some experimental code for my own implementation of a log(y) regression. The purpose
was to validate the predictions returned by scikit-learn's LinearRegression on log(y). LogLinearRegression implements predictions which adjust 
for the variance as described here: http://davegiles.blogspot.com/2013/08/forecasting-from-log-linear-regressions.html. The predictions returned by
LogLinearRegression.predict(X) and exp(LinearRegression.predict(X)) were close enough that I decided to disregard the bias in LinearRegression's estimates
of log(y).




