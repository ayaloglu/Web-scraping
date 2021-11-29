# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


# create route that renders index.html template
@app.route("/")

def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)



@app.route("/scrape")
def scraper():

    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.update({}, data, upsert=True)
    return redirect("/", code=302)
  
  



# to run from command line

if __name__ == "__main__":
    app.run(debug=True)