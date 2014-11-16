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
        print doc['country']
        print country
        if country in doc['country']:
            docs.append(doc)
        print docs
    return docs

def getPostCategory(category):
    docs = []
    for doc in posts.find():
        print doc
        if category == doc['category']:
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
        "lat"       : 12,
        "lng"       : -2,
        "country"   : ["BF"],
        "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    }
    posts.insert(post)
    post = {
        "_id"       : nextSequence(),
        "provider"  : "BBC News",
        "title"     : "Roger Federer out of ATP World Tour final v Novak Djokovic",
        "headline"  : "Roger Federer has withdrawn from the ATP World Tour final against Novak Djokovic because of a back injury",
        "summary"   : "The 33-year-old Swiss announced he was not match-fit as he apologised in person to the crowd at the O2 Arena. Federer beat Stan Wawrinka 4-6 7-5 7-6 (8-6) on Saturday in a thrilling semi-final lasting two hours and 48 minutes. It is Djokovic's fourth victory at the season-ending event and he also becomes the first man to win three titles on the trot since Ivan Lendl in the 1980s.",
        "category"  : "sports",
        "url"       : "http://www.bbc.com/sport/0/tennis/30074849",
        "lat"       : 52,
        "lng"       : -0.29,
        "country"   : ["GB"],
        "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    }
    posts.insert(post)
    post = {
        "_id"       : nextSequence(),
        "provider"  : "BBC News",
        "title"     : "MH17 flight investigators remove crucial debris",
        "headline"  : "Local workers have removed crucial debris and human remains from the crash site of the MH17 jet in rebel-held eastern Ukraine after months of delays.",
        "summary"   : "The team, overseen by Dutch experts, targeted areas of the plane where most of the bodies are still unidentified. The debris and remains will be taken to the Netherlands for examination. The plane was shot down in July killing all 298 people on board - mostly Dutch nationals. Russia-backed rebels have been blamed, though they deny it. Dutch experts oversaw workers from the self-proclaimed Donetsk People's Republic cutting up parts of the plane and using cranes to load them onto lorries. Inspectors from the Netherlands had wanted to retrieve the debris themselves, but agreed to work with the rebel administration as they feared for their safety.",
        "category"  : "conflict",
        "url"       : "http://www.bbc.com/news/world-europe-30073283",
        "lat"       : 49,
        "lng"       : 37,
        "country"   : ["NL", "UA"],
        "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    }
    posts.insert(post)
    post = {
        "_id"       : nextSequence(),
        "provider"  : "BBC News",
        "title"     : "China to double Iranian investment",
        "headline"  : "China is set to double its investment in Iranian infrastructure projects, Iran's Mehr news agency reports.",
        "summary"   : "China has raised its quota for Iranian projects to $52bn (33bn) from $25bn the report said, quoting Iran's deputy minister for energy, Esmail Mahsouli. Water, electricity, oil and gas projects will all benefit from the extra financing, Mr Mahsouli said. Iran has turned to China, Russia and Turkey for financing as Europe and the US have strict sanctions on the nation. The US has an almost total economic embargo on Iran, while the European Union tightened up its sanctions in 2012, particularly targeting the energy and banking industries.",
        "category"  : "economy",
        "url"       : "http://www.bbc.com/news/business-30075807",
        "lat"       : 32,
        "lng"       : 53,
        "country"   : ["IR", "CN"],
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

@app.route('/post/category/<string:category>')
def get_post_category(category):
    return Response(json.dumps(getPostCategory(category)),  mimetype='application/json')

initialize_logger('/var/www/server')
 
logging.debug("debug message")
logging.info("info message")
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")

if __name__ == '__main__':
    app.run(host='0.0.0.0')