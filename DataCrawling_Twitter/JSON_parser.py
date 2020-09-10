import tweepy
import json
from datetime import datetime, timedelta
from pytz import timezone
import time
import re
import demoji

inputfile = "AbrahamWeintraub_1000tweets"
country = "Brazil"
null = None


def connect_to_twitter():
    consumer_key = "iXmQt84QTdU4uVajypugSsPqV"
    consumer_secret = "GeTYh729O5dgBYytHxwR8Q4vImth5htFVqb4zbV65792mLPpeb"
    access_key = "1066216367504875520-X3RwzrhlbN1CQE3GefdsJXR6ns6uaa"
    access_secret = "0tWzmtZlzgs5OgsaMf235tllns23LhLCcWHcOG1sswB0F"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api


def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    timenow = t.replace(second=0, microsecond=0, minute=0, hour=t.hour) + timedelta(hours=t.minute // 30)
    return timenow.strftime("%Y-%m-%d %H:%M:%S %Z%z")


def remove_hashtags(string):
    string_array = string.split(' ')
    output_string = ''
    op_list = []
    for word in range(0, len(string_array)):
        try:
            if string_array[word].startswith('#') or '#' in string_array[word]:
                continue
            else:
                if string_array[word] not in op_list:
                    op_list.append(string_array[word])
        except IndexError as e:
            break
    for w in op_list:
        output_string = output_string + ' ' + w
    return output_string


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    # list_emoji=demoji.findall(string)
    return emoji_pattern.sub(r'', string)


def remove_url(string):
    # text = re.sub(r'^http\s+?:\/\/.*[\r\n]*', '', string, flags=re.MULTILINE)
    text = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
        " ", string)
    return text


def get_emoji_list(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)

    emoticons_dict = demoji.findall(string)
    if not emoticons_dict is null:
        emo_list = []
        for emo in emoticons_dict.keys():
            emo_list.append(emo)
    return emo_list


def remove_user_mentions(string):
    string_array = string.split(' ')
    output_string = ''
    op_list = []
    for word in range(0, len(string_array)):
        try:
            if string_array[word].startswith('@') or '@' in string_array[word]:
                continue
            else:
                if string_array[word] not in op_list:
                    op_list.append(string_array[word])
        except IndexError as e:
            break
    for w in op_list:
        output_string = output_string + ' ' + w
    return output_string


def modify_fields_json(inputfile):
    f = open(inputfile + '.json', "r")
    tweets = f.read()
    tweets_json = json.loads(tweets)
    modified_tweets_list = []
    for tweet in tweets_json:
        filtered_text = ''
        modified_tweet = tweet
        modified_tweet['poi_name'] = tweet['user']['screen_name']
        modified_tweet['poi_id'] = tweet['user']['id_str']
        modified_tweet['verified'] = tweet['user']['verified']
        modified_tweet['country'] = country  #hardcoded from top
        modified_tweet['replied_to_tweet_id'] = tweet['in_reply_to_status_id_str']
        if tweet['in_reply_to_status_id_str'] is null:  # check if None = null
            modified_tweet['replied_to_user_id'] = null
            modified_tweet['reply_text'] = null
        else:
            modified_tweet['replied_to_user_id'] = tweet['in_reply_to_user_id_str']
            modified_tweet['reply_text'] = tweet['full_text']
            # have to convert date
        modified_tweet['tweet_text'] = tweet['full_text']
        modified_tweet['tweet_lang'] = tweet['lang']
        temp_text = tweet['full_text']
        filtered_text_without_emoji = remove_emoji(temp_text)
        filtered_text_without_hashtags = remove_hashtags(filtered_text_without_emoji)
        filtered_text_without_mentions = remove_url(filtered_text_without_hashtags)
        filtered_text=remove_user_mentions(filtered_text_without_mentions)
        if tweet['lang'] == "hi":
            modified_tweet['text_hi'] = filtered_text
            modified_tweet['text_en'] = null
            modified_tweet['text_pt'] = null
        elif tweet['lang'] == "en":
            modified_tweet['text_en'] = filtered_text
            modified_tweet['text_hi'] = null
            modified_tweet['text_pt'] = null
        elif tweet['lang'] == "pt":
            modified_tweet["text_pt"] = filtered_text
            modified_tweet['text_hi'] = null
            modified_tweet['text_en'] = null
        else:
            modified_tweet['text_hi'] = null
            modified_tweet['text_en'] = null
            modified_tweet['text_pt'] = null
        hashtags = []
        if len(tweet['entities']['hashtags']) != 0:
            for hashtag in tweet['entities']['hashtags']:
                hashtags.append(hashtag['text'])

        modified_tweet['hashtags'] = hashtags
        user_list = []
        for user in tweet['entities']['user_mentions']:
            user_list.append(user['screen_name'])
        modified_tweet['mentions'] = tweet['entities']['user_mentions']
        modified_tweet['tweet_urls'] = tweet['entities']['urls']
        emo_list = get_emoji_list(tweet['full_text'])
        modified_tweet['tweet_emoticons'] = emo_list
        date_str = tweet['created_at']
        date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y'))
        datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
        datetime_obj_utc.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        updated_time = hour_rounder(datetime_obj_utc)
        modified_tweet['tweet_date'] = updated_time
        modified_tweet['tweet_loc'] = tweet['coordinates']

        modified_tweets_list.append(modified_tweet)
        modified_tweet = []
    f.close()
    return modified_tweets_list


def store_tweets(alltweets, filename):
    op = json.dumps(alltweets)
    with open('modified' + filename + '.json', 'w+') as f1:
        f1.write(op)


if __name__ == '__main__':
    list_of_tweets = modify_fields_json(inputfile)
    store_tweets(list_of_tweets, inputfile)
