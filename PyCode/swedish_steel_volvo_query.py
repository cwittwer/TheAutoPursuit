#! /usr/bin/python3

import pandas as pd
import datetime as dt
from craigslist import CraigslistForSale
from bs4 import BeautifulSoup as bs
import swedish_steel_tokens as tt
import requests
import insta
import twit as twit
import logging
import os

site_search = ''
cat_use = 'cto' #cars and trucks by owner
query_use = 'volvo'
num_value = 0
path_to_script = os.path.dirname(os.path.abspath(__file__))

right_now = dt.datetime.now()
log_file = 'logs/'+str(round(right_now.timestamp()))+'_clbot.log'
f=open(os.path.join(path_to_script, log_file), 'w')


logging.basicConfig(filename=os.path.join(path_to_script, log_file),
                    filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

datetime_limit = dt.datetime.now() - dt.timedelta(hours=8) #constant for posting time limit
logging.info('Datetime limit: '+datetime_limit.strftime("%m/%d/%Y, %H:%M:%S"))

def convert(date_time):
    #logging.info('Convert function')
    format = '%Y-%m-%d %H:%M' # The format 
    datetime_str = dt.datetime.strptime(date_time, format) 
    return datetime_str 

def get_image_from_page(request_url):
    #logging.info('Pulling image from URL function')
    r = requests.get(request_url)
    #logging.info('Requests status: '+str(r.status_code))
    soup = bs(r.content, 'lxml')
    image_url_use = soup.find("div", { "class":"slide first visible"} ).img["src"]
    #logging.info('Found image url:'+image_url_use)
    return image_url_use

try:
    #Read in CSV with list of all CL sites in US
    site_list = pd.read_csv(r'/home/pi/Desktop/CarBot/us_cl_sites.csv') 

    logging.info('Setting up the instagram and twitter accounts')
    insta_app = insta.insta_use(tt.insta_login)
    twit_app = twit.twit_use(tt.twitter_auth_keys)

    #iterate through all the sites in the csv read in
    for i,j in site_list.iterrows(): 
        #logging.info(j['site'])

        #run the search on the specific site
        cl_fs_car = CraigslistForSale(site=j['site'], category=cat_use, 
                                        filters={'query': query_use, 'has_image': True, 'search_titles': True #, 'auto_transmission':'manual'
                                                     ,'auto_fuel_type': ['gas', 'hybrid', 'electric', 'other']
                                                    ,'max_year':'2000', 'auto_title_status' : ['clean','salvage','rebuilt','lien']})
        
        for result in cl_fs_car.get_results():
            try:
                date_time_use = convert(result['datetime']) #convert the string time from the ad to datetime format
                logging.info('found result!')
                if(date_time_use > datetime_limit): #check to see if posting time was within the last 24 hours from when the code was run
                    the_image = get_image_from_page(result['url']) #returns the first image on the ad, shouldn't error out as we filter to ads with images
                    logging.info(the_image)

                    #set the caption
                    caption = result['name']+'\nListing Price: '+ result['price']+'\nPost Date: '+ result['datetime'][0:10]+'\nLink: '+ result['url'] 
                    caption = caption+'\n#cars #volvo #carforsale #auto'
                    #logging.info('Caption: ', caption)
                    #upload the photo to Insta
                    insta_app.upload_photo_insta(the_image ,caption)
                    #upload the photo to Twitter
                    twit_app.post_to_twit(the_image ,caption)

                #logging.info(result['name'],' : ', result['price'],' : ', result['datetime'],' : ', result['url'])
            except:
                logging.error('AN ERROR OCURRED')
                pass

except KeyboardInterrupt:
    insta_app.logout()
    raise

