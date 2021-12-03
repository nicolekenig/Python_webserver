import pytest
import requests

BASE = 'http://127.0.0.1:5000/botHandler/'


# ------------------------------------------- sub tests for get -------------------------------------------
def test_get_function_valid(base_url, bot, func_name, expected_message, name='', password=0, certificate=''):
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
    assert resp.json() == {'status': 200, 'message': expected_message}


def test_get_function_not_valid(base_url, bot, func_name, name='', password=0, certificate=''):
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
    assert resp.json() == {'status': 401, 'message': "You dont have permission for this function"}


# ******************************************** get test ********************************************
def test_get():
    test_get_function_valid(base_url=BASE, bot="bot1", func_name="play_sound", expected_message="Playing Lalalala")
    test_get_function_not_valid(base_url=BASE, bot="bot2", func_name="play_sound")
    test_get_function_not_valid(base_url=BASE, bot="bot3", func_name="play_sound")

    test_get_function_not_valid(base_url=BASE, bot="bot1", func_name="default_welcome_message")
    test_get_function_valid(base_url=BASE, bot="bot2", func_name="default_welcome_message", expected_message="Hello")
    test_get_function_not_valid(base_url=BASE, bot="bot3", func_name="default_welcome_message")

    test_get_function_not_valid(base_url=BASE, bot="bot1", func_name="make_api_call")
    test_get_function_not_valid(base_url=BASE, bot="bot2", func_name="make_api_call")

    test_get_function_valid(base_url=BASE, bot="bot3", func_name="make_api_call",
                            expected_message="This is the make_api_call function", name="my_bot", password=46543)
    test_get_function_not_valid(base_url=BASE, bot="bot3", func_name="make_api_call", name="not_my_name",
                                password=46543)
    test_get_function_not_valid(base_url=BASE, bot="bot3", func_name="make_api_call", name="my_bot", password=1111)
    test_get_function_not_valid(base_url=BASE, bot="bot3", func_name="make_api_call", name="not_my_name", password=1111)
    # test_get_function_valid(BASE,"bot3","my_bot",46543,"my-certificate!")


# ------------------------------------------- sub tests for post -------------------------------------------
def test_post_new_function_valid(base_url, bot, func_name, default_value):
    url = base_url + bot
    new_func = {"func_name": func_name, "default_value": default_value}
    resp = requests.post(url, new_func)
    assert resp.json() == {'status': 201, 'message': "Function added successfully"}


def test_post_new_function_not_valid(base_url, bot, func_name, default_value):
    url = base_url + bot
    new_func = {"func_name": func_name, "default_value": default_value}
    resp = requests.post(url, new_func)
    assert resp.json() == {'status': 409, 'message': "Function already exist in the bot"}


# ******************************************** post test ********************************************
def test_post():
    test_post_new_function_valid(base_url=BASE, bot="bot1", func_name="drink", default_value="water")
    test_post_new_function_not_valid(base_url=BASE, bot="bot1", func_name="drink", default_value="water")


# ------------------------------------------- sub tests for put -------------------------------------------
def test_put_new_valid(base_url, bot, field_name, new_value, sub_field_name_or_sub_value='',name='',password=0,certificate=''):
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
    assert resp.json() == {'status': 200, 'message': "Updated successfully"}


def test_put_new_not_valid(base_url, bot, field_name, new_value, sub_field_name_or_sub_value='',name='',password=0,certificate=''):
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
    assert resp.json() == {'status': 400, 'message': "Something want wrong didnt updated successfully"}


# ******************************************** put test ********************************************
def test_put():
    test_put_new_valid(base_url=BASE, bot="bot1", field_name="functions", new_value="Bom bom bom", sub_field_name_or_sub_value="play_sound")
    test_put_new_valid(base_url=BASE, bot="bot2", field_name="functions", new_value="Hi, this is my new welcome massage", sub_field_name_or_sub_value="default_welcome_message")
    test_put_new_not_valid(base_url=BASE, bot="bot1", field_name="functions", new_value="Hi, this is my new welcome massage", sub_field_name_or_sub_value="Not_bot1_func")
    test_put_new_not_valid(base_url=BASE, bot="bot2", field_name="functions", new_value="Bom bom bom", sub_field_name_or_sub_value="Not_bot2_func")
    test_put_new_not_valid(base_url=BASE, bot="bot3", field_name="functions", new_value="Bom bom bom", sub_field_name_or_sub_value="Not_bot3_func")


# ------------------------------------------- sub tests for patch -------------------------------------------
def test_patch_new_valid(base_url, bot, field_name, new_value, sub_field_name_or_sub_value='',name='',password=0,certificate=''):
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
    assert resp.json() == {'status': 200, 'message': "Patch successfully"}


def test_patch_new_not_valid(base_url, bot, field_name, new_value, sub_field_name_or_sub_value='', name='',password=0,certificate=''):
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
    assert resp.json() == {'status': 400, 'message': "Something want wrong didnt patch successfully"}


# ******************************************** patch test ********************************************
def test_patch():
    test_patch_new_valid(base_url=BASE, bot="bot1", field_name="intent", new_value="play_sound")
    test_patch_new_valid(base_url=BASE, bot="bot2", field_name="intent",new_value="default_welcome_message")
    test_patch_new_valid(base_url=BASE, bot="bot3", field_name="intent",new_value="make_api_call",name="my_bot", password=46543)

    test_patch_new_valid(base_url=BASE, bot="bot1", field_name="intent", new_value="play_sound")
    test_patch_new_valid(base_url=BASE, bot="bot2", field_name="intent",new_value="default_welcome_message")
    test_patch_new_valid(base_url=BASE, bot="bot3", field_name="intent",new_value="make_api_call", name="my_bot", password=46543)

    test_patch_new_not_valid(base_url=BASE, bot="bot1", field_name="intent", new_value="default_welcome_message")
    test_patch_new_not_valid(base_url=BASE, bot="bot2", field_name="intent",new_value="play_sound")
    test_patch_new_not_valid(base_url=BASE, bot="bot3", field_name="intent",new_value="make_api_call")
    test_patch_new_not_valid(base_url=BASE, bot="bot3", field_name="intent",new_value="make_api_call",name="not_my_name", password=46543)
    test_patch_new_not_valid(base_url=BASE, bot="bot3", field_name="intent",new_value="make_api_call",name="my_bot", password=111)
    test_patch_new_not_valid(base_url=BASE, bot="bot3", field_name="intent",new_value="make_api_call",name="not_my_name", password=111)


# ------------------------------------------- sub tests for delete -------------------------------------------
def test_delete_valid(delete_url, bot):
    url = delete_url + bot
    resp = requests.delete(url)
    assert resp.json() == {'status': 204, 'message': 'Bot deleted successfully'}


def test_delete_not_valid(delete_url, bot):
    url = delete_url + bot
    resp = requests.delete(url)
    assert resp.json() == {'status': 404, 'message': 'File dose not exist or could not deleted bot'}


# ******************************************** delete test ********************************************
def test_delete():
    test_delete_valid(delete_url=BASE, bot="bot1")
    test_delete_valid(delete_url=BASE, bot="bot2")
    test_delete_valid(delete_url=BASE, bot="bot3")
    test_delete_valid(delete_url=BASE, bot="logic")
    test_delete_not_valid(delete_url=BASE, bot="bot1")
    test_delete_not_valid(delete_url=BASE, bot="bot2")
    test_delete_not_valid(delete_url=BASE, bot="bot3")
    test_delete_not_valid(delete_url=BASE, bot="logic")
