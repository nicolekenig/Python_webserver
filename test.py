import pytest
import requests

BASE = 'http://127.0.0.1:5000/botHandler/'


# ------------------------------------------- get test -------------------------------------------
@pytest.mark.parametrize("url, data_for_get, expected_result", [
    (BASE + "bot1", {"func_name": "play_sound"}, {'status': 200, 'message': "Lalalala"}),
    (BASE + "bot2", {"func_name": "default_welcome_message"}, {'status': 200, 'message': "Hello (default message)"}),
    (BASE + "bot3", {"func_name": "make_api_call", "name": "my_bot", "password": 46543},
     {'status': 200, 'message': "making an api call"}),

    (BASE + "bot1", {"func_name": "default_welcome_message"},
     {'status': 401, 'message': "You dont have permission for this function"}),
    (BASE + "bot2", {"func_name": "play_sound"},
     {'status': 401, 'message': "You dont have permission for this function"}),
    (BASE + "bot3", {"func_name": "default_welcome_message"},
     {'status': 401, 'message': "You dont have permission for this function"}),

    (BASE + "bot1", {"func_name": "make_api_call"},
     {'status': 401, 'message': "You dont have permission for this function"}),
    (BASE + "bot2", {"func_name": "make_api_call"},
     {'status': 401, 'message': "You dont have permission for this function"}),
    (BASE + "bot3", {"func_name": "play_sound"},
     {'status': 401, 'message': "You dont have permission for this function"}),

    (BASE + "bot3", {"func_name": "make_api_call", "name": "not_my_name", "password": 46543},
     {'status': 401, 'message': "You dont have permission for this function"}),
    (BASE + "bot3", {"func_name": "make_api_call", "name": "my_bot", "password": 1111},
     {'status': 401, 'message': "You dont have permission for this function"}),
    (BASE + "bot3", {"func_name": "make_api_call", "name": "not_my_name", "password": 1111},
     {'status': 401, 'message': "You dont have permission for this function"}),

    (BASE + "bot4", {"func_name": "default_welcome_message"}, {'status': 401, 'message': "You dont have permission for this function"}),

])
def test_get(url, data_for_get, expected_result):
    resp = requests.get(url, data_for_get)
    assert resp.json() == expected_result


# ------------------------------------------- post test -------------------------------------------
@pytest.mark.parametrize("url, data_for_post, expected_result", [
    (BASE + "bot1", {"func_name": "drink", "default_value": "water"},
     {'status': 201, 'message': "Function added successfully"}),
    (BASE + "bot2", {"func_name": "play_movie", "default_value": "Harry Potter"},
     {'status': 201, 'message': "Function added successfully"}),
    (BASE + "bot3",
     {"func_name": "next_meeting_location", "default_value": "New York", "name": "my_bot", "password": 46543},
     {'status': 201, 'message': "Function added successfully"}),

    (BASE + "bot1", {"func_name": "drink", "default_value": "water"},
     {'status': 400, 'message': "Something want wrong didnt post successfully"}),
    (BASE + "bot2", {"func_name": "default_welcome_message", "default_value": "new message"},
     {'status': 400, 'message': "Something want wrong didnt post successfully"}),
    (BASE + "bot3",
     {"func_name": "next_meeting_location", "default_value": "Loa Angeles", "name": "my_bot", "password": 46543},
     {'status': 400, 'message': "Something want wrong didnt post successfully"}),

    (BASE + "bot3",
     {"func_name": "next_meeting_location", "default_value": "New York", "name": "not_my_bot", "password": 46543},
     {'status': 400, 'message': "Something want wrong didnt post successfully"}),
    (BASE + "bot3",
     {"func_name": "next_meeting_location", "default_value": "New York", "name": "my_bot", "password": 1111},
     {'status': 400, 'message': "Something want wrong didnt post successfully"}),
    (BASE + "bot3",
     {"func_name": "next_meeting_location", "default_value": "Loa Angeles", "name": "not_my_bot", "password": 1111},
     {'status': 400, 'message': "Something want wrong didnt post successfully"}),

    (BASE + "bot4", {"func_name": "drink", "default_value": "water"},
        {'status': 400, 'message': "Something want wrong didnt post successfully"}),
])
def test_post(url, data_for_post, expected_result):
    resp = requests.post(url, data_for_post)
    assert resp.json() == expected_result


# ------------------------------------------- put test -------------------------------------------
@pytest.mark.parametrize("url, data_for_put, expected_result", [
    (BASE + "bot1",
    {"field_name": "functions", "new_value": "Bom bom bom", "sub_field_name_or_sub_value": "play_sound"},
    {'status': 200, 'message': "Updated successfully"}),
    (BASE + "bot2", {"field_name": "functions", "new_value": "Hi, this is my new welcome massage",
                     "sub_field_name_or_sub_value": "default_welcome_message"},
     {'status': 200, 'message': "Updated successfully"}),

    (BASE + "bot1", {"field_name": "name", "new_value": "my_bot1"}, {'status': 200, 'message': "Updated successfully"}),
    (BASE + "bot2", {"field_name": "name", "new_value": "my_bot2"}, {'status': 200, 'message': "Updated successfully"}),
    (BASE + "bot3", {"field_name": "name", "new_value": "my_bot3", "name": "my_bot", "password": 46543},
     {'status': 200, 'message': "Updated successfully"}),

    (BASE + "bot1", {"field_name": "functions", "new_value": "Hi, this is my new welcome massage",
                     "sub_field_name_or_sub_value": "default_welcome_message"},
     {'status': 400, 'message': "Something want wrong didnt updated successfully"}),
    (
            BASE + "bot2",
            {"field_name": "functions", "new_value": "Bom Bom Bom", "sub_field_name_or_sub_value": "play_sound"},
            {'status': 400, 'message': "Something want wrong didnt updated successfully"}),
    (BASE + "bot3", {"field_name": "functions", "new_value": "play_sound", "sub_field_name_or_sub_value": "play_sound",
                     "name": "my_bot3", "password": 46543},
     {'status': 400, 'message': "Something want wrong didnt updated successfully"}),

    (BASE + "bot4", {"field_name": "functions", "new_value": "Hi, this is my new welcome massage",
                     "sub_field_name_or_sub_value": "default_welcome_message"},
     {'status': 400, 'message': "Something want wrong didnt updated successfully"}),
])
def test_put(url, data_for_put, expected_result):
    resp = requests.put(url, data_for_put)
    assert resp.json() == expected_result


# ------------------------------------------- patch test -------------------------------------------
@pytest.mark.parametrize("url, data_for_patch, expected_result", [
    (BASE + "bot1", {"field_name": "intent", "new_value": "play_sound"},
     {'status': 200, 'message': "Patch successfully"}),
    (BASE + "bot2", {"field_name": "intent", "new_value": "default_welcome_message"},
     {'status': 200, 'message': "Patch successfully"}),
    (BASE + "bot3", {"field_name": "intent", "new_value": "make_api_call", "name": "my_bot3", "password": 46543},
     {'status': 200, 'message': "Patch successfully"}),

    (BASE + "bot1", {"field_name": "intent", "new_value": "play_sound"},
     {'status': 200, 'message': "Patch successfully"}),
    (BASE + "bot2", {"field_name": "intent", "new_value": "default_welcome_message"},
     {'status': 200, 'message': "Patch successfully"}),
    (BASE + "bot3", {"field_name": "intent", "new_value": "make_api_call", "name": "my_bot3", "password": 46543},
     {'status': 200, 'message': "Patch successfully"}),

    (BASE + "bot1", {"field_name": "intent", "new_value": "default_welcome_message"},
     {'status': 400, 'message': "Something want wrong didnt patch successfully"}),
    (BASE + "bot2", {"field_name": "intent", "new_value": "play_sound"},
     {'status': 400, 'message': "Something want wrong didnt patch successfully"}),
    (BASE + "bot3", {"field_name": "intent", "new_value": "make_api_call"},
     {'status': 400, 'message': "Something want wrong didnt patch successfully"}),

    (BASE + "bot3", {"field_name": "intent", "new_value": "make_api_call", "name": "not_my_bot", "password": 46543},
     {'status': 400, 'message': "Something want wrong didnt patch successfully"}),
    (BASE + "bot3", {"field_name": "intent", "new_value": "make_api_call", "name": "my_bot3", "password": 1111},
     {'status': 400, 'message': "Something want wrong didnt patch successfully"}),
    (BASE + "bot3", {"field_name": "intent", "new_value": "make_api_call", "name": "not_my_bot", "password": 1111},
     {'status': 400, 'message': "Something want wrong didnt patch successfully"}),

    (BASE + "bot3",
     {"field_name": "is_basic_authentication", "new_value": "False", "name": "my_bot3", "password": 46543},
     {'status': 200, 'message': "Patch successfully"}),
    (BASE + "bot3",
     {"field_name": "is_basic_authentication", "new_value": "False", "name": "my_bot3", "password": 11111},
     {'status': 400, 'message': "Something want wrong didnt patch successfully"}),

    (BASE + "bot4", {"field_name": "intent", "new_value": "default_welcome_message"},
     {'status': 400, 'message': "Something want wrong didnt patch successfully"}),

])
def test_patch(url, data_for_patch, expected_result):
    resp = requests.patch(url, data_for_patch)
    assert resp.json() == expected_result


# ------------------------------------------- bot3 complex test -------------------------------------------
@pytest.mark.parametrize("url, data_for_put_bot3_complex_test, expected_result", [
    (BASE + "bot3", {"field_name": "name", "new_value": "my_bot", "name": "my_bot3_new_name", "password": 46543,
                     "certificate": "my-certificate!"}, {'status': 200, 'message': "Updated successfully"}),

    (BASE + "bot3", {"field_name": "functions", "new_value": "Bom bom bom", "sub_field_name_or_sub_value": "play_sound",
                     "name": "my_bot3_new_name", "password": 46543, "certificate": "my-certificate!"},
     {'status': 400, 'message': "Something want wrong didnt updated successfully"}),
])
def test_put_bot3_not_basic_auth(url, data_for_put_bot3_complex_test, expected_result):
    resp = requests.put(url, data_for_put_bot3_complex_test)
    assert resp.json() == expected_result


@pytest.mark.parametrize("url, data_for_get_bot3_complex_test, expected_result", [
    (BASE + "bot3",
     {"func_name": "make_api_call", "name": "my_bot", "password": 46543, "certificate": "my-certificate!"},
     {'status': 200, 'message': "making an api call"}),
    (BASE + "bot3", {"func_name": "play_sound", "name": "my_bot", "password": 46543, "certificate": "my-certificate!"},
     {'status': 401, 'message': "You dont have permission for this function"}),
])
def test_get_bot3_not_basic_auth(url, data_for_get_bot3_complex_test, expected_result):
    resp = requests.get(url, data_for_get_bot3_complex_test)
    assert resp.json() == expected_result


@pytest.mark.parametrize("url, data_for_post_bot3_complex_test, expected_result", [
    (BASE + "bot3",
     {"func_name": "drink", "default_value": "cofe", "name": "my_bot", "password": 46543,
      "certificate": "my-certificate!"},
     {'status': 201, 'message': "Function added successfully"}),

    (BASE + "bot3",
     {"func_name": "next_meeting_location", "default_value": "Loa Angeles", "name": "my_bot3_new_name",
      "password": 46543,
      "certificate": "my-certificate!"},
     {'status': 400, 'message': "Something want wrong didnt post successfully"}),

    (BASE + "bot3",
     {"func_name": "next_meeting_location", "default_value": "Loa Angeles", "name": "my_bot3_new_name",
      "password": 46543,
      "certificate": "not_my-certificate!"},
     {'status': 400, 'message': "Something want wrong didnt post successfully"}),

    (BASE + "bot3",
     {"func_name": "next_meeting_location", "default_value": "Loa Angeles"},
     {'status': 400, 'message': "Something want wrong didnt post successfully"}),
])
def test_post_bot3_not_basic_auth(url, data_for_post_bot3_complex_test, expected_result):
    resp = requests.post(url, data_for_post_bot3_complex_test)
    assert resp.json() == expected_result


# ------------------------------------------- delete test -------------------------------------------
@pytest.mark.parametrize("url, expected_result", [
    (BASE + "bot1", {'status': 204, 'message': 'Bot deleted successfully'}),
    (BASE + "bot2", {'status': 204, 'message': 'Bot deleted successfully'}),
    (BASE + "bot3", {'status': 204, 'message': 'Bot deleted successfully'}),

    (BASE + "bot1", {'status': 404, 'message': 'File dose not exist or could not deleted bot'}),
    (BASE + "bot2", {'status': 404, 'message': 'File dose not exist or could not deleted bot'}),
    (BASE + "bot3", {'status': 404, 'message': 'File dose not exist or could not deleted bot'}),
])
def test_delete(url, expected_result):
    resp = requests.delete(url)
    assert resp.json() == expected_result


if __name__ == '__main__':
    test_get()
    test_post()
    test_put()
    test_patch()
    test_put_bot3_not_basic_auth()
    test_get_bot3_not_basic_auth()
    test_post_bot3_not_basic_auth()
    test_delete()
