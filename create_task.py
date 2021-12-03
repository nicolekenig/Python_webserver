import json
import auth


def save_to_json(func_object, path, mode):
    """
    save the object in the json file according to the path
    :param: func_object : (object) the function we want to save as a json object
    :param: path:  (string)  in which jason file to save
    """
    json_object = json.dumps(func_object)
    with open(path, mode) as outfile:
        outfile.write(json_object)


def add_intent_and_permissions(bot_permission, func_name, func):
    """
    adds the function to the bots intent, and save it in the bot's JSON file
    in case of bot1 add it to this permissions_list also
    :param bot_permission: (string) bot1/ bot2/ bot3
    :param func_name: (string) the function name to add
    :param func : (object) the function as a JSON
    """
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
    """
    the function crater
    :param func_name:  (string) the function name
    :param bot_permission:  (string) bot1/bot2/bot3
    :param default_value:  (string) the default return value of the function
    :return response status and message:(dictionary) {status:201/409, message:message}
    """
    if default_value is '':
        func = {
            func_name: "This is the " + func_name + " function"
        }
    else:
        func = {
            func_name: default_value
        }
    save_to_json(func, "logic.json", "a")
    exist = auth.check_if_func_exists(bot_type=bot_permission,func=func_name)
    if not exist:
        add_intent_and_permissions(bot_permission, func_name, func)
        return {'status': 201, 'message': "Function added successfully"}
    else:
        return {'status': 409, 'message': "Function already exist in the bot"}



def create_play_sound_function(bot_permission, sound="Lalalala"):
    """
    creating the play sound function for bot1
    :param bot_permission: (string)  bot1
    :param sound: (string) the sound to play
    """
    play_sound = {
        "play_sound": "Playing " + sound
    }
    save_to_json(play_sound, "logic.json", "a")

    # add function to bot1
    add_intent_and_permissions('bot1', 'play_sound', play_sound)


def create_default_welcome_message_function(bot_permission, default_welcome_message="Hello"):
    """
    creating the default welcome message function of bot2
    :param bot_permission: (string) bot2
    :param default_welcome_message: (string) the default welcome
    """
    default_welcome_message = {
        "default_welcome_message": default_welcome_message
    }
    save_to_json(default_welcome_message, "logic.json", "a")

    # add function to bot2
    add_intent_and_permissions('bot2', 'default_welcome_message', default_welcome_message)
