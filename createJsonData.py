import random
import json
import create_task as ct


def create_bots():
    my_base_bot = {
        "id": random.randrange(10000),
        "name": "my_bot",
        "intent": []
    }

    ct.save_to_json(my_base_bot, "base_bot.json", "w")

    bot1 = {
        "allOf": my_base_bot,
        "permissions_list": [],
        "functions": {}
    }

    ct.save_to_json(bot1, "bot1.json", "w")

    bot2 = {
        "allOf": my_base_bot,
        "welcome_message": "Hello (default message)",
        "functions": {}
    }
    ct.save_to_json(bot2, "bot2.json", "w")

    bot3 = {
        "allOf": my_base_bot,
        "is_basic_authentication": True,
        "password": 46543,
        "certificate": "my-certificate!",
        "functions": {}
    }
    ct.save_to_json(bot3, "bot3.json", "w")


def add_intent():
    # add intent play_sound to bot1
    f = open("bot1.json", "r")
    bot_dict = json.load(f)
    f.close()
    bot_dict['allOf']['intent'].append('play_sound')
    bot1 = {
        "allOf": bot_dict['allOf'],
        "functions": bot_dict['functions']
    }
    f = open("bot1.json", "w")
    json.dump(bot1, f)
    f.close()

    # add intent default_welcome_message to bot2
    f = open("bot2.json", "r")
    bot_dict = json.load(f)
    f.close()
    bot_dict['allOf']['intent'].append('default_welcome_message')
    bot2 = {
        "allOf": bot_dict['allOf'],
        "permissions_list": bot_dict["permissions_list"],
        "functions": bot_dict['functions']
    }
    f = open("bot2.json", "w")
    json.dump(bot2, f)
    f.close()

def run():
    create_bots()
    ct.create_play_sound_function(bot_permission="bot1")
    ct.create_default_welcome_message_function(bot_permission="bot2")
    ct.create_function(func_name="make_api_call", bot_permission="bot3")
