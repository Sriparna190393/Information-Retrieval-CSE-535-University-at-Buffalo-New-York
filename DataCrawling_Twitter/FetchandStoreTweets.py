import tweepy
import json

consumer_key = "ENU7J8YHtRq8kKyg89lgRKslN"
consumer_secret = "OuuU2XPFLBy1EZ0kbo1CN2t9XdOtoUWBt3QrwSNlJ1Rof1KFis"
access_key = "1014396246252015616-EROwqgzXy4CFDn4TFnWF8xaiEppLXR"
access_secret = "9VLlXalPLUcQ0qjEMHIaP36cc662AhA7NupfZYrzGHPzr"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
# api = tweepy.API(auth, wait_on_rate_limit=True)
poi_name = "CoryBooker"
lang = "en"


def get_all_tweets(screen_name, lang):
    temptweets = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=screen_name, result_type='recent', timeout=999999).items(
            2000):
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            temptweets.append(tweet)
            # print(tweet)
    count = 0

    for i in range(0, len(temptweets) - 1):
        if temptweets[i].lang == lang:
            count = count + 1
    print(len(temptweets))
    print('Count: ' + str(count))
    # print(len(temptweets))
    return temptweets


def store_tweets(tweetlist, filename):
    file = open(filename, 'w', encoding='utf8')
    for status in tweetlist:
        # print(status)
        json.dump(status._json, file)
    file.close()


if __name__ == '__main__':
    # pass in the username of the account you want to download
    alltweets = get_all_tweets(poi_name, lang)
    # store the data into json file
    store_tweets(alltweets, "CoryBooker_1000tweets.json")
