import tweepy
import json
import time

screen_name = "AbrahamWeint"
# filenamefinal = "PiyushGoyal"
inputfile = "AbrahamWeintraub_1000tweets.json"


def connect_to_twitter():
    consumer_key = "iXmQt84QTdU4uVajypugSsPqV"
    consumer_secret = "GeTYh729O5dgBYytHxwR8Q4vImth5htFVqb4zbV65792mLPpeb"
    access_key = "1066216367504875520-X3RwzrhlbN1CQE3GefdsJXR6ns6uaa"
    access_secret = "0tWzmtZlzgs5OgsaMf235tllns23LhLCcWHcOG1sswB0F"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api


def get_all_tweets(screen_name: object):
    api = connect_to_twitter()
    temptweets = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=screen_name, result_type='recent', timeout=999999,
                               tweet_mode='extended').items(3000):
        if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
            temptweets.append(tweet._json)
            # print(tweet)
    print(len(temptweets))
    return temptweets


def store_tweets(alltweets, filename):
    op = json.dumps(alltweets)
    with open(filename + ".json", 'w+') as f1:
        f1.write(op)


def check_tweet_replies_length(tweet_replies_dict):
    cond_fulfilled = False
    for tweet_id in tweet_replies_dict.keys():
        if len(tweet_replies_dict[tweet_id]) >= 500:
            cond_fulfilled = True
        else:
            cond_fulfilled = False
            break
    return cond_fulfilled


def get_replies(screen_name, filename):
    api = connect_to_twitter()
    replies = []
    f = open(filename + '.json', "r")
    tweets = f.read()
    tweets_json = json.loads(tweets)
    tweets_for_reply = []
    # print(tweets_json)
    f.close()
    for tweet in tweets_json:
        t = tweet['created_at']
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(t, '%a %b %d %H:%M:%S +0000 %Y'))
        if '2019-09-02 00:00' <= ts < '2019-09-07 00:00':
            tweets_for_reply.append(str(tweet['id']))
    # print(tweets_for_reply)

    tweets_for_reply.sort(reverse=True)
    replies = {}
    # print("tweet count for reply: %d", count)

    count = 0
    for t_id in tweets_for_reply:
        if count == 0:
            tweet_replies = tweepy.Cursor(api.search, q='to:{} filter:replies'.format(screen_name), sinceId=t_id,
                                          tweet_mode='extended').items(300)
        else:
            tweet_replies = tweepy.Cursor(api.search, q='to:{} filter:replies'.format(screen_name), sinceId=t_id,
                                          max_id=prev - 1, tweet_mode='extended').items(300)

        while True:
            try:
                reply = tweet_replies.next()
                if hasattr(reply, 'in_reply_to_status_id_str'):
                    if reply.in_reply_to_status_id_str in replies:
                        if check_tweet_replies_length(replies) or len(replies[t_id]) >= 100:
                            break
                        replies[reply.in_reply_to_status_id_str].append(reply._json)
                    elif reply.in_reply_to_status_id_str in tweets_for_reply:
                        replies[reply.in_reply_to_status_id_str] = [reply._json]

            except tweepy.RateLimitError as e:
                print("--------------- Rate Limit Exceeded --------------")
                print(e)
                time.sleep(60 * 15)
                continue

            except tweepy.TweepError as e:
                print("--------------- Tweep Error --------------")
                print(time.time())
                print(e)
                time.sleep(60 * 15)
                continue

            except Exception as e:
                print(e)
                break

        count = count + 1
        prev = int(t_id)
        if check_tweet_replies_length(replies):
            break

    # print(replies)
    return replies


if __name__ == '__main__':
    # pass in the username of the account you want to download
    alltweets = get_all_tweets(screen_name)

    # store the data into json file
    # store_tweets(alltweets, filenamefinal)
    #list_screen_names = "wilsonwitzel"
    #list_filenames = "WilsonWitzel_1000tweets"
    # for i in range(0, len(list_screen_names) - 1):
    #replies = get_replies(list_screen_names, list_filenames)
    #for reply in replies.keys():
     #   print(reply + ": %d", len(replies[reply]))

    store_tweets(alltweets,inputfile)
