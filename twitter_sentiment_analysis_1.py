import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
  
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'XXXXXXXXXX'
        consumer_secret = 'XXXXXXXXXXXX'
        access_token = 'XXXXXXXXXX'
        access_token_secret = 'XXXXXXXXXXXXX'
  
        try: 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        tweets = [] 
        try: 
            fetched_tweets = self.api.search(q = query, count = count) 
            for tweet in fetched_tweets: 
                parsed_tweet = {} 
                parsed_tweet['text'] = tweet.text 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
            return tweets 
        except tweepy.TweepError as e: 
            print("Error : " + str(e)) 
  
def main(): 
    api = TwitterClient() 
    print '--------------'
    tweets = api.get_tweets(query = 'Donald Trump', count = 100) 
    print 'Total Tweets: {}' .format(len(tweets))
  
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    print 'Positive Tweets: {}' .format(len(ptweets))
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 

    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    print 'Negtative Tweets: {}' .format(len(ntweets))
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 

    # picking neutral tweets from tweets 
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral'] 
    print 'Negtative Tweets: {}' .format(len(neutweets))
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {} %".format(100*len(neutweets)/len(tweets))) 
  
    print '--------------'
    print("Positive tweets:") 
    for index, tweet in enumerate(ptweets): 
        print(str(index+1) + ') ' + tweet['text']) 
  
    print '--------------'
    print("Negative tweets:") 
    for index, tweet in enumerate(ntweets): 
        print(str(index+1) + ') ' + tweet['text']) 
  
    print '--------------'
    print("Neutral tweets:") 
    for index, tweet in enumerate(neutweets): 
        print(str(index+1) + ') ' + tweet['text']) 

if __name__ == "__main__": 
    main() 
