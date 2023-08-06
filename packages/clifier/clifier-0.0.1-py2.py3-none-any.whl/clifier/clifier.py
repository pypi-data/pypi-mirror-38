import os
import yaml
import logging
import argparse

logger = logging.getLogger("clifier")


class Clifier(object):

    defaults = {
        'required': False,
        'nargs': 1
    }

    def __init__(self, config_path, prog_version=None,
                 use_base_defaults=False, defaults=None):
        """

        :param config_path:
        :param use_base_defaults:
        :param defaults:
        """
        self.config_path = config_path
        self.config = self.read_config()
        self.defaults = defaults if defaults \
            else self.defaults if use_base_defaults else None
        self.prog_version = prog_version if prog_version else self.config.get(
            "parser", {}).get("version")

    def create_parser(self):
        """ """
        parser_params = self.config.get('parser', None)
        parser = argparse.ArgumentParser(**parser_params)

        if 'commands' in self.config:
            self.create_commands(self.config['commands'], parser)

        if 'subparsers' in self.config and self.config['subparsers']:
            self.create_subparsers(parser)

        if 'commands' not in self.config and not 'subparser' not in self.config:
            logging.warning("Created cli parser without commands and subparser."
                            "Need to define sections 'commands' and 'subparser'"
                            "in {}.".format(self.config_path))
        return parser

    def apply_defaults(self, commands):
        """ apply default settings to commands
            not static, shadow "self" in eval
        """
        for command in commands:
            if 'action' in command and "()" in command['action']:
                command['action'] = eval("self.{}".format(command['action']))
            if command['keys'][0].startswith('-'):
                if 'required' not in command:
                    command['required'] = False

    def create_commands(self, commands, parser):
        """ add commands to parser """
        self.apply_defaults(commands)
        def create_single_command(command):
            keys = command['keys']
            del command['keys']
            kwargs = {}
            for item in command:
                kwargs[item] = command[item]
            parser.add_argument(*keys, **kwargs)

        if len(commands) > 1:
            for command in commands:
                create_single_command(command)
        else:
            create_single_command(commands[0])


    def create_subparsers(self, parser):
        """ get config for subparser and create commands"""
        subparsers = parser.add_subparsers()
        for name in self.config['subparsers']:
            subparser = subparsers.add_parser(name)
            self.create_commands(self.config['subparsers'][name], subparser)

    def read_config(self):
        """ """
        if not os.path.isfile(self.config_path):
            raise Exception("File does not exist {}".format(
                self.config_path))
        yaml_file = open(self.config_path, 'r')
        conf = yaml.load(yaml_file)
        return conf

    def add_actions(self, actions_list):
        for action in actions_list:
            self.__setattr__(action.__name__, action)

    def show_version(self):
        """ custom command line  action to show version """
        class ShowVersionAction(argparse.Action):
            def __init__(inner_self, nargs=0, **kw):
                super(ShowVersionAction, inner_self).__init__(nargs=nargs, **kw)

            def __call__(inner_self, parser, args, value, option_string=None):
                print("{parser_name} version: {version}".format(
                    parser_name=self.config.get(
                        "parser", {}).get("prog"),
                    version=self.prog_version))
        return ShowVersionAction

    def check_path_action(self):
        """ custom command line action to check file exist """
        class CheckPathAction(argparse.Action):
            def __call__(self, parser, args, value, option_string=None):
                if type(value) is list:
                    value = value[0]
                user_value = value
                if option_string == 'None':
                    if not os.path.isdir(value):
                        _current_user = os.path.expanduser("~")
                        if not value.startswith(_current_user) \
                                and not value.startswith(os.getcwd()):
                            if os.path.isdir(os.path.join(_current_user, value)):
                                value = os.path.join(_current_user, value)
                            elif os.path.isdir(os.path.join(os.getcwd(), value)):
                                value = os.path.join(os.getcwd(), value)
                            else:
                                value = None
                        else:
                            value = None
                elif option_string == '--template-name':
                    if not os.path.isdir(value):
                        if not os.path.isdir(os.path.join(args.target, value)):
                            value = None
                if not value:
                    logger.error("Could not to find path %s. Please provide "
                                 "correct path to %s option",
                                 user_value, option_string)
                    exit(1)
                setattr(args, self.dest, value)

        return CheckPathAction
