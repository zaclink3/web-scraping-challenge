from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# clear db 
mongo.db.drop_collection("mars_web_info")


@app.route("/")
def index():
    mars_web_info = mongo.db.mars_web_info.find_one()
    return render_template("index.html", mars_web_info=mars_web_info)

@app.route("/scrape")
def scraped():
    mars_web_info = mongo.db.mars_web_info
    mars_data_scraped = scrape_mars.scrape()
    mars_web_info.replace_one({}, mars_data_scraped, upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)


# print(scrape_mars.scrape())