# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 15:38:49 2018

@author: David
"""

from pymongo import MongoClient
import datetime
from flask import Flask


app = Flask(__name__)


class TwitterWeb():
    def get_tweets_time(timeMin):
        tweet_list = []
        client = MongoClient('mongo') #'mongo'
        db = client.test_database
        # where topic is tweet
        tweet_list = list(db.posts.find({"date": {"$gt": datetime.datetime.utcnow() - datetime.timedelta(minutes=timeMin)}}))
        # filter the list on the topic of Tweet
        tweet_list = [token for token in tweet_list if token['topic'] == 'TWEET']
        return tweet_list
    
    def get_news_time(timeMin):
        news_list = []
        client = MongoClient('mongo') #'mongo'
        db = client.test_database
        # where topic is news
        news_list = list(db.posts.find({"date": {"$gt": datetime.datetime.utcnow() - datetime.timedelta(minutes=timeMin)}}))
        # filter the list on the topic of News
        news_list = [token for token in news_list if token['topic'] == 'NEWS']
        return news_list  
        

@app.route('/')
def read_values_from_db():
    output = ""
    print("requesting tweets")
   # TwitterWeb.get_tweets_time(1)
    # check if there is content for Tweets
    if(len(TwitterWeb.get_tweets_time(1)) > 0):
        tweet_list = TwitterWeb.get_tweets_time(1)
        ptweets = [tweet for tweet in tweet_list if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweet_list)))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweet_list if tweet['sentiment'] == 'negative']
        # percentage of negative tweets
        print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweet_list)))
        # percentage of neutral tweets
        print("Neutral tweets percentage: {} % ".format(100 * (len(tweet_list) - len(ntweets) - len(ptweets)) / len(tweet_list)))

        positiveTweets = 100 * (len(ptweets) / len(tweet_list))
        negativeTweets = 100 * (len(ntweets) / len(tweet_list))
        neutralTweets = 100 * (len(tweet_list) - len(ntweets) - len(ptweets)) / len(tweet_list)
        output = "Positive Tweets: %s<br>Negative Tweets: %s<br>Neutral Tweets: %s<br>" % (positiveTweets,negativeTweets,neutralTweets) + '\n';
    else:
        output="no tweets"
    #News Items
    # check if there is content for News
    if(len(TwitterWeb.get_news_time(1)) > 0):
        news_list = TwitterWeb.get_news_time(1)
        pNews = [news_item for news_item in news_list if news_item['sentiment'] == 'positive']
        # percentage of positive news
        print("Positive news percentage: {} %".format(100 * len(pNews) / len(news_list)))
        # picking negative news
        nNews = [news_item for news_item in news_list if news_item['sentiment'] == 'negative']
        # percentage of negative tweets
        print("Negative news percentage: {} %".format(100 * len(nNews) / len(news_list)))
        # percentage of neutral tweets
        print("Neutral news percentage: {} % ".format(100 * (len(news_list) - len(nNews) - len(pNews)) / len(news_list)))

        positiveNews = 100 * (len(pNews) / len(news_list))
        negativeNews = 100 * (len(nNews) / len(news_list))
        neutralNews = 100 * (len(news_list) - len(nNews) - len(pNews)) / len(news_list)
        output += "Positive News: %s<br>Negative News: %s<br>Neutral News: %s<br>" % (positiveNews, negativeNews,neutralNews)
    else:
        output+= "no news"
    return output


def main():
   
    app.run(host="0.0.0.0", port=8080)
    #app.run(host="localhost")


if __name__ == "__main__":
    # calling main function
    main()
