import os
import requests
import json
from tools.colors import Colors


class SceProtoGenerator:
    colors = Colors()
    language_map = {
        'js': True,
        'py': True
    }

    def __init__(self, proto_path, language_types):
        self.proto_path = proto_path
        self.full_proto_path = os.path.join(os.getcwd(), proto_path)
        self.language_types = language_types
        data = None
        with open('./config/config.json') as f:
            data = json.load(f)
        self.server_url = data['SERVER_URL']
        self.generate_api_url = self.server_url + '/generate'

    def check_file_path(self):
        if not os.path.isfile(self.full_proto_path):
            raise FileNotFoundError(
                f'The path {self.proto_path} could not be resolved.')

    def check_language_types(self):
        for language in self.language_types:
            if language not in self.language_map:
                self.print_supported_languages(language)

    def check_server_health(self):
        healthy = False
        try:
            requests.get(self.server_url)
            healthy = True
        except requests.exceptions.ConnectionError:
            self.colors.print_red(f'The server at {self.server_url} is down.')
        return healthy

    def call_generate_api(self):
        response = False
        try:
            params = dict((key, True) for key in self.language_types)
            with open(self.full_proto_path, 'rb') as f:
                response = requests.post(self.generate_api_url,
                                         files={self.proto_path: f},
                                         params=params)
        except requests.exceptions.ConnectionError:
            self.colors.print_red(f'The server at {self.server_url} is down.')
        return response

    def print_file_urls(self, file_dict):
        self.colors.print_green(
            'Your files have been sucessfully generated!\n')
        for file_name in file_dict.keys():
            self.colors.print_pink(file_name + ':')
            self.colors.print_yellow(file_dict[file_name] + '\n')

    def handle_proto_generation(self):
        self.colors.print_purple('Welcome to the gRPC proto code generator!')
        self.check_file_path()
        self.check_language_types()
        if self.check_server_health():
            response = self.call_generate_api()
            self.print_file_urls(response.json())

    def print_supported_languages(self, unsupported_type):
        supported_types = ', '.join(
            [type for type in self.language_map.keys()])
        error_str = f'Sorry! \'{unsupported_type}\' is not a supported language\
 type. Supported types are: {supported_types}'
        raise NotImplementedError(error_str)
