# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 15:29:02 2018

@author: David
"""
import time
from pymongo import MongoClient
import datetime
import re
from textblob import TextBlob
import pika

tweets = {}


class TwitterSentiment(object):
    def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        df = {}
        tweet = TwitterSentiment.clean_tweet(body.decode('utf-8'))
        if tweet.startswith('NEWS,'):
            df['text'].replace('NEWS,', '')# remove the news tag
            df = TwitterSentiment.get_tweet_sentiment(df)
            df['topic'] = 'NEWS'
        else:  
            if tweet not in tweets:
                df['text'] = tweet
                df['topic'] = 'TWEET'
                df['text'].replace('Tweet', '') # remove the tweet tag
                df = TwitterSentiment.get_tweet_sentiment(df)
        TwitterSentiment.write_sentiments_db(df)

    def write_sentiments_db(df):
        client = MongoClient('mongo') #'mongo'
        db = client.test_database
        posts = db.posts
        posts.insert_one(df).inserted_id
       

    def get_tweet_sentiment(dataframe):
        sentiment = ''
        analysis = TextBlob(TwitterSentiment.clean_tweet(dataframe["text"]))
        if analysis.sentiment.polarity > 0:
            sentiment = 'positive'
        elif analysis.sentiment.polarity == 0:
            sentiment = 'neutral'
        else:
            sentiment = 'negative'
        dataframe['sentiment'] = sentiment
        dataframe['date'] = datetime.datetime.utcnow()
        return dataframe


def main():
    tries = 0
    #credentials = pika.PlainCredentials('admin', 'admin')
    while True:
        time.sleep(1)
        #try for tweets
        try: # , credentials=credentials
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()

            channel.queue_declare(queue='task_queue2', durable=True)
      
            channel.basic_consume(TwitterSentiment.callback, queue=  'task_queue2', no_ack=True)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
            connection.consumer_cancel_notify()
            channel.stop_consuming()
            connection.close()
            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
            break
        except:
            if tries >= 10:
                print("Tweet Feed its broken, we tried {} times".format(tries))
                break
            tries += 1
            time.sleep(1)
            
if __name__ == "__main__":
    #  calling main function
    #print("sleeping")
    #time.sleep(30)
    main()
