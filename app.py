import requests
import configparser
from flask import Flask, render_template, request

# api key is stored in config.ini
def get_api_key():
	config = configparser.ConfigParser()
	config.read("config.ini")
	return config["openweathermap"]["api_key"]

# take in zip code and api and return the results of api
def get_weather_results(zip_code, api_key):
	# openweathermap.org
	api_url = "https://api.openweathermap.org/data/2.5/weather?zip={0}&units=imperial&appid={1}".format(zip_code, api_key)
	r = requests.get(api_url)
	return r.json()

# CREATE A SIMPLE FLASK APPLICATION:
app = Flask(__name__) # name is configured to be the name of the application replaced at runtime

# map application to a route to a simple webpage
@app.route("/") # route for homepage
def weather_dashboard():
	return render_template("home.html") # called in the app.route("/") (inside 'templates folder')

@app.route("/results", methods=["POST"]) # route for the results page
def render_results():
	zip_code = request.form["zipCode"]
	api_key = get_api_key()
	json_data = get_weather_results(zip_code, api_key)

	# temperature variables
	temp = "{0:.2f}".format(json_data["main"]["temp"])
	feels_like_temp = "{0:.2f}".format(json_data["main"]["feels_like"])
	weather_description = json_data["weather"][0]["main"]
	location = json_data["name"]
	
	# render tempalte for results page with variables set in the html
	return render_template("results.html",
						location=location,
						feels_like=feels_like_temp,
						weather_description=weather_description,
						temp=temp,
						zipCode=zip_code)

if __name__ == '__main__':
	app.run() # only run flask app once
