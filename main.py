# Inspired by https://github.com/rx00/GroupsAnalyser
import argparse
import json
import time

from urllib.request import urlopen
from urllib.parse import urlencode
from vk_auth import get_code, get_token


def call_api(method, params, token):
    params.append(("access_token", token))
    url = "https://api.vk.com/method/{}?{}".format(method, urlencode(params))
    res = urlopen(url).read().decode('utf-8')
    json_result = json.loads(str(res))
    if "response" not in json_result:
        return ""
    return json_result["response"]


def get_our_id(token):
    return call_api("users.get", [], token)[0]["uid"]


def get_friends(user_id, token):
    return call_api("friends.get", [("uid", user_id), ("fields", "deactivated")], token)


def delete_user(user_id, token):
    return call_api("friends.delete", [("uid", user_id)], token)


def delete_users_from_account(deleted, token):
    total = len(deleted)
    for i, uid in enumerate(deleted):
        delete_user(uid, token)
        time.sleep(1)
        print("Deleted: {} of {}\r"
              .format(i + 1, total)
              , end="")


def print_help_if_asked():
    parser = argparse.ArgumentParser(
        description="Removes deleted accounts from your page")
    return parser.parse_args()


if __name__ == '__main__':
    print_help_if_asked()
    get_code()
    code = input("Enter authorization code from web page: ")
    token = get_token(code)
    our_id = get_our_id(token)
    friends = get_friends(our_id, token)
    deleted = []
    for friend in friends:
        if "deactivated" in friend and friend["deactivated"] == "deleted":
            deleted.append(friend["uid"])
    print("Found {} deleted users".format(len(deleted)))
    delete_users_from_account(deleted, token)
    print("Removed all deleted accounts!")