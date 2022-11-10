import requests
import configparser
from flask import Flask, render_template, request

# api key is stored in config.ini
def get_api_key():
	config = configparser.ConfigParser()
	config.read("config.ini")
	return config["openweathermap"]["api_key"]

# take in zip code and api and return the results of api
def get_weather_request(zip_code, api_key):
	# openweathermap.org
	api_url = "https://api.openweathermap.org/data/2.5/weather?zip={0}&appid={1}".format(zip_code, api_key)
	r = requests.get(api_url)
	return r.json()

# create a simple flask application:

app = Flask(__name__) # name is configured to be the name of the application replaced at runtime

# map application to a route to a simple webpage
@app.route("/") # route for homepage
def weather_dashboard():
	return render_template("home.html") # called in the app.route("/") (inside 'templates folder')

@app.route("/results", methods=["POST"]) # route for the results page
def render_results():
	zip_code = request.form["zipCode"]
	return "Zip Code: {0}".format(zip_code) # called in app.route("/results")

if __name__ == '__main__':
	app.run() # only run flask app once
	print(get_weather_request("80305", get_api_key()))
