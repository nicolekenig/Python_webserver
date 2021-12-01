import base64
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler,SimpleHTTPRequestHandler
import cgi
import logging
import create_task as ct
from urllib.parse import urlparse
from urllib.parse import parse_qs


taskList = ['task1', 'task2', 'task3']


class webserverHandler(BaseHTTPRequestHandler):
    json_list = []
    key = 0
    # def __init__(self, json_list):
    #     self.json_list = json_list

    def set_auth(self, username, password, certificate=''):
        self.key = base64.b64encode(
            bytes('%s:%s:%s' % (username, password,certificate), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


    def _set_response(self):
        # send response
        self.send_response(200)
        # send the headers that have the content type details, which the web page will display
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def isAuthentication(self, path):
        split_path = path.split('/')
        # split the end of the path to bot type anf the function
        func = split_path[1]
        bot_type = split_path[2]
        # get bot permissions_list
        f = open(bot_type + '.json')
        bot_dict = json.load(f)
        intent_list = bot_dict["allOf"]["intent"]
        return func in intent_list



    def delete_bot(self,bot):
        if os.path.exists(bot + '.json'):
            os.remove(bot + '.json')
            return True
        else:
            return False


    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Auth realm="Demo Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    '''
    :do_GET- handler all get requests
    :param: self
    '''

    def do_GET(self):
        if self.path.endswith('/base_bot'):
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            self._set_response()
            self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
            # content to our page
            output = ''
            output += '<html><body>'
            output += '<h1>Base Bot details:</h1>'
            # Opening JSON file
            f = open('base_bot.json')
            # returns JSON object as a dictionary
            bot_dict = json.load(f)
            # Iterating through the json list
            for k in bot_dict.keys():
                output += k + ": " + str(bot_dict[k])
                output += "</br>"
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/bot1'):
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            self._set_response()
            self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
            # content to our page
            output = ''
            output += '<html><body>'
            output += '<h1> Bot 1 details:</h1>'
            # Opening JSON file
            f = open('bot1.json')
            # returns JSON object as a dictionary
            bot_dict = json.load(f)
            # Iterating through the json list
            for k in bot_dict.keys():
                if k == 'allOf':
                    k_list = bot_dict[k]
                    for v in k_list:
                        output += v + ": " + str(k_list[v])
                        output += "</br>"
                if k == 'permissions_list':
                    output += k + ": " + str(bot_dict[k])
                    output += "</br>"
                if k == 'functions':
                    output += k + ": " + str(bot_dict[k])
                    output += "</br>"
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/play_sound/bot1'):
            self._set_response()
            # check if the bot have permission to the func
            is_authorized = self.isAuthentication(self.path)
            output = ''
            output += '<html><body>'
            if is_authorized:
                f = open('bot1.json')
                bot_dict = json.load(f)
                output += '<h1>' + bot_dict["functions"][0]['play_sound'] + '</h1>'
                output += "</br>"
                output += '</body></html>'
                self.wfile.write(output.encode())
                return bot_dict["functions"][0]['play_sound']
            else:
                output += '<h1>You dont have permission for this function </h1>'
                output += "</br>"
                output += '</body></html>'
                self.wfile.write(output.encode())
                return "You dont have permission for this function"

        if self.path.endswith('/default_welcome_message/bot2'):
            self._set_response()
            # check if the bot have permission to the func
            is_authorized = self.isAuthentication(self.path)
            output = ''
            output += '<html><body>'
            if is_authorized:
                f = open('bot2.json')
                bot_dict = json.load(f)
                output += '<h1>' + bot_dict["functions"][0]['default_welcome_message'] + '</h1>'
                output += "</br>"
                output += '</body></html>'
                self.wfile.write(output.encode())
                return bot_dict["functions"][0]['default_welcome_message']
            else:
                output += '<h1>You dont have permission for this function </h1>'
                output += "</br>"
                output += '</body></html>'
                self.wfile.write(output.encode())
                return "You dont have permission for this function"

        if self.path.endswith('/make_api_call/bot3'):
            key = self.get_auth_key()

            ''' Present frontpage with user authentication. '''
            if self.headers.get('Authorization') == None:
                self.do_AUTHHEAD()

                response = {
                    'success': False,
                    'error': 'No auth header received'
                }

                self.wfile.write(bytes(json.dumps(response), 'utf-8'))

            elif self.headers.get('Authorization') == 'Auth ' + str(key):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                # Do make api call
                self.wfile.write(bytes(json.dumps(), 'utf-8'))
            else:
                self.do_AUTHHEAD()
                response = {
                    'success': False,
                    'error': 'Invalid credentials'
                }
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            # self._set_response()
            # # check if the bot have permission to the func
            # is_authorized = self.isAuthentication(self.path)
            # if is_authorized:
            #     split_path = self.path.split('/')
            #     # split the end of the path to bot type anf the function
            #     bot_type = split_path[2]
            #     # get bot permissions_list
            #     f = open(bot_type + '.json')
            #     bot_dict = json.load(f)
            #     is_basic_authentication = bot_dict["is_basic_authentication"]
            #     output = ''
            #     output += '<html><body>'
            #     output += '<h1> Enter Validation:</h1>'
            #     output += '<form enctype="multipart/form-data">'
            #     output += '<input name="name" type="text" placeholder="Name">'
            #     output += '</br>'
            #     output += '<input name="pass" type="text" placeholder="Password">'
            #     output += '</br>'
            #
            #     if not is_basic_authentication:
            #         output += '<input name="certificate" type="text" placeholder="Certificate">'
            #         output += '</br>'
            #
            #     output += '<input type="submit" value="Send">'
            #     output += '</form>'
            #     output += '</body></html>'
            #
            #     is_name_valid = bot_dict["allOf"]["name"] == name
            #     bot_pass = bot_dict["password"]




        if self.path.endswith('/new'):
            self._set_response()
            # content to our page
            output = ''
            output += '<html><body>'
            output += '<h1> Add a new function</h1>'
            output += '<form method="POST" enctype="multipart/form-data">'
            output += '<input name="function" type="text" placeholder="Add new function">'
            output += '</br>'
            output += '<input name="default_value" type="text" placeholder="Default value">'
            output += '</br>'
            output += '<input name="bot" type="text" placeholder="Write the bot that the function will be">'
            output += '</br>'
            output += '<h3> Note about bot1: the permission of this func will be added to permissions_list</h3>'
            output += '<input type="submit" value="Add">'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())

        if self.path.endswith('/delete'):
            self._set_response()
            # content to our page
            output = ''
            output += '<html><body>'
            output += '<h1> Delete a bot </h1>'
            output += '<form method="DELETE" enctype="multipart/form-data">'
            output += '<input name="bot" type="text" placeholder="bot to delete">'
            output += '<input type="submit" value="Delete">'
            output += '</form>'
            output += '</body></html>'
            self.wfile.write(output.encode())

    def do_POST(self):
        if self.path.endswith('/new'):

            # ctype - content type
            # pdict- dictionary of the content type parameters
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTANT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_function = fields.get('function')[0]
                default_value = fields.get('default_value')[0]
                bot = fields.get('bot')[0]
                ct.create_function(func_name=new_function,bot_permission=bot,default_value=default_value)
                output =''
                output += '<html><body>'
                output += '<h1> New function details added successfully:</h1>'
                output += '<h3> new_function: '+new_function+'</h3>'
                output += '<h3> default_value: ' + default_value + '</h3>'
                output += '<h3> bot: ' + bot + '</h3>'
                output += '</body></html>'
                self._set_response()
                self.wfile.write(output.encode())

    def do_DELETE(self):
            # ctype - content type
            # pdict- dictionary of the content type parameters
        query_components = parse_qs(urlparse(self.path).query)
        if 'bot' in query_components:
            name = query_components["bot"][0]
            # fields = cgi.parse_multipart(self.rfile, pdict)
            # bot = fields.get('bot')[0]
            was_deleted = self.delete_bot(name)
            output = ''
            output += '<html><body>'
            if was_deleted:
                output += '<h1> Bot '+bool+'deleted successfully:</h1>'
            else:
                output += '<h1> Can not delete the file as it doesnt exists</h1>'
            output += '</body></html>'
            self._set_response()
            self.wfile.write(output.encode())

        # ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        # pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
        # content_len = int(self.headers.get('Content-length'))
        # pdict['CONTANT-LENGTH'] = content_len
        # if ctype == 'multipart/form-data':
        #     fields = cgi.parse_multipart(self.rfile, pdict)
        #     bot = fields.get('bot')[0]
        #     was_deleted = self.delete_bot(bot)
        #     output = ''
        #     output += '<html><body>'
        #     if was_deleted:
        #         output += '<h1> Bot '+bot+'deleted successfully:</h1>'
        #     else:
        #         output += '<h1> Can not delete the file as it doesnt exists</h1>'
        #     output += '</body></html>'
        #     self._set_response()
        #     self.wfile.write(output.encode())


# def main():
#     PORT = 8000
#     server_address = ('loaclhost', PORT)
#     json_list_to_server = ['bot1.json', 'bot2.json', 'Bot3.json']
#     server = HTTPServer(('', PORT), webserverHandler)
#     print('Server runing on port: ', PORT)
#     server.serve_forever()
#
#
# if __name__ == '__main__':
#     main()
