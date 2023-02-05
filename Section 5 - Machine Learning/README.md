## Section 5: Machine Learning

This section will cover building a Machine Learning model to predict the price of Buying Price of a car.

In this section Jupyter Notebook running on Python 3.9 will be used

Documentation of this section will be cover in the Notebook
 
### Summary of tasks:

1. Train models to predict Buying Price (Classification Problem)
	- Ensemble model
		- Random forest model
		- Logistic regression model
		- Decision tree model
		- Naive Bayes model
2. Evaluate the model performance
3. Save trained model for future use
4. Using another notebook load trained model to perform prediction
---
### Summary of results:

#### Trained Model
Ensemble Model was trained with the following models:
1. Random Forest model
2. Logistic regression model
3. Decision tree model
4. Naive Bayes model

The accuracy of the trained model produced low accuracy of around **30%**

#### Explanation

- Upon analyzing the correlation between the label and attributes, it is found that buying price has poor correlation with the other attributes.
- Hence, it is difficult for any model to perform well with accurate prediction
- Upon inspecting the data set information given, it is realized that buying price is an attributes in the dataset instead of a classification value
  - This might explain the poor correlation between buying price and other attributes
---
#### Prediction
Predicting the buying price given the following parameters:
```
Maintenance = High
Number of doors = 4
Lug Boot Size = Big
Safety = High
Class Value = Good 
```
**Prediction = low** 

Answer is contained in **Car Evaluation Buying Price Prediction** notebook

