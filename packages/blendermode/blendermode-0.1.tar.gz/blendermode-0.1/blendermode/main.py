#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import logging
import os
import pwd
import re
import signal
import sys
import subprocess
from . import utils

# Initialize logger.
logger = logging.getLogger(__name__)

def sigint_handler(signal, frame):
    """
    Handle SIGINT interrupt.
    """
    logger.debug('Received SIGINT signal.')
    print('Exiting...')
    sys.exit(0)


def eval_config(L='[]'):
    """
    Evaluate the string representation of a Python literal.
    """
    return [l.strip() for l in ast.literal_eval(L)] if re.match(r'\[', L) else L


def get_system_conflicts(keyboard='[]', mouse='<Alt>'):
    logger.info('Looking for conflicts...')
    commands = [
        "gsettings list-recursively org.gnome.desktop.wm.keybindings",
        "gsettings list-recursively org.gnome.desktop.wm.preferences | grep 'mouse-button-modifier'"]

    system_settings = list()
    try:
        # Run each command and store all system settings.
        for command in commands:
            output = subprocess.check_output(
                ["/bin/bash", "-c", command]).decode("utf-8")
            system_settings.extend(output.split(os.linesep))
    except (subprocess.CalledProcessError) as error:
        # Exit if the command failed.
        print(error)
        sys.exit()
    else:
        # Filter out blank lines from the command output.
        system_settings = list(filter(None, system_settings))

    # Parse and determine relevant settings.
    gsetting_pattern = r"""
        ([a-z.]+)\          # Match GSettings schema (Group 1).
        ([a-z0-9-]+)\       # Match GSettings key (Group 2).
        (?!@as|\[?''\]?)    # Don't match disabled (i.e., blank) settings.
        ([\w_<>', \[\]]+)   # Match values (Group 3).
        """
    gsetting_regex = re.compile(gsetting_pattern, re.VERBOSE)

    relevant_settings = list()
    for setting in system_settings:
        match = re.search(gsetting_regex, setting)
        if match:
            relevant_settings.append(
                (match.group(1), match.group(2), eval_config(match.group(3))))

    # Find conflicts.
    keyboard_conflicts, mouse_conflict = dict(), dict()
    for setting in relevant_settings:
        schema, key, values = setting

        if (schema == 'org.gnome.desktop.wm.keybindings'
            and set(values).intersection(eval_config(keyboard))):
            keyboard_conflicts.update({' '.join([schema, key]): values})
        elif schema == 'org.gnome.desktop.wm.preferences' and values == mouse:
            mouse_conflict.update({' '.join([schema, key]): values})

    logger.info(
        'Conflicts found!' if keyboard_conflicts or mouse_conflict else
        'No conflicts found!')

    return (keyboard_conflicts, mouse_conflict)


def store_conflicts(keyboard={}, mouse={}):
    logger.info('Storing conflicts...')
    section_name = '$%s' % pwd.getpwuid(os.getuid()).pw_name
    utils.update_config(section_name, values=keyboard)
    utils.update_config(section_name, values=mouse)
    logger.info('Stored conflicts.')


def remap_system_settings(config, keyboard={}, mouse={}):

    logger.info('Remapping system settings...')

    keyboard_remap = config['DEFAULT']['keyboard_remap']
    mouse_remap = config['DEFAULT']['mouse_remap']

    for key in keyboard.keys():
        command = 'gsettings set {0} {1}'.format(key, keyboard_remap)
        logger.debug('Executing: %s' % command)
        subprocess.call(['/bin/bash', '-c', command])
    for key in mouse.keys():
        command = 'gsettings set {0} {1}'.format(key, mouse_remap)
        logger.debug('Executing: %s' % command)
        subprocess.call(['/bin/bash', '-c', command])

    logger.info('Remapped system settings.')


def restore_system_settings(config):
    logger.info('Restoring system settings...')

    # Filter items from the DEFAULT out of the stored settings.
    section_name = '$%s' % pwd.getpwuid(os.getuid()).pw_name
    stored_settings = {
        key: value for key, value in config[section_name].items()
        if key not in config.defaults()}

    # Restore system settings to their previous state.
    for key, value in stored_settings.items():
        if not re.match(r'[\'"]', value): value = '"%s"' % value
        command = 'gsettings set {0} {1}'.format(key, value)
        subprocess.call(['/bin/bash', '-c', command])

    # Purge stored settings.
    config.remove_section(section_name)
    logger.debug('Saving config.ini file...')
    with open(utils.DEFAULT_PATH, 'w') as configfile:
        config.write(configfile)
    logger.debug('Saved config.ini file.')

    logger.info('Restored system settings.')
    return config


def main():
    signal.signal(signal.SIGINT, sigint_handler)

    args = utils.parse_arguments()
    logger.debug('Received the following arguments...')
    logger.debug(args)

    config = utils.get_config()

    if args.command == 'on':
        print('Entering blendermode...')
        keyboard, mouse = get_system_conflicts(
            keyboard=config['@blender']['keyboard_shortcuts'],
            mouse=config['@blender']['mouse_conflict'])
        store_conflicts(keyboard=keyboard, mouse=mouse)
        remap_system_settings(config, keyboard=keyboard, mouse=mouse)
        print('Blendermode active!')
    else:
        print('Leaving blendermode...')
        restore_system_settings(config)
        print('Goodbye!')


if __name__ == '__main__':
    main()

