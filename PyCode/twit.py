#! /usr/bin/python3

import tweepy as tw
import wget
import os
import time

class twit_use():

    def __init__(self, twitter_auth_keys):
        auth = tw.OAuthHandler(
                twitter_auth_keys['consumer_key'],
                twitter_auth_keys['consumer_secret']
                )
        auth.set_access_token(
                twitter_auth_keys['access_token'],
                twitter_auth_keys['access_token_secret']
                )
        self.api = tw.API(auth)

    def post_to_twit(self, image_url, caption_):
        local_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        image_filename  = wget.download(image_url, local_path)
        #print('Downloaded: ', image_filename)
        
        #print('UPLOADING')
        time.sleep(1)
        #upload the photo to the API after storing local
        media = self.api.media_upload(image_filename)
        #set the message to tweet
        tweet = caption_
        #post the tweet
        post_result = self.api.update_status(status=tweet, media_ids=[media.media_id])
        
        time.sleep(1)
        
        mydir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        
        #delete the file
        filelist = [f for f in os.listdir(mydir) if '.jpg' in f]
        for f in filelist:
            os.remove(os.path.join(mydir, f))