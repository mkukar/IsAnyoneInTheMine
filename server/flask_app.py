from flask import Flask
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from isanyoneinthemine import IsAnyoneInTheMine

TEMPLATES_DIR =  Path(__file__).parent.resolve() / 'templates'
PAGE_TEMPLATE = 'page.html'

load_dotenv()
mine = IsAnyoneInTheMine()
app = Flask(__name__)
environment = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
template = environment.get_template(PAGE_TEMPLATE)

@app.route("/")
def display_homepage():
    status_text = "YES" if mine.is_anyone_in_the_mine() else "NO"
    return template.render(
        PAGE_NAME="IsAnyoneInTheMine?",
        PAGE_BODY="<h1>Is Anyone in the Mine? <b>{0}</b></h1>".format(status_text)
    )

@app.route("/api/isanyoneinthemine", methods=['GET'])
def is_anyone_in_the_mine():
    return {"isanyoneinthemine" : mine.is_anyone_in_the_mine()}

@app.errorhandler(404)
def page_not_found(e):
    return template.render(
        PAGE_NAME="IsAnyoneInTheMine? - 404",
        PAGE_BODY="<h1>404 - Check your map, or craft one if you don't have it!</h1>"
    ), 404

@app.errorhandler(500)
def internal_error(e):
        return template.render(
        PAGE_NAME="IsAnyoneInTheMine? - 404",
        PAGE_BODY="<h1>500 - A creeper got into our server!</h1><p>Try again later :(</p>"
    ), 500
