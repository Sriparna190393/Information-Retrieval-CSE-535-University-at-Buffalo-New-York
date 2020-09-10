from datetime import datetime, timedelta
from pytz import timezone
import time
import re

'''import demoji
import preprocessor as p

demoji.download_codes()

string = "पप्पू, तेरा तो ये बोलना बनता है....🤣🤣"

emo = demoji.findall(string)
# print(type(emo))
print(emo)
# d=string.encode('unicode-escape')
print(p.clean('Preprocessor is #awesome 👍 https://github.com/s/preprocessor'))'''

'''date_str = "Fri Sep 06 13:48:53 +0000 2019"
date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y'))
datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
print(datetime_obj_utc.strftime("%Y-%m-%d %H:%M:%S %Z%z"))


def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    timenow = t.replace(second=0, microsecond=0, minute=0, hour=t.hour) + timedelta(hours=t.minute // 30)
    return timenow.strftime("%Y-%m-%d %H:%M:%S %Z%z")'''

# print(hour_rounder(datetime_obj_utc))


'''def deEmojify(inputstring):
    #return inputstring.encode('ascii', 'ignore').decode('ascii')

    return emoji.get_emoji_regexp().sub(u'', inputstring)'''


# https://stackoverflow.com/a/49146722/330558
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_hashtags(string):
    string_array = string.split(' ')
    output_string=''
    op_list=[]
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
        output_string=output_string+' '+w
    return output_string


if __name__ == '__main__':
    #inputstring = 'While Baba is away, Mumma is being a bad copy. Mummiyan kaam par hi theek hai.👨‍👧 #father #proud'
    #inputstring='#namodriu jfhihef lmdkwq #dfikj'
    #inputstring= 'अमाननीय #राहुलजी..कम से कम दो चार टविट्स.. भारत के 135 करोड़ लोगों को ध्यान में रखते हुए.. आप रोजाना जरूर करे..क्योंकि देश की जनता का मनोरंजन आप से अच्छा कोई कर नहीं सकता..खैर.. भिजवा दे?? कहीं भूखा ना मर जाए?? 😎🤔😅'
    inputstring='अब लग गए ना ज़्ज़त के बट्टे😂'
    str1=remove_emoji(inputstring)
    print(remove_hashtags(str1))
