from flask import render_template, request
from app import app, flickr
import xml.etree.ElementTree as ET
import random
import json
from urllib2 import Request, urlopen

def getPhoto(search_text):
    try:
        response = None
        if search_text == u'sky is clear':
            response = flickr.photos_search(tags='sunny,cloudless',\
                sort='relevance')
        else:
            response = flickr.photos_search(text=search_text, sort='relevance')
        if response.attrib['stat'] == 'ok':
            photos = response.find('photos')
            index = random.randint(0, len(photos)-1)
            photo = photos[index]
            imageUrl = 'https://farm' + photo.attrib['farm'] + \
                '.staticflickr.com/' + photo.attrib['server'] + '/' + \
                photo.attrib['id'] + '_' + photo.attrib['secret'] + '.jpg'
            return imageUrl
        else:
            print 'Not ok'
            return "http://"
    except Exception, e:
        print "Unexpected error: " + str(e)
        return "http://"
        
def getWeather(city):
    weatherUrl = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + \
        '&units=metric'
    request = Request(weatherUrl)
    try:
    	response = urlopen(request)
    	weatherJson = response.read()
    	return json.loads(weatherJson)
    except Exception, e:
        print "Unexpected error: " + str(e)
        return None

@app.route('/', methods=['GET'])
def index():
    weather = getWeather(request.args.get('city', 'seoul'))
    # print str(weather)
    if weather:
        description = weather[u'weather'][0][u'description']
        temp = weather[u'main'][u'temp']
        humidity = weather[u'main'][u'humidity']
        imageUrl = getPhoto(description)
        return render_template('index.html', imageUrl=imageUrl, \
            description=description, temp=temp, humidity=humidity)
    else:
        return "no weather"