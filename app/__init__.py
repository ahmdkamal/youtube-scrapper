from flask import Flask
from dotenv import dotenv_values

app = Flask(__name__)
config = dotenv_values(".env")
app.config["MONGO_URI"] = "mongodb://" + config['DATABASE_USERNAME'] + ":" + config[
    'DATABASE_PASSWORD'] + "@mongo-inmobly/" + config['DATABASE_NAME'] + "?authSource=admin"

from app.src import youtube_controller
from app.helpers import response


@app.errorhandler(404)
def page_not_found(e):
    return response.error_response(404, 'url not found', [{"route": ["not-found"]}])


@app.errorhandler(500)
def page_not_found(err):
    return response.error_response(500, 'Something went wrong', [{"failed": [err]}])
