import feedparser
import pika
import time
from IPython import display
import praw

# A list to hold all headlines
allheadlines = []
#credentials = pika.PlainCredentials('admin', 'admin')  # rabbitmq #,credentials=credentials
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='task_queue2', durable=True)

class NewsStreamer():

    # Sends the news item over rabbit mq
    def send_news_rabbitmq(newsitem):
        # Here I attached the word NEWS so when it is sent down the queue
        # it can be added as a 'topic' when written to the database
            newsitem = "NEWS," + newsitem
            channel.basic_publish(exchange='',
                                  routing_key='task_queue2',
                                  body=newsitem,
                                  properties=pika.BasicProperties(
                                     delivery_mode = 2, # make message persistent
                                  ))
            print(" [x] Sent News %r" % newsitem)

    # Function grabs the rss feed headlines (titles) and returns them as a list
    def getHeadlines(rss_url):
        headlines = []
        feed = feedparser.parse(rss_url)
        for newsitem in feed['items']:
            headlines.append(newsitem['title'])
        return headlines


    def on_error(status_code):
        if status_code == 420:
            connection.close()
            return False

def main():
    newsStreamer = NewsStreamer()
    #reddit
    reddit = praw.Reddit(client_id='2_tq6wOnYXnh7g',
                         client_secret='scvg7U5vBdOB843CI3pRk0FtCXk',
                         user_agent='assignment_larkin')
    headlinesReddit = set()


    # List of RSS feeds that we will fetch and combine
    newsurls = {
        'apnews': 'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305',
        'googlenews': 'https://news.google.com/news/rss/?hl=en&amp;ned=us&amp;gl=US',
        'yahoonews': 'http://news.yahoo.com/rss/'
    }

    # Iterate over the feed urls
    for key, url in newsurls.items():
        allheadlines.extend(NewsStreamer.getHeadlines(url))
        # Call getHeadlines() and combine the returned headlines with allheadlines


    #reddit
    for submission in reddit.subreddit('politics').new(limit=None):
        headlinesReddit.add(submission.title)
        NewsStreamer.send_news_rabbitmq(submission.title)
        display.clear_output()
        print(len(headlinesReddit))
    # Iterate over the all headlines list and print each headline
    for hl in allheadlines:
        newsitem = hl
        NewsStreamer.send_news_rabbitmq(newsitem)
        print('----------------------------------')
        print(hl)

        
if __name__ == "__main__":
    print("sleeping")
    time.sleep(60)
    main()
