#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import logging
import os
import sys
from argparse import ArgumentParser

logger = logging.getLogger(__name__)

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')

def parse_arguments():
    # Parse arguments.
    parser = ArgumentParser(
        description='Automatic keyboard shortcut remapping when working in Blender')
    parser.add_argument( '-d', '--log', dest='loglevel', action='store',
        default='ERROR', help=(
            'set log level [DEBUG, INFO, WARNING, ERROR, CRITICAL] '
            '(default: ERROR)'))
    parser.add_argument( '--debug', dest='debug', action='store_true',
        default=False, help='run in DEBUG mode')

    subparsers = parser.add_subparsers(title='subcommands', description='Valid subcommands',
                                       help='Select a command to run.', dest='command')
    subparsers.required = True

    parser_on = subparsers.add_parser('on', help='Turn blendermode on')
    parser_off = subparsers.add_parser('off', help='Turn blendermode off')

    args = parser.parse_args()

    if args.debug:
        args.loglevel = 'DEBUG'

    # Configure logger.
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel.upper())
    logging.basicConfig(level=numeric_level)

    return args


def get_config_path():

    config_path = None
    if os.environ.get('BLENDERMODE_CONFIG'):
        config_path = os.path.expanduser(os.environ.get('BLENDERMODE_CONFIG'))
    elif os.path.exists(DEFAULT_PATH):
        config_path = DEFAULT_PATH
    elif os.environ.get('XDG_CONFIG_HOME') and os.path.exists(
        os.path.join(os.environ.get('XDG_CONFIG_HOME'), 'blendermode')):
        config_path = os.path.join(os.environ.get('XDG_CONFIG_HOME'), 'blendermode')
    elif os.environ.get('HOME') and os.path.exists(
        os.path.join(os.environ.get('HOME'), '.config', 'blendermode')):
        config_path = os.path.join(os.environ.get('HOME'), '.config', 'blendermode')
    elif os.path.exists(os.path.expanduser('~/.blendermode')):
        config_path = os.path.expanduser('~/.blendermode')
    elif os.path.exists('/etc/blendermode.cfg'):
        config_path = '/etc/blendermode.cfg'

    return config_path


def update_config(section, values={}):

    result = False

    config_path = get_config_path()
    if config_path and values:
        logger.debug('Updating config.ini file.')
        config = configparser.ConfigParser()
        config.read(config_path)
        if section not in config: config.update({section: dict()})
        config[section].update({
            key:str(value) for key, value in values.items()
        })

        with open(config_path, 'w') as configfile:
            config.write(configfile)
        logger.debug('Updated config.ini file.')
        result = True

    return result


def get_config():

    config_path = get_config_path()
    config = configparser.ConfigParser()

    if config_path:
        try:
            logger.debug('Reading configuration file (%s).' % config_path)
            config.read(config_path)
        except configparser.MissingSectionHeaderError as e:
            logger.error('Could not read configuration file (%s).' % config_path)
            sys.exit(str(e))
        else:
            logger.info('Read configuration file successfully! (%s)' % config_path)
    else:
        logger.info('No configuration file found!')
        logger.debug('Saving default config.ini file.')

        # Define default config.ini file.
        config['DEFAULT'] = {
            'mouse_remap': "'<Super>'",
            'keyboard_remap': "['']"}
        config['@blender'] = {
            'mouse_conflict': "'<Alt>'",
            'keyboard_shortcuts': [
                '<Alt>space',
                '<Primary><Alt>KP_0'] }

        with open(DEFAULT_PATH, 'w') as configfile:
            config.write(configfile)
        logger.debug('Saved config.ini file.')

    return config

