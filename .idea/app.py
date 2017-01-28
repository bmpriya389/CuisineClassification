from flask import Flask, render_template

application = Flask(__name__)

@application.route('/')
def show_home_page():
    return 'Hello'

if __name__=="__main__":
    application.run(host='0.0.0.0')