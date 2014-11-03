from flask import Flask
from flask import Response
from pymongo import MongoClient
import logging
import os.path
import datetime
import sys
import json

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.newsmapp
posts = db.newsitems
counters = db.counters

def nextSequence():
    doc = counters.find_one({'type':'itemcount'})
    print doc
    if not doc:
        print 'no counter found'
        counters.insert({
            'type': 'itemcount',
            'count': 0
        })
        doc = counters.find_one({'type':'itemcount'})
    doc['count'] =  doc['count'] + 1
    counters.update({'type': doc['type']}, doc)
    return doc['count']


def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "all.log"),"w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get():
    # Convert from string to ObjectId:
    docs = []
    for doc in posts.find():
        docs.append(doc)
    return docs

def getPost(post_id):
    doc = posts.find_one({'_id': post_id})
    return doc

def getPostCountry(country):
    docs = []
    for doc in posts.find():
        print doc
        if country in doc['country']:
            docs.append(doc)
    return docs

@app.route('/')
def hello_world():
    post = {
        "_id"       : nextSequence(),
        "provider"  : "BBC News",
        "title"     : "Burkina Faso army told to hand over power",
        "headline"  : "The African Union (AU) has given Burkina Faso's military a two-week deadline to hand power to a civilian ruler or face sanctions.",
        "summary"   : "The AU said the army had acted unconstitutionally when it took over after President Blaise Compaore was forced to resign on Friday.",
        "category"  : "politics",
        "url"       : "http://www.bbc.com/news/world-africa-29888244",
        "lat"       : 50,
        "lng"       : 50,
        "country"   : ["NL", "DE"],
        "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    }
    posts.insert(post)
    post = {
        "_id"       : nextSequence(),
        "provider"  : "BBC News",
        "title"     : "Burkina Faso army told to hand over power",
        "headline"  : "The African Union (AU) has given Burkina Faso's military a two-week deadline to hand power to a civilian ruler or face sanctions.",
        "summary"   : "The AU said the army had acted unconstitutionally when it took over after President Blaise Compaore was forced to resign on Friday.",
        "category"  : "politics",
        "url"       : "http://www.bbc.com/news/world-africa-29888244",
        "lat"       : 50,
        "lng"       : 100,
        "country"   : ["NL", "DE"],
        "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    }
    posts.insert(post)
    post = {
        "_id"       : nextSequence(),
        "provider"  : "BBC News",
        "title"     : "Burkina Faso army told to hand over power",
        "headline"  : "The African Union (AU) has given Burkina Faso's military a two-week deadline to hand power to a civilian ruler or face sanctions.",
        "summary"   : "The AU said the army had acted unconstitutionally when it took over after President Blaise Compaore was forced to resign on Friday.",
        "category"  : "politics",
        "url"       : "http://www.bbc.com/news/world-africa-29888244",
        "lat"       : 0,
        "lng"       : 20,
        "country"   : ["US"],
        "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    }
    posts.insert(post)
    return 'Post saved'

@app.route('/post/<int:post_id>')
def get_post(post_id):
    return Response(json.dumps(getPost(post_id)),  mimetype='application/json')

@app.route('/post/country/<string:country>')
def get_post_country(country):
    return Response(json.dumps(getPostCountry(country)),  mimetype='application/json')

@app.route('/post/all')
def get_all():
    return Response(json.dumps(get()),  mimetype='application/json')


initialize_logger('/var/www/server')
 
logging.debug("debug message")
logging.info("info message")
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")

if __name__ == '__main__':
    app.run(host='0.0.0.0')