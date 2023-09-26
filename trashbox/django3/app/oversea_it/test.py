import sys
import json
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Statichub
import datetime
import markdown

import urllib3


SE_MAINTAIN_KEYS = {
    'access_token':'1349555933257469955-WbaP6d9zGAgW1s7ojZ4TLBZBCdGYV5',
    'access_secret':'EphtxrZL6dApZiu9Ijs5qsHVB9J4DWYCyAfZg7U1jwvcf',
    'consumer_key' : "5IHbswu1IxG9jWWlCJnTkxVZn",
    'consumer_secret':"LOJVAtsOAtdOQj9KukUE3gR5Qhdwx4BVUExll4GmWXp7e2GqFp"
}

FEATUHER = {
    'access_token' : '968269222525587456-nTufoFnhYpNIY1sLQwB9WYGiDlAIEMM',
    'access_secret' : 'rhoqnAXt3VHz9dnNv8DlyDUd9V1fijfw2Of091UkjVUTV',
    'consumer_key' : 'nAllJpqiUKtnUG4aHrk2G6T9v',
    'consumer_secret' : 'QAY2CnNGt2onuun6QckyYniZeh753q6X4dEXw9mS3pjTecPk9Y'
}

FEATUHER = {
    'access_token' : '968269222525587456-nTufoFnhYpNIY1sLQwB9WYGiDlAIEMM',
    'access_secret' : 'rhoqnAXt3VHz9dnNv8DlyDUd9V1fijfw2Of091UkjVUTV',
    'consumer_key' : 'nAllJpqiUKtnUG4aHrk2G6T9v',
    'consumer_secret' : 'QAY2CnNGt2onuun6QckyYniZeh753q6X4dEXw9mS3pjTecPk9Y'
}

KEY = "AAAAAAAAAAAAAAAAAAAAAANLdAEAAAAA5KC6e%2F5Cp5dnphqQc03R5p3GcjE%3DBHTDd7pxR5kcedwzzTkMy74ojkaccqq3FLsuPG4KJfUeD5J0Th"

#user = 

#q = f"to:{user} until:{until} since:{since}"
q = "to:xtremepentest until:2022-05-29 since:2022-05-28 min_faves:20"

myTwitterAction = Twitter.MyTwitterAction(FEATUHER)
tweet_list = myTwitterAction.search_tweet_list(q, 100)


## this is answer 
## to:d_feldman until:2018-08-08 since:2018-08-06 

json_tweets = json.dumps(tweet_list, ensure_ascii=False, indent=4)

print(json_tweets)

