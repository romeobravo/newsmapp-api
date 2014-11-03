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
        print doc
        doc.pop("_id", None)
        docs.append(doc)
    return docs

@app.route('/')
def hello_world():
    post = {"author": "Mike",
        "id": nextSequence(),
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")}
    posts.insert(post)
    return 'Post saved'

@app.route('/post/<int:post_id>')
def get_posts(post_id):
    doc = get(post_id)
    logging.info(doc.author)
    return post

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