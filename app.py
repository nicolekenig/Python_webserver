# import the Flask class from the flask module
from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, marshal_with, fields
import auth
import create_json_data
import utils
import create_task as ct

# create the application object
app = Flask(__name__, template_folder="templates")
# create the api using Flask
api = Api(app)

# get argument that pass in the get request param
get_arg = reqparse.RequestParser()
get_arg.add_argument("func_name", type=str, help="Name of the function is required", required=True)
get_arg.add_argument("name", type=str, help="bot name is required", required=False)
get_arg.add_argument("password", type=int, help="bot password is required", required=False)
get_arg.add_argument("certificate", type=str, help="bot certificate is required", required=False)

# post argument that pass in the post request param
post_arg = reqparse.RequestParser()
post_arg.add_argument("func_name", type=str, help="Name of the function is required", required=True)
post_arg.add_argument("default_value", type=str, help="Default value the function return is required",
                      required=True)

# put and patch argument that pass in the put or patch request param
put_and_patch_arg = reqparse.RequestParser()
put_and_patch_arg.add_argument("field_name", type=str, help="Field name is required", required=True)
put_and_patch_arg.add_argument("new_value", type=str, help="New value the function return is required",
                               required=True)
put_and_patch_arg.add_argument("sub_field_name_or_sub_value", type=str, help="Field name is required", required=False)
put_and_patch_arg.add_argument("name", type=str, help="bot name is required", required=False)
put_and_patch_arg.add_argument("password", type=int, help="bot password is required", required=False)
put_and_patch_arg.add_argument("certificate", type=str, help="bot certificate is required", required=False)

# format & return the value for the object to render
resource_fields = {
    'status': fields.Integer,
    'message': fields.String
}


class server(Resource):
    """
    A server class used to handle the http request from the user in the server side
    ...
    #Attributes
    ----------
    :param json_bot_list: list
        a list of all the bots json file
    #Methods
    ----------
    get(self, bot_type):
        handles all the get http request
    post(self, bot_type):
        handles all the post http request
    put(self, bot_type):
        handles all the put http request
    patch(self, bot_type):
        handles all the patch http request
    delete(self, bot_type):
        handles all the delete http request
    -------
    """

    json_bot_list = []

    def __init__(self, json_bot_list=['bot1.json', 'bot2.json', 'bot3.json']):
        """
        @:param json_bot_list: (list) a list of all the bots json file
        """
        self.json_bot_list = json_bot_list

    def before_first_request(self, bot_type, func_name='', args=None):
        bot_authorization = True

        if bot_type == 'bot1':
            bot_authorization = auth.check_bot1_permissions(bot_type=bot_type, func=func_name)

        elif bot_type == 'bot3':
            name = args.get("name")
            password = args.get("password")
            certificate = args.get("certificate")
            bot_authorization = auth.check_bot3_authentication(bot_type=bot_type, name=name, password=password,
                                                               certificate=certificate)

        return bot_authorization

    @marshal_with(resource_fields)
    def get(self, bot_type):
        """
        handles GET request: get what the function returns.
        The function name is received in the request param argument in a JSON form.
        :param bot_type: (string) bot1/ bot2/ bot3
        :return: resource_fields= (dictionary) {status: request status(200/401, message:message}
        """
        args = get_arg.parse_args()  # the params
        func_name = args.get("func_name")
        # check bot authorization
        bot_authorization = self.before_first_request(bot_type=bot_type, func_name=func_name, args=args)

        # check if function is in the bot intent
        is_authorized_in_intent = auth.is_authorized_in_intent(bot_type=bot_type, func=func_name)

        if (not is_authorized_in_intent) or (not bot_authorization):
            return {'status': 401, 'message': "You dont have permission for this function"}

        # else: is authorized in intent
        ans = utils.do_the_function(bot_type=bot_type, func_name=func_name)
        return ans

    @marshal_with(resource_fields)
    def post(self, bot_type):
        """
            handles POST request: add function to bot
            The function name and a default value to return from the new function is received in the request param argument
            in a JSON form.
            :param bot_type: (string) bot1/ bot2/ bot3
            :return: resource_fields= (dictionary) {status: request status(200/409, message:message}
        """
        args = post_arg.parse_args()  # the params
        ans = ct.create_function(func_name=args.get("func_name"), bot_permission=bot_type,
                                 default_value=args.get("default_value"))
        return ans

    @marshal_with(resource_fields)
    def put(self, bot_type):
        """
            handles PUT request: update a return value of a bot function
            The function name and new value to return from the function is received in the request param argument
            in a JSON form, and in case of bot3 also the bot details to check authentication.
            :param bot_type: (string) bot1/ bot2/ bot3
            :return: resource_fields: (dictionary) {status: request status(200/400, message:message}
        """
        args = put_and_patch_arg.parse_args()  # the param

        # check bot authorization
        bot_authorization = self.before_first_request(bot_type=bot_type, func_name=args.get("sub_field_name_or_sub_value"), args=args)
        # check if function is in the bot intent
        can_update = auth.is_authorized_in_intent(bot_type=bot_type, func=args.get("sub_field_name_or_sub_value"))

        # # in case of bot1 check permission
        # if bot_type == "bot1":
        #     can_update = auth.check_bot1_permissions(bot_type=bot_type, func=args.get("sub_field_name_or_sub_value"))
        #
        # # in case of cot3 check authentication
        # elif bot_type == "bot3":
        #     name = args.get("name")
        #     password = args.get("password")
        #     certificate = args.get("certificate")
        #     can_update = auth.check_bot3_authentication(bot_type=bot_type, name=name, password=password,
        #                                                 certificate=certificate)
        if (not can_update) or (not bot_authorization):
            return {'status': 400, 'message': "Something want wrong didnt updated successfully"}

        # else: can update
        ans = utils.update_in_bot(bot=bot_type, field_name=args.get("field_name"), new_value=args.get("new_value"),
                                  sub_field_name_or_sub_value=args.get("sub_field_name_or_sub_value"))
        return ans

    @marshal_with(resource_fields)
    def patch(self, bot_type):
        """
            handles PATCH request: change authorization or bot basic details as name or intent
            The function name and new value to return from the function is received in the request param argument
            in a JSON form, and in case of bot3 also the bot details to check authentication
            :param bot_type: (string) bot1/ bot2/ bot3
            :return: resource_fields=(dictionary) {status: request status(200/400, message:message}
        """
        args = put_and_patch_arg.parse_args()  # the param
        can_patch = True

        # check bot authorization
        bot_authorization = self.before_first_request(bot_type=bot_type, func_name=args.get("new_value"), args=args)

        if not can_patch or not bot_authorization:
            return {'status': 400, 'message': "Something want wrong didnt patch successfully"}

        # else: can patch
        ans = utils.patch_in_bot(bot=bot_type, field_name=args.get("field_name"), new_value=args.get("new_value"),
                                 sub_field_name_or_sub_value=args.get("sub_field_name_or_sub_value"))
        return ans

    @marshal_with(resource_fields)
    def delete(self, bot_type):
        """
            handles DELETE request: delete a bot
            The function name and new value to return from the function is received in the request param argument
            in a JSON form, and in case of bot3 also the bot details to check authentication
            :param bot_type: (string) bot1/ bot2/ bot3
            :return: resource_fields= (dictionary) {status: request status(204/404, message:message}
        """
        ans = utils.delete_bot(bot_type)
        return ans


# api resource
api.add_resource(server, "/botHandler/<string:bot_type>")

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    # create all the bots JSON file and there functions
    create_json_data.run()

    # start the server with the 'run()' method
    app.run(port=5000, debug=True)
