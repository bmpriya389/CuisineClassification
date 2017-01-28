from flask import Flask, render_template, request, json, __version__
from classify import predictor_score
import pymongo


try:
    conn = pymongo.MongoClient('localhost', 27017)
    print("Connected")
    print(__version__)
except pymongo.errors.ConnectionFailure, e:
    print(u"could not connect to db {}").format(e)
db = conn['cuisine']


application = Flask(__name__)

@application.route('/')
def show_home_page():
    return render_template('writeRecipe.html')


@application.route('/predict', methods = ['POST'])
def predict():
    input_ingreds = request.json['ingreds']
    return json.jsonify(predictor_score(input_ingreds, db))

if __name__=="__main__":
    application.run(host='0.0.0.0')