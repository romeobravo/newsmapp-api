# -*- coding: UTF-8 -*-

from flask import Flask, request, jsonify
from flask import Response
from pymongo import MongoClient
import logging
import os.path
import datetime
import sys
import json
import glob

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.newsmapp
posts = db.newsitems
surveys = db.surveys
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


# @app.route('/')
# def hello_world():
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "BBC News",
#         "title"     : "Burkina Faso army told to hand over power",
#         "headline"  : "The African Union (AU) has given Burkina Faso's military a two-week deadline to hand power to a civilian ruler or face sanctions.",
#         "summary"   : "The AU said the army had acted unconstitutionally when it took over after President Blaise Compaore was forced to resign on Friday. The military said a civilian-led transitional government would be established as quickly as possible. Mr Compaore quit after mass protests at his bid to extend his 27-year rule. On Saturday, the military named Lt Col Isaac Zida, previously second in command of the presidential guard, as the new interim ruler. <br> A popular revolt led to Mr Compaore's resignation, but the military takeover was against democracy, said AU official Simeon Oyono Esono, following a meeting of the body's Peace and Security Council in Ethiopia. The AU will apply sanctions against Burkina Faso if the military fails to give up power within two weeks, Mr Esonohe told Reuters. The BBC's Emmanuel Igunza in the Ethiopian capital Addis Ababa says the sanctions could include suspension of Burkina Faso's AU membership and a travel ban on military officials.",
#         "category"  : "politics",
#         "url"       : "http://www.bbc.com/news/world-africa-29888244",
#         "lat"       : 12,
#         "lng"       : -2,
#         "country"   : ["BF"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "BBC News",
#         "title"     : "Roger Federer out of ATP World Tour final v Novak Djokovic",
#         "headline"  : "Roger Federer has withdrawn from the ATP World Tour final against Novak Djokovic because of a back injury",
#         "summary"   : "The 33-year-old Swiss announced he was not match-fit as he apologised in person to the crowd at the O2 Arena. Federer beat Stan Wawrinka 4-6 7-5 7-6 (8-6) on Saturday in a thrilling semi-final lasting two hours and 48 minutes. It is Djokovic's fourth victory at the season-ending event and he also becomes the first man to win three titles on the trot since Ivan Lendl in the 1980s.",
#         "category"  : "sports",
#         "url"       : "http://www.bbc.com/sport/0/tennis/30074849",
#         "lat"       : 52,
#         "lng"       : -0.29,
#         "country"   : ["GB"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "BBC News",
#         "title"     : "MH17 flight investigators remove crucial debris",
#         "headline"  : "Local workers have removed crucial debris and human remains from the crash site of the MH17 jet in rebel-held eastern Ukraine after months of delays.",
#         "summary"   : "The team, overseen by Dutch experts, targeted areas of the plane where most of the bodies are still unidentified. The debris and remains will be taken to the Netherlands for examination. The plane was shot down in July killing all 298 people on board - mostly Dutch nationals. Russia-backed rebels have been blamed, though they deny it. Dutch experts oversaw workers from the self-proclaimed Donetsk People's Republic cutting up parts of the plane and using cranes to load them onto lorries. Inspectors from the Netherlands had wanted to retrieve the debris themselves, but agreed to work with the rebel administration as they feared for their safety.",
#         "category"  : "conflict",
#         "url"       : "http://www.bbc.com/news/world-europe-30073283",
#         "lat"       : 49,
#         "lng"       : 37,
#         "country"   : ["NL", "UA"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "BBC News",
#         "title"     : "China to double Iranian investment",
#         "headline"  : "China is set to double its investment in Iranian infrastructure projects, Iran's Mehr news agency reports.",
#         "summary"   : "China has raised its quota for Iranian projects to $52bn (33bn) from $25bn the report said, quoting Iran's deputy minister for energy, Esmail Mahsouli. Water, electricity, oil and gas projects will all benefit from the extra financing, Mr Mahsouli said. Iran has turned to China, Russia and Turkey for financing as Europe and the US have strict sanctions on the nation. The US has an almost total economic embargo on Iran, while the European Union tightened up its sanctions in 2012, particularly targeting the energy and banking industries.",
#         "category"  : "economy",
#         "url"       : "http://www.bbc.com/news/business-30075807",
#         "lat"       : 32,
#         "lng"       : 53,
#         "country"   : ["IR", "CN"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)
    
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "BBC News",
#         "title"     : "Iraqi army 'had 50,000 ghost troops' on payroll",
#         "headline"  : "An investigation into corruption in the Iraqi army has revealed that there were 50,000 false names on its payroll.",
#         "summary"   : "Known in the military as \"ghost soldiers\", they either did not exist or no longer reported for duty, however their salaries were still paid. A statement from the PM's office said the payments have been stopped. Correspondents say rampant corruption in the Iraqi army is seen as one of the reasons why it has struggled to contain Islamic State militants. A spokesman for Prime Minister Haidar al-Abadi, quoted by AFP news agency, said the investigation began when the latest salary payments were made. \"Over the past few weeks, the prime minister has been cracking down to expose the ghost soldiers and get to the root of the problem,\" said Rafid Jaboori. It is thought that the salaries were siphoned off by corrupt officers. An unnamed officer told AFP that the 50,000 names include soldiers who had deserted or were killed in recent fighting. The US has spent billions of dollars trying to build up the Iraqi army. But security forces were caught by surprise by an IS offensive last summer and lost huge swathes of territory in northern and western Iraq.", 
#         "category"  : "conflict",
#         "url"       : "http://www.bbc.com/news/world-middle-east-30269343",
#         "lat"       : 33.071633800309,
#         "lng"       : 43.2,
#         "country"   : ["IQ"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)    
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "RT",
#         "title"     : "China overtakes Japan to become world's second largest stock market",
#         "headline"  : "The capitalization of the Chinese stock market increased 33 percent in 2014 reaching $4.48 trillion, which makes the market second only to the US.",
#         "summary"   : "Japan's stock market declined 3.2 percent to $4.46 trillion in 2013, according to Bloomberg analysts. The Chinese market surge came hot on the heels of allowing foreign investors unprecedented access to mainland shares through the merger of the Shanghai and Hong Kong stock exchanges. The decision to spur the Chinese economy has made the country an attractive investment. On November 21 the People's Bank of China reduced its key interest rate for the first time in two years. Economists predict Chinese authorities will put in place additional measures to support the economy, which slowed to a five-year low in the third quarter this year. The weakening of the yen against the dollar has played an important part in the falling capitalization of the Japanese market. After Shinzo Abe's tight monetary policy proved to be ineffective, the yen has seen a 10 percent decline in 10 months. China had once been the world's second largest stock market. In March 2011, it briefly surpassed Japan, which was hit by a devastating earthquake. The disaster was accompanied by a sharp fall in stock market indices.",
#         "category"  : "economy",
#         "url"       : "http://rt.com/business/209835-chinese-market-overtakes-japanese/",
#         "lat"       : 31.2,
#         "lng"       : 120.9,
#         "country"   : ["CN", "JP"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)    
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "The Independent",
#         "title"     : "Switzerland votes on ending mass immigration",
#         "headline"  : "The controversial Ecopop movement wants to slash the numbers entering the coutry from 80,000 a year to just 16,000",
#         "summary"   : "Their critics call them “Birkenstock racists” and accuse them of marrying Green ideology with the toxic xenophobia of the far right. But if the controversial “Ecopop” movement wins a key referendum in Switzerland today there are fears that they could ring some alarming changes in the Alpine nation. Ecopop takes its name from the French terms “Ecologie” and “Population”.  The movement believes that there are too many people in the world and that draconian immigration cuts and massive investment in birth control for the developing world are the only ways to address the problem. Ecopop wants Switzerland to slash its annual immigration to 0.2 percent of the country's population. “We don't want to see our countryside covered in concrete because it has to cope with an immigrant population flood,” said Andreas Thommen one of Ecopop's activists, a farmer and father of three. “I don't' mind foreigners, but it the numbers that count,” he says. If Ecopop's policy were enforced it would mean cutting Switzerland's annual immigration from the current 80,000 to just 16,000. Critics point out that such a move would torpedo the country's key agreements with the European Union on free movement of labour and spell disaster for the economy. But the movement's also has another aim: it wants to oblige Switzerland to spend at least ten percent of its annual development aid budget on voluntary birth control and family planning projects in the Third World. Ecopop claims its objective, which is based on a 1972 Club of Rome study entitled “The limits of growth”, is to prevent a global population explosion.",
#         "category"  : "politics",
#         "url"       : "http://www.independent.co.uk/news/world/europe/switzerland-votes-on-ending-mass-immigration-9893224.html",
#         "lat"       : 46.67,
#         "lng"       : 7.6,
#         "country"   : ["CH"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)    
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "The Nation",
#         "title"     : "This Is Black Friday in Bangladesh",
#         "headline"  : "",
#         "summary"   : "Walmart marks the holiday season this Friday with deals on its Faded Glory women's sweaters. But this time of year marks a different occasion in another corner of Walmart's empire: In Bangladesh, survivors and families remember the second anniversary of a massive fire at the Tazreen factory on the outskirts of Dhaka. After the fire on November 24, 2012, as families mourned over the incinerated bodies in the factory ruins, activists dug up some damning shreds of evidence: they uncovered a Faded Glory label, proving that the workers had produced Walmart-branded clothes. Today, two years on, Walmart seems eager to put the horrific legacy of Tazreen behind it. But the victims, including 112 dead and many others left injured and impoverished, can't move on. The disaster left Maliha partially blind, with severe leg and head injuries, leading her husband to abandon her “to avoid taking care of me.” She recounted in a 2013 report by the Clean Clothes Campaign and International Labor Rights Forum (ILRF), “The money I used to earn at Tazreen helped me support my ill mother in the village. Now, I wonder everyday how to survive and feed my children who are so young.”",
#         "category"  : "economy",
#         "url"       : "http://www.thenation.com/blog/191585/black-friday-bangladesh",
#         "lat"       : 22.5,
#         "lng"       : 89.5,
#         "country"   : ["BD"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)    
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "Estonian World",
#         "title"     : "Estonia becomes the first country in the world to offer e-residency",
#         "headline"  : "Estonia is set to make a history by starting the first supranational e-residency scheme in the world.",
#         "summary"   : "More than a hundred years ago, the renowned Estonian folklorist and linguist Jakob Hurt proclaimed: “Let us remain Estonians, but let us become Europeans!” This task has successfully been accomplished for the ancient Nordic nation, but from 1 December, foreigners can turn the old call around and say: “Let us remain world citizens, but let us become Estonians!” as the ambitious national startup project of giving e-residency to people around the world kicks off. The e-resident number one will be Edward Lucas, senior editor at the Economist magazine, and a great long-time friend and advocate of Estonia",
#         "category"  : "technology",
#         "url"       : "http://estonianworld.com/business/estonia-becomes-first-country-world-offer-e-residency/",
#         "lat"       : 58.8,
#         "lng"       : 23.8,
#         "country"   : ["EE"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)    
#     post = {
#         "_id"       : nextSequence(),
#         "provider"  : "Charlotte Observer",
#         "title"     : "Blatter: 2022 World Cup will be played in Qatar",
#         "headline"  : "FIFA president Sepp Blatter responded to the latest criticism of the World Cup bidding process by assuring Asian football delegates that the tournament will go ahead in Qatar in 2022.",
#         "summary"   : "\"Believe me, with all what has been said, what is told around the world, by whom? By those ... not involved exactly (with) what has happened or what happens in football,\" he said. \"The World Cup 2022 will be played in Qatar.\" Blatter made his latest remarks about the World Cup during a speech at the Asian Football Confederation's 60th anniversary celebrations in Manila late Sunday. Allegations of bribery and favor-seeking have engulfed world football in the four years since Russia was awarded the 2018 World Cup and Qatar was selected as host for 2022. The Swiss attorney general has already received a criminal complaint from FIFA against possible law-breaking by unnamed individuals mentioned in American attorney Michael Garcia's investigation into the 2018 and 2022 World Cup bidding process, and the British government is considering launching a criminal investigation.",
#         "category"  : "sports",
#         "url"       : "http://www.charlotteobserver.com/2014/11/30/5353444/blatter-2022-world-cup-will-be.html#.VHwuATGG_60",
#         "lat"       : 25.2,
#         "lng"       : 51.2,
#         "country"   : ["QA"],
#         "date"      : datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
#     }
#     posts.insert(post)
#     return 'Post saved'

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

@app.route('/exp/result', methods=["POST"])
def save_result():
    obj = json.loads(request.data)
    docs = list(surveys.find({'_id': obj['_id']}))
    print obj['_id']
    if len(docs) is 0:
        surveys.insert(obj)
    return Response('',  mimetype='application/json');

initialize_logger('/var/www/server')
 
logging.debug("debug message")
logging.info("info message")
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")


posts.drop()
script_dir = os.path.dirname(__file__)
print script_dir
file_path = os.path.join(script_dir, 'articles.json')


f = open(file_path, 'r')
for line in f.read().split("\n"):
    print line
    if line:
        lineJson = json.loads(line)
        lineJson['_id'] = nextSequence()
        lineJson['date'] = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        postid = posts.insert(lineJson)
        print 'inserted with id: ' , postid

    f.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')