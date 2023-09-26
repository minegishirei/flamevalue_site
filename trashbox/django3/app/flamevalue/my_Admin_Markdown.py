
import sys
if '/God' not in sys.path:
    sys.path.append('/God')

#import Github


def getAdminMarkdown(name):
    repo = "flamevalue_database"
    category = "admin_comment"
    if f"{name}.md" in Github.seach_page_list(repo, category):
        raw_comment = Github.load(repo, category + "/" +name +".md")
        return raw_comment
    return None



if __name__ == "__main__":
    print( getAdminMarkdown("React") )

