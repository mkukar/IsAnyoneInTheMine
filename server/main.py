from flask import Flask
from dotenv import load_dotenv

from isanyoneinthemine import IsAnyoneInTheMine

load_dotenv()
mine = IsAnyoneInTheMine()
app = Flask(__name__)

STYLEHEADER = "<head><link rel=\"stylesheet\" href=\"static/styles.css\"></head>"

@app.route("/")
def display_homepage():
    status_text = "YES" if mine.is_anyone_in_the_mine() else "NO"
    return "{0}<body><h1>Is Anyone in the Mine? <b>{1}</b></h1></body>".format(STYLEHEADER, status_text)

@app.route("/api/isanyoneinthemine", methods=['GET'])
def is_anyone_in_the_mine():
    return {"isanyoneinthemine" : mine.is_anyone_in_the_mine()}

@app.errorhandler(404)
def page_not_found(e):
    return "{0}<body><h1>404 - Check your map, or craft one if you don't have it!</h1></body>".format(STYLEHEADER)

@app.errorhandler(500)
def internal_error(e):
    return "{0}<body><h1>500 - A creeper got into our server!</h1><p>Try again later :(</p></body>".format(STYLEHEADER)