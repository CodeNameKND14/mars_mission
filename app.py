# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
#import python function from mars_scraping.py
import mars_scraping

# Flask Setup 
app = Flask(__name__)

# Local MongoDB connection 
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# create/use database 
db = client.mars_db

# create/use collection
collection = db.mars_data

#mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_news')

# create route that renders index.html template and finds documents from mongo
# mars_db is the database; mars_data is the collection
@app.route('/')
def index():
    mars_info_data = collection.find_one()
    return render_template('index.html', mars_info_data=mars_info_data)

# Route that will trigger scrape function.
@app.route('/scrape')
def scrape():
    # Run scrape function
    mars_info_data = mars_scraping.mars_scrape()
    collection.update({}, mars_info_data, upsert=True)
    
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
