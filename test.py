import pytest
import requests

BASE = 'http://127.0.0.1:5000/botHandler/'


# ------------------------------------------- sub tests for get -------------------------------------------
def get_function(base_url, bot, func_name, name='', password=0, certificate=''):
    if func_name != "make_api_call":
        func_name = {
            "func_name": func_name
        }
    else:
        func_name = {
            "func_name": func_name,
            "name": name,
            "password": password,
            "certificate": certificate
        }
    url = base_url + bot
    resp = requests.get(url, func_name)
    return resp.json()


# ------------------------------------------- sub tests for post -------------------------------------------
def post_new_function(base_url, bot, func_name, default_value):
    url = base_url + bot
    new_func = {"func_name": func_name, "default_value": default_value}
    resp = requests.post(url, new_func)
    return resp.json()


# ------------------------------------------- sub tests for put -------------------------------------------
def put_new_value(base_url, bot, field_name, new_value, sub_field_name_or_sub_value='', name='', password=0,
                  certificate=''):
    url = base_url + bot
    if bot != "bot3":
        put_details = {
            "field_name": field_name,
            "new_value": new_value,
            "sub_field_name_or_sub_value": sub_field_name_or_sub_value,
        }
    else:
        put_details = {
            "field_name": field_name,
            "new_value": new_value,
            "sub_field_name_or_sub_value": sub_field_name_or_sub_value,
            "name": name,
            "password": password,
            "certificate": certificate
        }
    resp = requests.put(url, put_details)
    return resp.json()


# ------------------------------------------- sub tests for patch -------------------------------------------
def patch_new_value(base_url, bot, field_name, new_value, sub_field_name_or_sub_value='', name='', password=0,
                    certificate=''):
    url = base_url + bot
    if bot != "bot3":
        patch_details = {
            "field_name": field_name,
            "new_value": new_value,
            "sub_field_name_or_sub_value": sub_field_name_or_sub_value
        }
    else:
        patch_details = {
            "field_name": field_name,
            "new_value": new_value,
            "sub_field_name_or_sub_value": sub_field_name_or_sub_value,
            "name": name,
            "password": password,
            "certificate": certificate
        }
    resp = requests.patch(url, patch_details)
    return resp.json()


# ------------------------------------------- sub tests for delete -------------------------------------------
def delete_json(delete_url, bot):
    url = delete_url + bot
    resp = requests.delete(url)
    return resp.json()


# ******************************************** get test ********************************************

def test_get():
    ans = get_function(base_url=BASE, bot="bot1", func_name="play_sound")
    assert ans == {'status': 200, 'message': "Playing Lalalala"}

    ans = get_function(base_url=BASE, bot="bot2", func_name="play_sound")
    assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    ans = get_function(base_url=BASE, bot="bot3", func_name="play_sound")
    assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    ans = get_function(base_url=BASE, bot="bot1", func_name="default_welcome_message")
    assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    ans = get_function(base_url=BASE, bot="bot2", func_name="default_welcome_message")
    assert ans == {'status': 200, 'message': "Hello"}

    ans = get_function(base_url=BASE, bot="bot3", func_name="default_welcome_message")
    assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    ans = get_function(base_url=BASE, bot="bot1", func_name="make_api_call")
    assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    ans = get_function(base_url=BASE, bot="bot2", func_name="make_api_call")
    assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="my_bot", password=46543)
    assert ans == {'status': 200, 'message': "This is the make_api_call function"}

    ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="not_my_name", password=46543)
    assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="my_bot", password=1111)
    assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="not_my_name", password=1111)
    assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    # ans= test_get_function_valid(BASE,"bot3","my_bot",46543,"my-certificate!")
    # assert ans == {'status': 200, 'message': "Playing Lalalala"}


# ******************************************** post test ********************************************
def test_post():
    ans = post_new_function(base_url=BASE, bot="bot1", func_name="drink", default_value="water")
    assert ans == {'status': 201, 'message': "Function added successfully"}

    ans = post_new_function(base_url=BASE, bot="bot1", func_name="drink", default_value="water")
    assert ans == {'status': 409, 'message': "Function already exist in the bot"}


# ******************************************** put test ********************************************
def test_put():
    ans = put_new_value(base_url=BASE, bot="bot1", field_name="functions", new_value="Bom bom bom",
                        sub_field_name_or_sub_value="play_sound")
    assert ans == {'status': 200, 'message': "Updated successfully"}

    ans = put_new_value(base_url=BASE, bot="bot2", field_name="functions",
                        new_value="Hi, this is my new welcome massage",
                        sub_field_name_or_sub_value="default_welcome_message")
    assert ans == {'status': 200, 'message': "Updated successfully"}

    ans = put_new_value(base_url=BASE, bot="bot1", field_name="functions",
                        new_value="Hi, this is my new welcome massage", sub_field_name_or_sub_value="Not_bot1_func")
    assert ans == {'status': 400, 'message': "Something want wrong didnt updated successfully"}

    ans = put_new_value(base_url=BASE, bot="bot2", field_name="functions", new_value="Bom bom bom",
                        sub_field_name_or_sub_value="Not_bot2_func")
    assert ans == {'status': 400, 'message': "Something want wrong didnt updated successfully"}

    ans = put_new_value(base_url=BASE, bot="bot3", field_name="functions", new_value="Bom bom bom",
                        sub_field_name_or_sub_value="Not_bot3_func")
    assert ans == {'status': 400, 'message': "Something want wrong didnt updated successfully"}


# ******************************************** patch test ********************************************
def test_patch():
    ans = patch_new_value(base_url=BASE, bot="bot1", field_name="intent", new_value="play_sound")
    assert ans == {'status': 200, 'message': "Patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot2", field_name="intent", new_value="default_welcome_message")
    assert ans == {'status': 200, 'message': "Patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call", name="my_bot",
                          password=46543)
    assert ans == {'status': 200, 'message': "Patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot1", field_name="intent", new_value="play_sound")
    assert ans == {'status': 200, 'message': "Patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot2", field_name="intent", new_value="default_welcome_message")
    assert ans == {'status': 200, 'message': "Patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call", name="my_bot",
                          password=46543)
    assert ans == {'status': 200, 'message': "Patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot1", field_name="intent", new_value="default_welcome_message")
    assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot2", field_name="intent", new_value="play_sound")
    assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call")
    assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call",
                          name="not_my_name", password=46543)
    assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}

    ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call", name="my_bot",
                          password=111)
    assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}
    ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call",
                          name="not_my_name", password=111)
    assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}


# ******************************************** delete test ********************************************
def test_delete():
    ans = delete_json(delete_url=BASE, bot="bot1")
    assert ans == {'status': 204, 'message': 'Bot deleted successfully'}

    ans = delete_json(delete_url=BASE, bot="bot2")
    assert ans == {'status': 204, 'message': 'Bot deleted successfully'}

    ans = delete_json(delete_url=BASE, bot="bot3")
    assert ans == {'status': 204, 'message': 'Bot deleted successfully'}

    ans = delete_json(delete_url=BASE, bot="logic")
    assert ans == {'status': 204, 'message': 'Bot deleted successfully'}

    ans = delete_json(delete_url=BASE, bot="bot1")
    assert ans == {'status': 404, 'message': 'File dose not exist or could not deleted bot'}

    ans = delete_json(delete_url=BASE, bot="bot2")
    assert ans == {'status': 404, 'message': 'File dose not exist or could not deleted bot'}

    ans = delete_json(delete_url=BASE, bot="bot3")
    assert ans == {'status': 404, 'message': 'File dose not exist or could not deleted bot'}

    ans = delete_json(delete_url=BASE, bot="logic")
    assert ans == {'status': 404, 'message': 'File dose not exist or could not deleted bot'}


