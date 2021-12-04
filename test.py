import pytest
import requests

import create_json_data

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
def post_new_function(base_url, bot, func_name, default_value, name='', password=0, certificate=''):
    url = base_url + bot
    if bot != "bot3":
        param = {
            "func_name": func_name,
            "default_value": default_value
        }
    else:
        param = {
            "func_name": func_name,
            "default_value": default_value,
            "name": name,
            "password": password,
            "certificate": certificate
        }
    resp = requests.post(url, param)
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
class TestGet:
    def test1_get(self):
        ans = get_function(base_url=BASE, bot="bot1", func_name="play_sound")
        assert ans == {'status': 200, 'message': "Lalalala"}

    def test2_get(self):
        ans = get_function(base_url=BASE, bot="bot2", func_name="default_welcome_message")
        assert ans == {'status': 200, 'message': "Hello (default message)"}

    def test3_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="my_bot", password=46543)
        assert ans == {'status': 200, 'message': "making an api call"}

    def test4_get(self):
        ans = get_function(base_url=BASE, bot="bot1", func_name="default_welcome_message")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test5_get(self):
        ans = get_function(base_url=BASE, bot="bot2", func_name="play_sound")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test6_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="default_welcome_message")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test7_get(self):
        ans = get_function(base_url=BASE, bot="bot1", func_name="make_api_call")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test8_get(self):
        ans = get_function(base_url=BASE, bot="bot2", func_name="make_api_call")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test9_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="play_sound")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test10_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="not_my_name", password=46543)
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test11_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="my_bot", password=1111)
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test12_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="not_my_name", password=1111)
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

# ******************************************** post test ********************************************
class TestPost:
    def test1_post(self):
        ans = post_new_function(base_url=BASE, bot="bot1", func_name="drink", default_value="water")
        assert ans == {'status': 201, 'message': "Function added successfully"}

    def test2_post(self):
        ans = post_new_function(base_url=BASE, bot="bot2", func_name="play_movie", default_value="Harry Potter")
        assert ans == {'status': 201, 'message': "Function added successfully"}

    def test3_post(self):
        ans = post_new_function(base_url=BASE, bot="bot3", func_name="next_meeting_location", default_value="New York",
                                name='my_bot', password=46543)
        assert ans == {'status': 201, 'message': "Function added successfully"}

    def test4_post(self):
        ans = post_new_function(base_url=BASE, bot="bot1", func_name="drink", default_value="water")
        assert ans == {'status': 400, 'message': "Something want wrong didnt post successfully"}

    def test5_post(self):
        ans = post_new_function(base_url=BASE, bot="bot2", func_name="default_welcome_message",
                                default_value="new message")
        assert ans == {'status': 400, 'message': "Something want wrong didnt post successfully"}

    def test6_post(self):
        ans = post_new_function(base_url=BASE, bot="bot3", func_name="next_meeting_location",
                                default_value="Los Angeles")
        assert ans == {'status': 400, 'message': "Something want wrong didnt post successfully"}


# ******************************************** put test ********************************************
class TestPut:
    def test1_put(self):
        ans = put_new_value(base_url=BASE, bot="bot1", field_name="functions", new_value="Bom bom bom",
                            sub_field_name_or_sub_value="play_sound")
        assert ans == {'status': 200, 'message': "Updated successfully"}

    def test2_put(self):
        ans = put_new_value(base_url=BASE, bot="bot2", field_name="functions",
                            new_value="Hi, this is my new welcome massage",
                            sub_field_name_or_sub_value="default_welcome_message")
        assert ans == {'status': 200, 'message': "Updated successfully"}

    def test3_put(self):
        ans = put_new_value(base_url=BASE, bot="bot1", field_name="name", new_value="my_bot1")
        assert ans == {'status': 200, 'message': "Updated successfully"}

    def test4_put(self):
        ans = put_new_value(base_url=BASE, bot="bot2", field_name="name", new_value="my_bot2")
        assert ans == {'status': 200, 'message': "Updated successfully"}

    def test5_put(self):
        ans = put_new_value(base_url=BASE, bot="bot3", field_name="name", new_value="my_bot3", name='my_bot', password=46543)
        assert ans == {'status': 200, 'message': "Updated successfully"}

    def test6_put(self):
        ans = put_new_value(base_url=BASE, bot="bot1", field_name="functions",
                            new_value="Hi, this is my new welcome massage", sub_field_name_or_sub_value="Not_bot1_func")
        assert ans == {'status': 400, 'message': "Something want wrong didnt updated successfully"}

    def test7_put(self):
        ans = put_new_value(base_url=BASE, bot="bot2", field_name="functions", new_value="Bom bom bom",
                            sub_field_name_or_sub_value="Not_bot2_func")
        assert ans == {'status': 400, 'message': "Something want wrong didnt updated successfully"}

    def test8_put(self):
        ans = put_new_value(base_url=BASE, bot="bot3", field_name="functions", new_value="Bom bom bom",
                            sub_field_name_or_sub_value="Not_bot3_func", name='my_bot3', password=46543)
        assert ans == {'status': 400, 'message': "Something want wrong didnt updated successfully"}


# ******************************************** patch test ********************************************
class TestPatch:
    def test1_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot1", field_name="intent", new_value="play_sound")
        assert ans == {'status': 200, 'message': "Patch successfully"}

    def test2_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot2", field_name="intent", new_value="default_welcome_message")
        assert ans == {'status': 200, 'message': "Patch successfully"}

    def test3_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call", name="my_bot3",
                              password=46543)
        assert ans == {'status': 200, 'message': "Patch successfully"}

    def test4_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot1", field_name="intent", new_value="play_sound")
        assert ans == {'status': 200, 'message': "Patch successfully"}

    def test5_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot2", field_name="intent", new_value="default_welcome_message")
        assert ans == {'status': 200, 'message': "Patch successfully"}

    def test6_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call", name="my_bot3",
                              password=46543)
        assert ans == {'status': 200, 'message': "Patch successfully"}

    def test7_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot1", field_name="intent", new_value="default_welcome_message")
        assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}

    def test8_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot2", field_name="intent", new_value="play_sound")
        assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}

    def test9_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call")
        assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}

    def test10_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call",
                              name="not_my_name", password=46543)
        assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}

    def test11_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call", name="my_bot",
                              password=111)
        assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}

    def test12_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call",
                              name="not_my_name", password=111)
        assert ans == {'status': 400, 'message': "Something want wrong didnt patch successfully"}


# ******************************************** delete test ********************************************
class TestDelete:
    def test1_delete(self):
        ans = delete_json(delete_url=BASE, bot="bot1")
        assert ans == {'status': 204, 'message': 'Bot deleted successfully'}

    def test2_delete(self):
        ans = delete_json(delete_url=BASE, bot="bot2")
        assert ans == {'status': 204, 'message': 'Bot deleted successfully'}

    def test3_delete(self):
        ans = delete_json(delete_url=BASE, bot="bot3")
        assert ans == {'status': 204, 'message': 'Bot deleted successfully'}

    def test4_delete(self):
        ans = delete_json(delete_url=BASE, bot="logic")
        assert ans == {'status': 204, 'message': 'Bot deleted successfully'}

    def test5_delete(self):
        ans = delete_json(delete_url=BASE, bot="bot1")
        assert ans == {'status': 404, 'message': 'File dose not exist or could not deleted bot'}

    def test6_delete(self):
        ans = delete_json(delete_url=BASE, bot="bot2")
        assert ans == {'status': 404, 'message': 'File dose not exist or could not deleted bot'}

    def test7_delete(self):
        ans = delete_json(delete_url=BASE, bot="bot3")
        assert ans == {'status': 404, 'message': 'File dose not exist or could not deleted bot'}

    def test8_delete(self):
        ans = delete_json(delete_url=BASE, bot="logic")
        assert ans == {'status': 404, 'message': 'File dose not exist or could not deleted bot'}


# ******************************************** complex test ********************************************
class TestComplexCases:
    def test1_bot3_not_basic_auth(self):
        create_json_data.run()
        ans = patch_new_value(base_url=BASE, bot="bot3", field_name="is_basic_authentication", new_value="False", name="my_bot",
                              password=46543)
        assert ans == {'status': 200, 'message': "Patch successfully"}

        ans = put_new_value(base_url=BASE, bot="bot3", field_name="name", new_value="my_bot3", name='my_bot', password=46543,certificate="my-certificate!")
        assert ans == {'status': 200, 'message': "Updated successfully"}

        ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="my_bot3", password=46543, certificate="my-certificate!")
        assert ans == {'status': 200, 'message': "making an api call"}

        ans = get_function(base_url=BASE, bot="bot3", func_name="play_sound", name="my_bot3", password=46543, certificate="my-certificate!")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

        ans = post_new_function(base_url=BASE, bot="bot3", func_name="next_meeting_location", default_value="New York",
                                name='my_bot3', password=46543, certificate="my-certificate!")
        assert ans == {'status': 201, 'message': "Function added successfully"}

        ans = post_new_function(base_url=BASE, bot="bot3", func_name="next_meeting_location",
                                default_value="Los Angeles")
        assert ans == {'status': 400, 'message': "Something want wrong didnt post successfully"}

        ans = put_new_value(base_url=BASE, bot="bot3", field_name="functions", new_value="Bom bom bom",
                            sub_field_name_or_sub_value="Not_bot3_func",name="my_bot3", password=46543, certificate="my-certificate!")
        assert ans == {'status': 400, 'message': "Something want wrong didnt updated successfully"}


if __name__ == "__main__":
    TestGet()
    TestPost()
    TestPut()
    TestPatch()
    TestDelete()
    TestComplexCases()
