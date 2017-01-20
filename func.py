from __future__ import division, print_function
import pandas
import numpy
import json
from collections import Counter
import pymongo
from sklearn.naive_bayes import MultinomialNB


def create_dataset():
    # load training set
    train = json.load(open('train.json'))

    training_dataset = pandas.DataFrame(
        [{"id": i["id"], "cuisine": i["cuisine"], "ingredients": dict(Counter(i["ingredients"]))} for i in train]
    )

    ingredients_global = pandas.DataFrame(training_dataset["ingredients"].tolist()).fillna(0.0)
    ingredients_stat = ingredients_global.describe()

    # creating a collection for ingredient stats
    try:
        db.create_collection('ingredStats')
        db.create_collection('training_dataset')
        map(lambda x: db.ingredStats.insert_one({'ingredient': x, 'stats': dict(ingredients_stat[x])}),
            ingredients_stat.keys())
        map(lambda z: db.training_dataset.insert_one(dict(training_dataset.loc[z])), training_dataset.index)
    except pymongo.errors.ConnectionFailure, e:
        print("{}".format(e))


def add_to_dataset(id, cuisine_input, ingred_input):
    try:
        db.training_dataset.insert_one({"id": id, "cuisine": cuisine_input, "ingredients": dict(Counter(ingred_input))})
        training_dataset_ingred = pandas.DataFrame(
            pandas.DataFrame([i for i in db.training_dataset.find()])['ingredients'].tolist()).fillna(0).describe()
        print(training_dataset_ingred)
        map(lambda x: db.ingredStats.update_one({'ingredient': x},
                                                {'$set': {'stats': dict(training_dataset_ingred[x])}}, upsert=True),
            training_dataset_ingred.keys())
    except pymongo.errors.WriteError, e:
        print(u"unsuccessful write: {}").format(e)


def predictor_score(ingredients):

    ingredients = Counter(ingredients)
    not_in_ingredients = set(
        i['ingredient'] for i in db.ingredStats.find({"ingredient": {"$exists": True}})).difference(ingredients.keys())
    for j in not_in_ingredients:
        ingredients[j] = 0.0
    model = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
    X = pandas.DataFrame([y for y in db.training_dataset.find()])
    a = pandas.DataFrame(X['ingredients'].tolist()).fillna(0)
    model.fit(X=a, y=X['cuisine'])
    a = numpy.array(pandas.Series(ingredients)).reshape(1, -1)
    print(model.predict(a))


if __name__ == "__main__":

    # Connect To Db
    try:
        conn = pymongo.MongoClient('localhost', 27017)
        print("Connected")
    except pymongo.errors.ConnectionFailure, e:
        print(u"could not connect to db {}").format(e)
    db = conn['cuisine']
    #create_dataset()
    """
    predictor_score([
		"noodles", "garam masala", "coconut oil", "chickpeas",
		"vegetable stock", "chickpeas", "cinnamon sticks", "garlic"
    ])
    """
