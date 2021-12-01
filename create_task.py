import json

'''
:save_to_json - save the object in the json file according to the path
:param: func_object- the function we want to save
:param: path -  in which jason file to save
'''
def save_to_json(func_object, path, mode):
    json_object = json.dumps(func_object)
    with open(path, mode) as outfile:
        outfile.write(json_object)


def add_intent_and_permissions(bot_permission, func_name, func):
    # add function to bot1
    file = bot_permission + ".json"
    f = open(file, "r+")
    bot_dict = json.load(f)
    f.close()
    bot_dict['allOf']['intent'].append(func_name)
    bot_dict['functions'].append(func)
    if bot_permission == 'bot1':
        bot_dict['permissions_list'].append(func_name)
        bot = {
            "allOf": bot_dict['allOf'],
            "permissions_list": bot_dict["permissions_list"],
            "functions": bot_dict["functions"]
        }
    else:
        bot = {
            "allOf": bot_dict['allOf'],
            "functions": bot_dict["functions"]
        }
    save_to_json(bot, file, "w")


def create_function(func_name, bot_permission, default_value=''):
    if default_value is None:
        func = {
            func_name: "This is the " + func_name + "function"
        }
    else:
        func = {
            func_name: default_value
        }
    save_to_json(func, "logic.json", "a")
    add_intent_and_permissions(bot_permission, func_name, func)


def create_play_sound_function(bot_permission, sound="Lalalala"):
    play_sound = {
        "play_sound": "Playing " + sound
    }
    save_to_json(play_sound, "logic.json", "a")

    # add function to bot1
    add_intent_and_permissions('bot1', 'play_sound', play_sound)


def create_default_welcome_message_function(bot_permission, default_welcome_message="Hello"):
    default_welcome_message = {
        "default_welcome_message": default_welcome_message
    }
    save_to_json(default_welcome_message, "logic.json", "a")

    # add function to bot2
    add_intent_and_permissions('bot2', 'default_welcome_message', default_welcome_message)
