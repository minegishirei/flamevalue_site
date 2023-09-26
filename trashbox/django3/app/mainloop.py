import sys
if '/God' not in sys.path:
    sys.path.append('/God')
import Twitter
import Github
import Statichub
import datetime
import time
import json


repo = "engineer_rank"

def main():
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


while True:
    try:
        main()
    except:
        pass
    time.sleep(60*60*1)