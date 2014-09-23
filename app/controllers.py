from flask import render_template, request
from app import app, flickr
import xml.etree.ElementTree as ET
import random
import json
from urllib2 import Request, urlopen

def getLicenses():
    try:
        licenses = {}
        response = flickr.photos_licenses_getInfo()
        if response.attrib['stat'] == 'ok':
            result = response.find('licenses')
            for i in result:
                index = i.attrib['id']
                licenses[str(index)] = {'name': i.attrib['name'], 'url': i.attrib['url']}
            return licenses
        else:
            print 'flickr.photos_licenses_getInfo failed'
            return None
    except Exception, e:
        print "Unexpected error: " + str(e)
        return None
        
licenses = getLicenses()

def getPhoto(search_text):
    def getPhotos(search_text):
        try:
            response = None
            if search_text == u'sky is clear':
                response = flickr.photos_search(tags='sunny,cloudless',\
                    sort='relevance', safe_search='1', license='0,1,2,4,5,7,8')
            else:
                response = flickr.photos_search(text=search_text, \
                    sort='relevance', safe_search='1', license='0,1,2,4,5,7,8')
            if response.attrib['stat'] == 'ok':
                return response.find('photos')
            else:
                print 'flickr.photos_search failed'
                return None
        except Exception, e:
            print "Unexpected error: " + str(e)
            return None
            
    def getPhotoUrl(photo):
        try:
            imageUrl = 'https://farm' + photo.attrib['farm'] + \
                    '.staticflickr.com/' + photo.attrib['server'] + '/' + \
                    photo.attrib['id'] + '_' + photo.attrib['secret'] + '.jpg'
            return imageUrl
        except Exception, e:
            print "Unexpected error: " + str(e)
            return "http://"
    
    def getPhotoInfo(photoId):
        try:
            response = None
            response = flickr.photos_getInfo(photo_id=photoId)
            if response.attrib['stat'] == 'ok':
                return response.find('photo')
            else:
                print 'flickr.photos_getInfo failed'
                return None
        except Exception, e:
            print "Unexpected error: " + str(e)
            return None
            
    photos = getPhotos(search_text)
    index = random.randint(0, len(photos)-1)
    photo = getPhotoInfo(photos[index].attrib['id'])
    imageUrl = getPhotoUrl(photo)
    license = licenses[str(photo.attrib['license'])]
    # print ET.tostring(photo, encoding='utf8', method='xml')
    owner = photo.find('owner')
    author = owner.attrib['username']
    authorUrl = 'https://www.flickr.com/people/' + owner.attrib['nsid']
    
    return {'imageUrl': imageUrl, 'license': license, 'author': author, 'authorUrl': authorUrl}
        
def getWeather(city):
    weatherUrl = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + \
        '&units=metric'
    request = Request(weatherUrl)
    try:
    	response = urlopen(request)
    	weather = json.loads(response.read())
    	if weather and u'cod' in weather:
            cod = weather[u'cod']
            if cod == 200:
                description = weather[u'weather'][0][u'description']
                temp = weather[u'main'][u'temp']
                humidity = weather[u'main'][u'humidity']
                return {'description': description, 'temp': temp, \
                'humidity': humidity}
                
            else:
                print "Weather is none: cod is " + str(cod)
                return None
        else:
            print "Weather is none: Unexpected error"
            return None
    except Exception, e:
        print "Unexpected error: " + str(e)
        return None

@app.route('/', methods=['GET'])
def index():
    weather = getWeather(request.args.get('city', 'seoul'))
    if weather == None:
        return "Weather is none"
    photo = getPhoto(weather['description'])
    if weather == None:
        return "Photo is none"
    return render_template('index.html', weather=weather, photo=photo)