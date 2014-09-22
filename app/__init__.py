from flask import Flask
app = Flask(__name__)
import flickrapi
api_key = '1bb68d78110e40cee89a92ef52faddaa'
flickr = flickrapi.FlickrAPI(api_key, format='etree')
from app import controllers