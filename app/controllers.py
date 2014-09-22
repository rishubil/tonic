from flask import render_template
from app import app, flickr
import xml.etree.ElementTree as ET
import random

@app.route('/')
def index():
    try:
        response = flickr.photos_search(text='seoul rainy')
        if response.attrib['stat'] == 'ok':
            photos = response.find('photos')
            index = random.randint(0, len(photos)-1)
            photo = photos[index]
            imageUrl = 'https://farm' + photo.attrib['farm'] + \
                '.staticflickr.com/' + photo.attrib['server'] + '/' + \
                photo.attrib['id'] + '_' + photo.attrib['secret'] + '_b.jpg'
            return render_template('index.html', imageUrl=imageUrl)
            # return imageUrl
        else:
            return 'Not ok'
    except Exception, e:
        return "Unexpected error: " + str(e)
    # https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}_[mstzb].jpg
    # return flickr.test_echo(boo='baah')
    # return "Testing for flask"