# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 15:21:08 2018

@author: David
"""
import tweepy
from tweepy import OAuthHandler
import pika
import time

tweets = []


class TwitterClient(tweepy.StreamListener):

    def __init__(self):
        tweepy.StreamListener.__init__(self)
        #time.sleep(5)
        #credentials = pika.PlainCredentials('admin', 'admin') # , credentials=credentials
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue2', durable=True)

    def on_status(self, status):
        self.send_tweets_rabbitmq(status)

    def send_tweets_rabbitmq(self, tweet):

        self.channel.basic_publish(exchange='',
                              routing_key='task_queue2',
                              body=tweet.text,
                              properties=pika.BasicProperties(
                                 delivery_mode = 2, # make message persistent
                              ))
        print(" [x] Sent %r" % tweet)

    

def on_error(self, status_code):
    if status_code == 420:
        self.connection.close()
        return False


def main():
    consumer_key = "YdpxSvyUBDPJa8ADRTdPPrdhC"
    consumer_secret = "J6I9U3t2rTGioGMHkcQWspibVIagKlui7MaIuWj8m2VwgObK7J"
    access_token = "968102258960412677-ZYxlzoAxoWX3M6KG5yYtlxWKgGUOmPG"
    access_token_secret = "e7r6g3lnEkoHd57z82IAOhjNFDJDgmeHqLrs19oKaHTB6"
    auth = OAuthHandler(consumer_key, consumer_secret)
    # set access token and secret
    auth.set_access_token(access_token, access_token_secret)

    myStreamListener = TwitterClient()
    myStream = tweepy.Stream(auth=auth, listener=myStreamListener)
    myStream.filter(track=['Trump'], languages=["en"])


if __name__ == "__main__":
    # calling main function
    print("sleeping")
    time.sleep(60)
    main()
