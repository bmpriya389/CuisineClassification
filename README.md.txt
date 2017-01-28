Cuisine Classification 
A project, in the works, to classify a set of ingredients in a recipe to a cuisine based on a Multinomial Naives Bayes prediction model built from a training dataset consisting of recipes with the cuisines they belong to cuisines and their corresponding ingredients.

Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes

Prerequisites
1.	Mongodb v3.4.1
2.	Python v2.7.12
3.	Flask 0.12
4.	Angular 1.5.6
5.	D3

Intructions:
Download or clone this repository.
Install Mongodb and create a database ‘cuisine’ using the following command:
use <database_name>
Import the collections(.json files) in the database folder into the database using the following commands:
mongoimport --db cuisine --collection ingred_info --file ingred_info.json 
mongoimport --db cuisine --collection cuisine_info --file cuisine_info.json
mongoimport --db cuisine --collection training_set_info --file training_set.json
Install the numpy, json, collections, pymongo, operator and flask  libraries in python using pip.
Run the flask server in a terminal by navigating to the project folder and running the following commands:
export FLASK_APP=app.py
flask run
Access the application at localhost:5000.

Authors
	•	Priya Balachandran Mary

Sources
information: https://www.kaggle.com/c/whats-cooking
dataset: https://www.kaggle.com/c/whats-cooking/data