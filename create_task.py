import json
from flask_restful import abort
'''
:save_to_json - save the object in the json file according to the path
:param: func_object- the function we want to save
:param: path -  in which jason file to save
'''

def check_if_func_exist(func_name, bot_type):
    # get bot permissions_list
    f = open(bot_type + '.json')
    bot_dict = json.load(f)
    functions_list = bot_dict["functions"]
    if func_name in functions_list:
        return "exist"
    else:
        return "not exist"


def save_to_json(func_object, path, mode):
    json_object = json.dumps(func_object)
    with open(path, mode) as outfile:
        outfile.write(json_object)


def add_intent_and_permissions(bot_permission, func_name, func):
    # add function to bot1
    file = bot_permission + ".json"
    f = open(file, "r")
    bot_dict = json.load(f)
    f.close()
    bot_dict['allOf']['intent'].append(func_name)
    bot_dict['functions'][func_name] = func[func_name]
    if bot_permission == 'bot1':
        bot_dict['permissions_list'].append(func_name)
        bot = {
            "allOf": bot_dict['allOf'],
            "permissions_list": bot_dict["permissions_list"],
            "functions": bot_dict["functions"]
        }
    elif bot_permission == 'bot2':
        bot = {
            "allOf": bot_dict['allOf'],
            "functions": bot_dict["functions"]
        }

    else:
        bot = {
            "allOf": bot_dict['allOf'],
            "is_basic_authentication": bot_dict["is_basic_authentication"],
            "password": bot_dict["password"],
            "certificate": bot_dict["certificate"],
            "functions": bot_dict["functions"]
        }
    save_to_json(bot, file, "w")


def create_function(func_name, bot_permission, default_value=''):
    if default_value is '':
        func = {
            func_name: "This is the " + func_name + " function"
        }
    else:
        func = {
            func_name: default_value
        }
    save_to_json(func, "logic.json", "a")
    ans= check_if_func_exist(func_name=func_name, bot_type=bot_permission)
    if ans == "not exist":
        add_intent_and_permissions(bot_permission, func_name, func)
        return {'status': 201, 'message': "Function added successfully"}
    else:
        return {'status': 409, 'message': "Function already exist in the bot"}



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


def put_in_func(bot, func, new_value):
    path = bot + '.json'
    with open(path, "r") as jsonFile:
        data = json.load(jsonFile)

    data["functions"][func] = new_value

    with open(path, "w") as jsonFile:
        json.dump(data, jsonFile)
