import tweet_fnts as twf
import json


def save_user_info(usname):
    user = twf.api.get_user(usname)
    usjson = user._json
    usjson["Following"] = [friend.screen_name for friend in twf.api.get_user(usname).friends()]

    with open('users.json','a') as f:
        json.dump(usjson,f)
        f.write("\n")


#TODO MAKE THIS WORK FOR GENERIC NUM OF LEVELS , OPTIMIZE FOR LESS API CALLS
def save_two_level_users(usname):
    depth = 2
    flwrs = twf.api.get_user(usname).friends()

    save_user_info(usname)

    for i in flwrs:
        for j in  twf.api.get_user(i.screen_name).friends():
            save_user_info(j.screen_name)
        save_user_info(i.screen_name)

# TESTING DATA ACCUM
# save_two_level_users("realDonaldTrump")



