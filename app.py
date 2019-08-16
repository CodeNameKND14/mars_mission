from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import mars_scraping

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db

collection = db.mars_data

#mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_news')

@app.route('/')
def index():
    mars_info_data = collection.find_one()
    return render_template('index.html', mars_info_data=mars_info_data)


@app.route('/scrape')
def scrape():
    mars_info_data = mars_scraping.mars_scrape()
    collection.update({}, mars_info_data, upsert=True)
    
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)