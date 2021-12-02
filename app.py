# import the Flask class from the flask module
from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, marshal_with, fields
import createJsonData
import utils
import create_task as ct

# create the application object
app = Flask(__name__, template_folder="templates")
api = Api(app)

get_arg = reqparse.RequestParser()
get_arg.add_argument("func_name", type=str, help="Name of the function is required", required=True)
get_arg.add_argument("name", type=str, help="bot name is required", required=False)
get_arg.add_argument("password", type=int, help="bot password is required", required=False)
get_arg.add_argument("certificate", type=str, help="bot certificate is required", required=False)

post_arg = reqparse.RequestParser()
post_arg.add_argument("func_name", type=str, help="Name of the function is required", required=True)
post_arg.add_argument("default_value", type=str, help="Default value the function return is required",
                      required=True)

put_and_patch_arg = reqparse.RequestParser()
put_and_patch_arg.add_argument("field_name", type=str, help="Field name is required", required=True)
put_and_patch_arg.add_argument("new_value", type=str, help="New value the function return is required",
                               required=True)
put_and_patch_arg.add_argument("sub_field_name_or_sub_value", type=str, help="Field name is required", required=False)
put_and_patch_arg.add_argument("name", type=str, help="bot name is required", required=False)
put_and_patch_arg.add_argument("password", type=int, help="bot password is required", required=False)
put_and_patch_arg.add_argument("certificate", type=str, help="bot certificate is required", required=False)


resource_fields = {
    'status': fields.Integer,
    'message': fields.String
}


class server(Resource):

    @marshal_with(resource_fields)
    def get(self, bot_type):
        args = get_arg.parse_args()
        func_name = args.get("func_name")
        is_authorized = utils.is_authentication(bot_type=bot_type, func=func_name)
        bot_permission = True
        # in case of bot1 check permission
        if bot_type == 'bot1':
            bot_permission = utils.check_bot1_permissions(bot_type=bot_type, func="play_sound")
        # in case of cot3 check authentication
        elif bot_type == 'bot3':
            name = args.get("name")
            password = args.get("password")
            certificate = args.get("certificate")
            bot_permission = utils.check_bot3_authentication(bot_type=bot_type, name=name, password=password,
                                                             certificate=certificate)

        if (not is_authorized) or (not bot_permission):
            return {'status': 401, 'message': "You dont have permission for this function"}

        ans = utils.do_the_function(bot_type=bot_type, func_name=func_name)
        return ans

    @marshal_with(resource_fields)
    def post(self, bot_type):
        args = post_arg.parse_args()
        ans = ct.create_function(func_name=args.get("func_name"), bot_permission=bot_type,
                                 default_value=args.get("default_value"))
        return ans

    @marshal_with(resource_fields)
    def put(self, bot_type):
        args = put_and_patch_arg.parse_args()
        can_update = utils.is_authentication(bot_type=bot_type, func=args.get("sub_field_name_or_sub_value"))
        if bot_type == "bot1":
            can_update = utils.check_bot1_permissions(bot_type=bot_type, func=args.get("sub_field_name_or_sub_value"))
        elif bot_type == "bot3":
            name = args.get("name")
            password = args.get("password")
            certificate = args.get("certificate")
            can_update = utils.check_bot3_authentication(bot_type=bot_type, name=name, password=password,
                                                             certificate=certificate)
        if not can_update:
            return {'status': 400, 'message': "Something want wrong didnt updated successfully"}

        ans = utils.update_in_bot(bot=bot_type, field_name=args.get("field_name"), new_value=args.get("new_value"),
                                  sub_field_name_or_sub_value=args.get("sub_field_name_or_sub_value"))
        return ans

    @marshal_with(resource_fields)
    def patch(self,bot_type):
        args = put_and_patch_arg.parse_args()
        can_patch = True
        if bot_type == "bot1":
            can_patch = utils.check_bot1_permissions(bot_type=bot_type, func=args.get("new_value"))
        elif bot_type == "bot3":
            name = args.get("name")
            password = args.get("password")
            certificate = args.get("certificate")
            can_patch = utils.check_bot3_authentication(bot_type=bot_type, name=name, password=password,
                                                         certificate=certificate)
        if not can_patch:
            return {'status': 400, 'message': "Something want wrong didnt patch successfully"}

        ans = utils.patch_in_bot(bot=bot_type, field_name=args.get("field_name"), new_value=args.get("new_value"),
                                  sub_field_name_or_sub_value=args.get("sub_field_name_or_sub_value"))
        return ans

    @marshal_with(resource_fields)
    def delete(self, bot_type):
        ans = utils.delete_bot(bot_type)
        return ans


api.add_resource(server, "/botHandler/<string:bot_type>")

# start the server with the 'run()' method
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    createJsonData.run()
    app.run(port=5000, debug=True)
