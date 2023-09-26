import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Statichub
import datetime
import time
import json
import GoogleTrans



def translate_tweet_list(tweet_list):
    new_tweet_list = []
    
    count = 0
    for tweet in tweet_list:
        count += 1
        if count <= 3:
            text = str(tweet["text"])
            new_text = GoogleTrans.en_to_ja(text)
            tweet.update({
                "text" : new_text
            })
        new_tweet_list.append(tweet)
    return new_tweet_list




def main():
    repo = "engineer_rank"
    tag_list = Github.seach_page_list(repo)
    for htmlname in tag_list:
        Github.delete_page(repo, htmlname)
        print("mainloop:", htmlname,"has deleted")
        myTwitterAction = Twitter.MyTwitterAction()
        tweet_list = myTwitterAction.search_tweet_list('"'+ htmlname+ '"' + " lang:ja min_faves:100", amount=50)
        
        git_json = {}
        git_json.update({
            "tweet_list" : tweet_list
        })

        text = json.dumps(git_json, ensure_ascii=False, indent=4)
        Github.upload(repo, htmlname, text)
        print("mainloop:", htmlname,"is created")
        time.sleep(4)


def main2():
    repo = "overseas"
    for htmlname in Github.seach_page_list(repo):

        tweet_list = []
        myTwitterAction = Twitter.MyTwitterAction()
        query = htmlname + " lang:en min_faves:100"
        tweet_list = myTwitterAction.search_tweet_list(
            query,
            amount=50)
        tweet_list = translate_tweet_list(tweet_list)

        git_json = {}
        git_json.update({
            "tweet_list" : tweet_list
        })
        text = json.dumps(git_json, ensure_ascii=False, indent=4)
        Github.delete_page(repo, htmlname)
        Github.upload(repo, htmlname, text)
        time.sleep(4)


one_circle_time = 60*60*24

time_count = 0
while True:
    if (60*60*3)%(time_count+1) == 1:
        try:
            pass
            #main()
        except:
            pass
    if (60*60*8 + 60*30)%(time_count+1) == 1:
        try:
            main2()
        except:
            import traceback
            traceback.print_exc()
    
    time_count += 1
    if time_count > one_circle_time:
        time_count = 0