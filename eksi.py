#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, tweepy, logging, json, pickle
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

logging.basicConfig(filename = 'eksi.log', level = logging.INFO, format = '%(asctime)s %(message)s')

def get_data(page):
    r = requests.get("https://eksisozluk.com/basliklar/gundem?p=" + page, headers = {"X-Requested-With": "XMLHttpRequest", "User-Agent": generate_user_agent()})
    soup = BeautifulSoup(r.text)

    data = '{"current_page": "' + page + '",'

    if(page == "1"):
        data += '"page_count": "2",'
    else:
        data += '"page_count": "' + soup.find("div", {"class": "pager"})["data-currentpage"] + '",'

    data += '"populer_title_models": ['

    o = soup.find("ul", {"class": "topic-list partial"}).find_all("a")

    for i in xrange(len(o)):
        title = o[i].text
        link = o[i]["href"]
        entry_count = o[i].find("small").text
        title = title.replace(' ' + entry_count, '')
        data += '{"title": "' + title + '", "link": "' + link + '", "entry_count": "' + entry_count + '"}'
        if i != (len(o) - 1):
            data += ","
    data += "]}"

    return data

def get_popular(page):
    text = ""
    try:
        text = get_data(str(page))
    except Exception as e:
        logging.info('Error with getting the popular titles')
    else:
        logging.info('Pulled the popular titles from API')
    return json.loads(text)

def load_list():
    try:
        iof = open("eksi.db", "rb")
    except Exception as e:
        logging.info('Error with opening the database')
    else:
        logging.info('Opened the database for reading')
    input_list = pickle.load(iof)
    iof.close()
    return input_list

def save_list(input_list):
    try:
        iof = open("eksi.db", "wb")
    except Exception as e:
        logging.info('Error with opening the database')
    else:
        logging.info('Opened the database for writing')
    pickle.dump(input_list, iof, 2)
    iof.close()

def main():
    input_list = load_list()

    titles = []

    i = 1
    popular = get_popular(i)

    while popular["populer_title_models"] != []:
        titles.extend([(k['title'].encode("utf-8"), k['link'].encode("utf-8"), k['entry_count']) for k in popular['populer_title_models']])
        i += 1
        popular = get_popular(i)

    for j in xrange(len(titles)):
        title, link, count = titles[j]
        if title not in input_list:
            try:
                count = int(count)
            except ValueError:
                if count.endswith('b'):
                    count = int(float(count[:-1].replace(',','.')) * 1000)
            if count >= 200:
                input_list.append(title)
                to_be_posted = title + ": https://eksisozluk.com" + link
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)
                try:
                        api.update_status(to_be_posted)
                except tweepy.TweepError as e:
                        logging.info('Can not tweet, reason: ' + str(e.message[0]['code']))
                else:
                        logging.info('Tweeted')
    titles = dict((x, z) for x, y, z in titles)

    input_list = [x for x in input_list if x in titles and ((titles.get(x).isdecimal() and int(titles.get(x)) >= 150) or titles.get(x).endswith("b"))]

    save_list(input_list)

main()
