import json


# ************************************** authentication and checking functions **************************************
def is_authorized_in_intent(bot_type, func):
    """
    check if the function is in the bot intent
    :param bot_type: bot1/bot2/bot3
    :param func: the name of the function the bot want
    :return: True- the function is in the bot intent
            False - he function isn't in the bot intent
    """
    # get bot permissions_list
    f = open(bot_type + '.json')
    bot_dict = json.load(f)
    intent_list = bot_dict["allOf"]["intent"]
    return func in intent_list


def check_bot1_permissions(bot_type, func):
    """
    check if bot1 have permission to the function
    :param bot_type: bot1
    :param func: the name of the function the bot want
    :return: True- bot1 have permission to accesses the function
            False - bot1 dose not have permission to accesses the function
    """
    # get bot permissions_list
    f = open(bot_type + '.json')
    bot_dict = json.load(f)
    permissions_list = bot_dict["permissions_list"]
    return func in permissions_list


def check_bot3_authentication(bot_type, name, password, certificate):
    """
    check if the details that bot3 gave is correct
    :param bot_type: bot3
    :param name: the bot name
    :param password: the bot password
    :param certificate: the bot certificate
    :return: True - the details are correct
            False - the details are wrong
    """
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


def check_if_func_exists(bot_type, func):
    """
    check if the function exists in the bot functions before added a new one or before delete it
    :param bot_type: bot1- bot2/ bot3
    :param func: the name of the function
    :return: True - the function exists in the bot functions
            False - the function dont exists in the bot functions
    """
    # get bot permissions_list
    f = open(bot_type + '.json')
    bot_dict = json.load(f)
    functions_list = bot_dict["functions"]
    return func in functions_list
