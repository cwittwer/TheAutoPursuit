#! /usr/bin/python3

import wget
import os
import time
from instabot import Bot
import crop_image as crp

username = 'carbotsocial@gmail.com'
password = 'Kubu_422312'

class insta_use():

    def __init__(self, insta_login):
        self.bot = Bot()
        self.bot.login(username=insta_login['username'],
                       password=insta_login['password'],
                       use_cookie= False)


    def upload_photo_insta(self, image_url, caption_):
        local_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        image_filename  = wget.download(image_url, local_path)
        #print('Downloaded: ', image_filename)

        crp.crop(image_filename)
        #print('Cropped: ', image_filename)

        
        #print('UPLOADING')
        time.sleep(1)
        self.bot.upload_photo(image_filename, caption=caption_)
        #print('UPLOADED')
        time.sleep(1)
        
        mydir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        
        filelist = [f for f in os.listdir(mydir) if '.jpg' in f]
        for f in filelist:
            os.remove(os.path.join(mydir, f))

        #if os.path.exists(image_filename):
        #    os.remove(image_filename)
        #    print('Delete: ', image_filename)
        #else:
        #    print('File does not exist')

    def logout(self):
        #self.bot.logout()
        pass
