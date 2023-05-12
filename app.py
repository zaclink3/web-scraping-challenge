from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_data_info = mongo.db.mars_website_db.find_one()
    return render_template("index.html", mars_website_data=mars_website_data)

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()
    mongo.db.mars_website_db.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
