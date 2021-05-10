import datetime

from flask import Flask, render_template, request
from google.cloud import datastore

datastore_client = datastore.Client()

app = Flask(__name__)
LISTINGS_PER_PAGE=20

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

def fetch_listings(lim, query_name, off, secondary=None):
    query = datastore_client.query(kind=query_name)
    query.order = ['-timestamp']

    listings = query.fetch(limit=lim, offset=off)

    listofcars = {}
    i=1
    if secondary == 1:
        i=11
    for list in listings:
        listofcars.update({str(i):list})
        i=i+1
    i=1

    return listofcars

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

    page = request.args.get('page',1,type=int)
    offset= (page-1)*20
    cars = fetch_listings(20, 'BMW', offset) 

    return render_template('classic_bimmers.html', cars=cars)

@app.route('/m-cars')
def mcars():

    page = request.args.get('page',1,type=int)
    offset= (page-1)*20
    cars = fetch_listings(20, 'mcar', offset)

    return render_template('mcars.html', cars=cars)

@app.route('/miata-hunter')
def miata_hunter():

    page = request.args.get('page',1,type=int)
    offset= (page-1)*20
    cars = fetch_listings(20, 'miata', offset)

    return render_template('miata_hunter.html', cars=cars)

@app.route('/swedish-steel')
def swedish_steel():

    page = request.args.get('page',1,type=int)
    offset= (page-1)*10

    cars = fetch_listings(10, 'volvo', offset)
    cars2 = fetch_listings(10, 'Saab', offset, secondary=1)

    cars_ = {**cars, **cars2}

    return render_template('swedish_steel.html', cars=cars_)
    
@app.route('/barely-driven')
def barely_driven():

    page = request.args.get('page',1,type=int)
    offset= (page-1)*20
    cars = fetch_listings(20, 'barely', offset)

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