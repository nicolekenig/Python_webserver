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
class TestGet:
    def test1_get(self):
        ans = get_function(base_url=BASE, bot="bot1", func_name="play_sound")
        assert ans == {'status': 200, 'message': "Playing Lalalala"}

    def test2_get(self):
        ans = get_function(base_url=BASE, bot="bot2", func_name="play_sound")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test3_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="play_sound")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test4_get(self):
        ans = get_function(base_url=BASE, bot="bot1", func_name="default_welcome_message")
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test5_get(self):
        ans = get_function(base_url=BASE, bot="bot2", func_name="default_welcome_message")
        assert ans == {'status': 200, 'message': "Hello"}

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
        ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="my_bot", password=46543)
        assert ans == {'status': 200, 'message': "This is the make_api_call function"}

    def test10_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="not_my_name", password=46543)
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test11_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="my_bot", password=1111)
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    def test12_get(self):
        ans = get_function(base_url=BASE, bot="bot3", func_name="make_api_call", name="not_my_name", password=1111)
        assert ans == {'status': 401, 'message': "You dont have permission for this function"}

    # def test13_get(self):
        # ans= test_get_function_valid(BASE,"bot3","my_bot",46543,"my-certificate!")
        # assert ans == {'status': 200, 'message': "Playing Lalalala"}


# ******************************************** post test ********************************************
class TestPost:
    def test1_post(self):
        ans = post_new_function(base_url=BASE, bot="bot1", func_name="drink", default_value="water")
        assert ans == {'status': 201, 'message': "Function added successfully"}

    def test2_post(self):
        ans = post_new_function(base_url=BASE, bot="bot1", func_name="drink", default_value="water")
        assert ans == {'status': 409, 'message': "Function already exist in the bot"}


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
        ans = put_new_value(base_url=BASE, bot="bot1", field_name="functions",
                            new_value="Hi, this is my new welcome massage", sub_field_name_or_sub_value="Not_bot1_func")
        assert ans == {'status': 400, 'message': "Something want wrong didnt updated successfully"}

    def test4_put(self):
        ans = put_new_value(base_url=BASE, bot="bot2", field_name="functions", new_value="Bom bom bom",
                            sub_field_name_or_sub_value="Not_bot2_func")
        assert ans == {'status': 400, 'message': "Something want wrong didnt updated successfully"}

    def test5_put(self):
        ans = put_new_value(base_url=BASE, bot="bot3", field_name="functions", new_value="Bom bom bom",
                            sub_field_name_or_sub_value="Not_bot3_func")
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
        ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call", name="my_bot",
                              password=46543)
        assert ans == {'status': 200, 'message': "Patch successfully"}

    def test4_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot1", field_name="intent", new_value="play_sound")
        assert ans == {'status': 200, 'message': "Patch successfully"}

    def test5_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot2", field_name="intent", new_value="default_welcome_message")
        assert ans == {'status': 200, 'message': "Patch successfully"}

    def test6_patch(self):
        ans = patch_new_value(base_url=BASE, bot="bot3", field_name="intent", new_value="make_api_call", name="my_bot",
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


if __name__ == "__main__":
    TestGet()
    TestPost()
    TestPut()
    TestPatch()
    TestDelete()