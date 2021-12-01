import json
import random
import pytest as pytest
import create_task as ct
from webserver import webserverHandler


def save_to_json(bot, path):
    json_object = json.dumps(bot)
    with open(path, "w") as outfile:
        outfile.write(json_object)


ct.create_play_sound_function()


@pytest.fixture()
def create_bots_to_test():
    my_base_bot = {
        "id": random.randrange(10000),
        "name": "my_bot",
        "intent": []
    }

    save_to_json(my_base_bot, "base_bot_test.json")
    # Opening JSON file
    bot1 = {
        "permissions_list": ["play_sound"],
        "allOf": [my_base_bot]
    }
    save_to_json(bot1, "bot1_test.json")
    # add intent to bot1
    f = open("bot1_test.json", "r")
    bot_dict = json.load(f)
    f.close()
    bot_dict['allOf'][0]['intent'].append('play_sound')
    bot1 = {
        "allOf": bot_dict['allOf'],
        "permissions_list": bot_dict["permissions_list"]
    }
    print(bot1)
    f = open("bot1_test.json", "w")
    json.dump(bot1, f)
    f.close()


def test_do_get():
    do_get_server = webserverHandler()
    res = do_get_server.do_GET()
    assert res == "Get return"

        # self.fail()

#
# def test_do_get():
#     assert False
