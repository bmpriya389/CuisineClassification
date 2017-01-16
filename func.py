import pandas
import json
from collections import Counter
import pymongo

# load training set
train = json.load(open('test2.json'))

# create dictionaries for ingredients, no of recorded recipes per type of cuisine & ingredient count
cuisines = set([k["cuisine"] for k in train])
cuisineIngredient = dict.fromkeys(cuisines,[])
cuisineCount = dict.fromkeys(cuisines,0)
cuisineIngredientCount = dict.fromkeys(cuisines, Counter)

for i in train:
    if not cuisineIngredient[i['cuisine']]:
        cuisineIngredient[i['cuisine']] = i['ingredients']
    else:
        cuisineIngredient[i['cuisine']].extend(i['ingredients'])
    cuisineCount[i['cuisine']] += 1

cuisineIngredientCount = {i : Counter(cuisineIngredient[i]) for i in cuisineIngredient}

print cuisineIngredient

# Combine metioned dictionaries to form a dataframe with rows as cuisines and columns as no of recipes recorded, ingredients, no of time an ingredie nt has featured in a cuisine
trainCuisine = pandas.DataFrame({'noOfRecipes':cuisineCount, 'Ingredients': cuisineIngredient, 'IngredientsCount':cuisineIngredientCount })


ingredientsGlobal = [i for _ in trainCuisine['Ingredients'] for i in _]
ingredientsGlobalCount = dict(Counter(ingredientsGlobal))
ingredientsGlobalTotal = len(ingredientsGlobal)
ingredientsGlobal = list(set(ingredientsGlobal))
ingredientsCuisine = dict.fromkeys(ingredientsGlobal,{})


for i in ingredientsGlobal:
    ingredientsCuisine[i] = {j:trainCuisine.loc[j, "IngredientsCount"][i] for j in list(trainCuisine.index) if i in trainCuisine.loc[j, "IngredientsCount"].keys()}

for i in ingredientsGlobalCount:
    ingredientsCuisine[i]['globalCount'] = ingredientsGlobalCount[i]


try:
    conn = pymongo.MongoClient('localhost', 27017)
    print "Connected"
except pymongo.errors.ConnectionFailure, e:
    print "could not connect to db %s" %e

db = conn['cuisine']
print db

# creating a collection for ingredient stats
# db.drop_collection('ingredStats')

ingredientsID = dict.fromkeys(ingredientsCuisine.keys(),pymongo.results.InsertOneResult)

for i in ingredientsCuisine:
    ingredientsID[i] = db.get_collection('ingredStats').insert_one({i:ingredientsCuisine[i]}).inserted_id



print db.get_collection('ingredStats').find({"_id" : ingredientsID['indian']})

