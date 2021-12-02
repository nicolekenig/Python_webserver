import json
import os


# ************************************** authentication functions **************************************
def is_authentication(bot_type, func):
    # get bot permissions_list
    f = open(bot_type + '.json')
    bot_dict = json.load(f)
    intent_list = bot_dict["allOf"]["intent"]
    return func in intent_list


def check_bot1_permissions(bot_type, func):
    # get bot permissions_list
    f = open(bot_type + '.json')
    bot_dict = json.load(f)
    permissions_list = bot_dict["permissions_list"]
    return func in permissions_list


def check_bot3_authentication(bot_type, name, password, certificate):
    f = open(bot_type + '.json')
    bot_dict = json.load(f)
    is_basic_authentication = bot_dict["is_basic_authentication"]
    is_name_valid = bot_dict["allOf"]["name"] == name
    is_password_valid = bot_dict["password"] == password
    is_certificate_valid = True
    if not is_basic_authentication:
        is_certificate_valid = bot_dict['certificate'] == certificate

    if is_name_valid and is_password_valid and is_certificate_valid:
        return True
    else:
        return False


# ************************************** delete bot function **************************************
def delete_bot(bot):
    try:
        # if os.path.exists(bot + '.json'):
        os.remove(bot + '.json')
        return {'status': 204, 'message': 'Bot deleted successfully'}
    except:
        return {'status': 404, 'message': 'File dose not exist or could not deleted bot'}


# ************************************** get function **************************************
def play_sound(bot_type):
    """
    This function responds to a request for /api/play_sound/{bot_type}
    with the sound the bot what to play

    :param bot_type: the bot who want to play sound
    :return:        sound
    """
    is_authorized = is_authentication(bot_type, "play_sound")
    bot_permission = True
    if is_authorized:
        if bot_type == 'bot1':
            bot_permission = check_bot1_permissions(bot_type, "play_sound")
        if bot_permission:
            f = open(bot_type + '.json')
            bot_dict = json.load(f)
            return {'status': 200, 'message': bot_dict["functions"]['play_sound']}

    elif (not is_authorized) or (not bot_permission):
        return {'status': 400, 'message': "You dont have permission for this function"}


def do_the_function(bot_type, func_name):
    f = open(bot_type + '.json')
    bot_dict = json.load(f)
    return {'status': 200, 'message': bot_dict["functions"][func_name]}


# ************************************** put and patch function **************************************
def update_in_func(bot, field_name, func_name, new_value):
    try:
        path = bot + '.json'
        with open(path, "r") as jsonFile:
            bot_dict = json.load(jsonFile)

        bot_dict[field_name][func_name] = new_value

        with open(path, "w") as jsonFile:
            json.dump(bot_dict, jsonFile)

        return {'status': 200, 'message': "Updated successfully"}
    except:
        return {'status': 400, 'message': "Something want wrong didnt updated successfully"}


def update_bot_name(bot, field_name, new_value):
    try:
        path = bot + '.json'
        with open(path, "r") as jsonFile:
            bot_dict = json.load(jsonFile)

        bot_dict["allOf"][field_name] = new_value

        with open(path, "w") as jsonFile:
            json.dump(bot_dict, jsonFile)
        return {'status': 200, 'message': "Updated successfully"}
    except:
        return {'status': 400, 'message': "Something want wrong didnt updated successfully"}


def update_bot_intent(bot, field_name, new_value):
    try:
        path = bot + '.json'
        with open(path, "r") as jsonFile:
            bot_dict = json.load(jsonFile)

        if new_value in bot_dict["allOf"][field_name]:
            bot_dict["allOf"][field_name].remove(new_value)
            if bot == "bot1":
                bot_dict["permissions_list"].remove(new_value)
        else:
            bot_dict["allOf"][field_name].append(new_value)

        with open(path, "w") as jsonFile:
            json.dump(bot_dict, jsonFile)

        return {'status': 200, 'message': "Patch successfully"}
    except:
        return {'status': 400, 'message': "Something want wrong didnt Patch successfully"}


def update_bot_permissions_list(bot, field_name, new_value):
    try:
        path = bot + '.json'
        with open(path, "r") as jsonFile:
            bot_dict = json.load(jsonFile)

        if new_value in  bot_dict[field_name]:
            bot_dict[field_name].remove(new_value)

        elif new_value not in bot_dict[field_name] and new_value in bot_dict["allOf"]["intent"]:
            bot_dict[field_name].append(new_value)

        elif new_value not in bot_dict[field_name] and new_value not in bot_dict["allOf"]["intent"]:
            return {'status': 400, 'message': "Something want wrong didnt Patch successfully"}

        with open(path, "w") as jsonFile:
            json.dump(bot_dict, jsonFile)

        return {'status': 200, 'message': "Patch successfully"}
    except:
        return {'status': 400, 'message': "Something want wrong didnt Patch successfully"}


def update_bot_is_basic_authentication(bot, field_name, new_value, certificate=''):
    try:
        path = bot + '.json'
        with open(path, "r") as jsonFile:
            bot_dict = json.load(jsonFile)
        if new_value == "True":
            bot_dict[field_name] = True
            bot_dict[certificate] = certificate
        if new_value == "False":
            bot_dict[field_name] = False
            bot_dict[certificate] = ''

        with open(path, "w") as jsonFile:
            json.dump(bot_dict, jsonFile)
        return {'status': 200, 'message': "Patch successfully"}
    except:
        return {'status': 400, 'message': "Something want wrong didnt Patch successfully"}


def update_in_bot(bot, field_name, new_value, sub_field_name_or_sub_value=''):
    if field_name == "functions":
        return update_in_func(bot=bot, field_name=field_name, func_name=sub_field_name_or_sub_value,
                              new_value=new_value)
    if field_name == "name":
        return update_bot_name(bot=bot, field_name=field_name, new_value=new_value)

    else:
        return {'status': 400, 'message': "Something want wrong didnt updated successfully"}


# ************************************** patch function **************************************
def patch_in_bot(bot, field_name, new_value, sub_field_name_or_sub_value=''):
    if field_name == "intent":
        return update_bot_intent(bot=bot, field_name=field_name, new_value=new_value)
    if bot == 'bot1' and field_name == "permissions_list":
        return update_bot_permissions_list(bot=bot, field_name=field_name, new_value=new_value)
    if bot == 'bot3' and field_name == "is_basic_authentication":
        return update_bot_is_basic_authentication(bot=bot, field_name=field_name, new_value=new_value,
                                                  certificate=sub_field_name_or_sub_value)
    else:
        return {'status': 400, 'message': "Something want wrong didnt updated successfully"}
