import json
import os
import auth


# ************************************** get function **************************************
def do_the_function(bot_type, func_name):
    """
    This function responds to a GET request for function, after checking all the needed authentication
    :param bot_type: (string) bot1/ bot2/ bot3
    :param func_name: (string) the function name that the bot want
    :return: the respond status and the value of the function: (dictionary) {status: 200, message: value of the function}
    """
    f = open(bot_type + '.json')
    bot_dict = json.load(f)
    return {'status': 200, 'message': bot_dict["functions"][func_name]}


# ************************************** put and patch function **************************************
def update_in_func(bot, field_name, func_name, new_value):
    """
    update the function returned value
    :param bot: (string) bot1/ bot2/ bot3
    :param field_name: (string) what the bot want to update- function
    :param func_name: (string) the function name
    :param new_value: (string) the new value
    :return: the respond status and message: (dictionary) {status: 200/400, message: message}
    """
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
    """
    update the bot name
    :param bot: (string) bot1/ bot2/ bot3
    :param field_name: (string) -name
    :param new_value: (string) the new name of the bot
    :return: the respond status and message: (dictionary) {status: 200/400, message: message}
    """
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


def update_bot_intent(bot, field_name, func_name):
    """
    update in the bot intent:
    if the function exists on the intent, it deleted.
    if the function doesn't exists on the intent, it added.
    :param bot: (string) bot1/ bot2/ bot3
    :param field_name: (string) intent
    :param func_name: (string) the function name
    :return: the respond status and message: (dictionary) {status:200/400, message:message}
    """
    try:
        is_exists = auth.check_if_func_exists(bot_type=bot, func=func_name)
        if is_exists:
            path = bot + '.json'
            with open(path, "r") as jsonFile:
                bot_dict = json.load(jsonFile)

            if func_name in bot_dict["allOf"][field_name]:
                bot_dict["allOf"][field_name].remove(func_name)

            else:
                bot_dict["allOf"][field_name].append(func_name)

            with open(path, "w") as jsonFile:
                json.dump(bot_dict, jsonFile)

            return {'status': 200, 'message': "Patch successfully"}
        else:
            return {'status': 400, 'message': "Something want wrong didnt patch successfully"}
    except:
        return {'status': 400, 'message': "Something want wrong didnt patch successfully"}


def update_bot_permissions_list(bot, field_name, func_name):
    """
    update bot1 permissions
    if the function exists on the permission list, it deleted
    if the function doesn't exists on the permission list, it added only if it exists in the bot intent
    :param bot: (string) bot1
    :param field_name: (string) permissions_list
    :param func_name: (string) the function name
    :return: the respond status and message: (dictionary) {status:200/400, message:message}
    """
    try:
        path = bot + '.json'
        with open(path, "r") as jsonFile:
            bot_dict = json.load(jsonFile)

        if func_name in bot_dict[field_name]:
            bot_dict[field_name].remove(func_name)

        elif func_name not in bot_dict[field_name] and func_name in bot_dict["allOf"]["intent"]:
            bot_dict[field_name].append(func_name)

        elif func_name not in bot_dict["allOf"]["intent"]:
            return {'status': 400, 'message': "Something want wrong didnt patch successfully"}

        with open(path, "w") as jsonFile:
            json.dump(bot_dict, jsonFile)

        return {'status': 200, 'message': "Patch successfully"}
    except:
        return {'status': 400, 'message': "Something want wrong didnt patch successfully"}


def update_bot_is_basic_authentication(bot, field_name, new_value, certificate=''):
    """
    change bot3 authentication
    if bot3 authentication is basic, it change to not basic
    if bot3 authentication is not basic, it change to basic
    :param bot: (string) bot3
    :param field_name: (string) is_basic_authentication
    :param new_value:(string)  "Ture"/"False"
    :param certificate: (string) in case that the bot authentication isn't basic- authentication
    :return: the respond status and message: (dictionary) {status:200/400, message:message}
    """
    try:
        path = bot + '.json'
        with open(path, "r") as jsonFile:
            bot_dict = json.load(jsonFile)
        if new_value == "True":
            bot_dict[field_name] = True
            bot_dict[certificate] = ''
        if new_value == "False":
            bot_dict[field_name] = False
            bot_dict[certificate] = certificate

        with open(path, "w") as jsonFile:
            json.dump(bot_dict, jsonFile)
        return {'status': 200, 'message': "Patch successfully"}
    except:
        return {'status': 400, 'message': "Something want wrong didnt patch successfully"}


def update_in_bot(bot, field_name, new_value, sub_field_name_or_sub_value=''):
    """
    respond to a PUT request, and make an update according to the bot request
    :param bot: bot1/ bot2/ bot3
    :param field_name: (string) that the bot want to update- function/name
    :param new_value: (string) the return value of the function/ the new name of the bot
    :param sub_field_name_or_sub_value:(string)  in case of en function update- the function name
    :return: the respond update status and the value of the function: (dictionary) {status: 200/400, message: message}
    """
    if field_name == "functions":
        return update_in_func(bot=bot, field_name=field_name, func_name=sub_field_name_or_sub_value,
                              new_value=new_value)
    if field_name == "name":
        return update_bot_name(bot=bot, field_name=field_name, new_value=new_value)

    else:
        return {'status': 400, 'message': "Something want wrong didnt updated successfully"}


# ************************************** patch function **************************************
def patch_in_bot(bot, field_name, new_value, sub_field_name_or_sub_value=''):
    """
    respond to a Patch request, and make an update on the bot intent/permission/authentication:
    :param bot:  (string) bot1/ bot2/ bot3
    :param field_name: (string) that the bot want to update- intent/permission/authentication
    :param new_value: (string) the new value of the field
    :param sub_field_name_or_sub_value: (string) in case that bot3 want to add certificate, is the new certificate
    :return: the respond status and message: (dictionary) {status:200/400, message:message}
    """
    if field_name == "intent":
        return update_bot_intent(bot=bot, field_name=field_name, func_name=new_value)
    if bot == 'bot1' and field_name == "permissions_list":
        return update_bot_permissions_list(bot=bot, field_name=field_name, func_name=new_value)
    if bot == 'bot3' and field_name == "is_basic_authentication":
        return update_bot_is_basic_authentication(bot=bot, field_name=field_name, new_value=new_value,
                                                  certificate=sub_field_name_or_sub_value)
    else:
        return {'status': 400, 'message': "Something want wrong didnt patch successfully"}


# ************************************** delete bot function **************************************
def delete_bot(bot):
    """
    delete a bot
    :param bot: (string) bot1/ bot2/ bot3
    :return: delete status and message: (dictionary) { status: 204/204, message:message}
    """
    try:
        os.remove(bot + '.json')
        return {'status': 204, 'message': 'Bot deleted successfully'}

    except:
        return {'status': 404, 'message': 'File dose not exist or could not deleted bot'}