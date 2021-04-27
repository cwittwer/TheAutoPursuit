import datetime

from flask import Flask, render_template
from google.cloud import datastore

datastore_client = datastore.Client()

app = Flask(__name__)

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp' : dt
    })

    datastore_client.put(entity)

def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times

def fetch_listings(lim, query_name):
    query = datastore_client.query(kind=query_name)
    query.order = ['-timestamp']

    listings = query.fetch(limit=lim)

    return listings

@app.route('/')
def index():
    # Store the current access time in Datastore
    store_time(datetime.datetime.now())

    #Fetch the most recent 10 access times from datastore.
    times = fetch_times(10)

    return render_template('index.html', times=times)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/classic-bimmers')
def classic_bimmers():

    cars = fetch_listings(20, 'BMW')

    return render_template('classic_bimmers.html', cars=cars)

@app.route('/m-cars')
def mcars():

    cars = fetch_listings(20, 'mcar')

    return render_template('mcars.html', cars=cars)

@app.route('/miata-hunter')
def miata_hunter():

    cars = fetch_listings(20, 'miata')

    return render_template('miata_hunter.html', cars=cars)

@app.route('/swedish-steel')
def swedish_steel():

    cars = fetch_listings(20, 'volvo')
    cars2 = fetch_listings(20, 'Saab')

    return render_template('swedish_steel.html', cars=cars)
    
@app.route('/barely-driven')
def barely_driven():

    cars = fetch_listings(20, 'barely')

    return render_template('barely_driven.html', cars=cars)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)