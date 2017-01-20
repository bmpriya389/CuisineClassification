from __future__ import division, print_function
import pandas
import numpy
import json
from collections import Counter
import pymongo
from sklearn.naive_bayes import MultinomialNB

def create_dataset():

    # load training set
    train = json.load(open('test2.json'))

    # create dictionaries for ingredients, no of recorded recipes per type of cuisine & ingredient count
    total_recipes = len(train)

    training_dataset = [{"id":i["id"], "cuisine": i["cuisine"], "ingredients": dict(Counter(i["ingredients"]))} for i in train]
    cuisines = set([k["cuisine"] for k in train])
    cuisine_ingredient = dict.fromkeys(cuisines, [])
    cuisine_count = dict.fromkeys(cuisines, 0)

    for i in train:
        if not cuisine_ingredient[i['cuisine']]:
            cuisine_ingredient[i['cuisine']] = i['ingredients']
        else:
            cuisine_ingredient[i['cuisine']].extend(i['ingredients'])
        cuisine_count[i['cuisine']] += 1

    cuisine_ingredient_count = {i: Counter(cuisine_ingredient[i]) for i in cuisine_ingredient}

    # Combine metioned dictionaries to form a data frame with rows as cuisines and columns as no of recipes recorded,
    # ingredients, no of time an ingredient has featured in a cuisine

    train_cuisine = pandas.DataFrame(
        {'noOfRecipes': cuisine_count, 'Ingredients': cuisine_ingredient, 'IngredientsCount': cuisine_ingredient_count})

    ingredients_global = [i for _ in train_cuisine['Ingredients'] for i in _]
    ingredients_global_count = dict(Counter(ingredients_global))
    ingredients_global_total = len(ingredients_global)
    ingredients_global = set(ingredients_global)
    ingredients_cuisine = dict.fromkeys(ingredients_global, {})


    for i in ingredients_global:
        ingredients_cuisine[i] = {j: train_cuisine.loc[j, "IngredientsCount"][i] for j in list(train_cuisine.index) if
                                  i in train_cuisine.loc[j, "IngredientsCount"].keys()}

    for i in ingredients_global_count:
        ingredients_cuisine[i]['globalCount'] = ingredients_global_count[i]
        ingredients_cuisine[i]['ingredient'] = i

    # creating a collection for ingredient stats
    try:
        db.create_collection('ingredStats')
        db.create_collection('cuisine')
        db.create_collection('recipes')
        db.create_collection('training_dataset')

        map(lambda x: db.get_collection('ingredStats').insert_one(ingredients_cuisine[x]), ingredients_cuisine)
        map(lambda y: db.get_collection('cuisine').insert_one({'cuisine': y, 'count': train_cuisine['noOfRecipes'][y]}), train_cuisine.index)
        map(lambda z: db.get_collection('training_dataset').insert_one(z), training_dataset)

        db.get_collection('recipes').insert_one({'desc': 'recipesInfo','recipeCount': total_recipes})
        db.get_collection('ingredStats').insert_one({'desc':'globalTotalIngredient','global_total': ingredients_global_total})
    except pymongo.errors.WriteError, e:
        print(u"unsuccessful write: {}").format(e)
    print(training_dataset)

def add_to_dataset(cuisine_input, ingred_input):
    try:
        db.recipes.update_one({'desc': 'recipesInfo'}, {"$inc": {'recipeCount': 1}})
        map(lambda i: db.ingredStats.update_one({"ingredient": i}, {"$inc": {cuisine_input : 1, 'globalCount': 1}},
                                            upsert = True), ingred_input)
        db.ingredStats.update_one({'desc':'globalTotalIngredient'},{'$inc':{'global_total': len(ingred_input)}})
        db.cuisine.update_one({'cuisine': cuisine_input}, {"$inc" : {'count' : 1}}, upsert = True)
    except pymongo.errors.WriteError, e:
        print(u"unsuccessful write: {}").format(e)

def predictor_score(ingredients):
    not_in_ingredients =set(i['ingredient'] for i in db.ingredStats.find({"ingredient": {"$exists": True}})).difference(ingredients.keys())
    for j in not_in_ingredients:
        ingredients[j]=0.0
    model = MultinomialNB(alpha = 1.0, fit_prior = True, class_prior = None)
    X = pandas.DataFrame([y for y in db.training_dataset.find()])
    a = pandas.DataFrame(X['ingredients'].tolist()).fillna(0)
    model.fit(X=a, y=X['cuisine'])
    print(model.predict(ingredients))

if __name__ == "__main__":

    # Connect To Db
    try:
        conn = pymongo.MongoClient('localhost', 27017)
        print("Connected")
    except pymongo.errors.ConnectionFailure, e:
        print(u"could not connect to db {}").format(e)
    db = conn['cuisine']
    #create_dataset()
    predictor_score(pandas.DataFrame({"coconut oil":1.0,
      "garam masala":1.0,
      "chickpeas":1.0,
      "cilantro":1.0,
      "ground ginger":1.0,
      "fresh leav spinach":1.0,
      "garlic":1.0,
      "chickpeas":1.0}, index=[0]))
