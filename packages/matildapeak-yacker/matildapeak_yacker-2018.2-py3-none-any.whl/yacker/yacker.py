#!/usr/bin/env python3

"""A utility to drive packer with a YAML file. It's a packer YAML wrapper.

Alan Christie
November 2018
"""

import json
import os
import subprocess
import sys
import yaml


def error(msg):
    """Prints an error message and exists with a non-zero exit code.

    :param msg: The error message
    :type msg: ``str``
    """
    print('ERROR: %s' % msg)
    sys.exit(1)


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main():
    """The console script entry-point. Called when yacker is executed
    or from __main__.py, which is used by the installed console script.
    """

    # Find the yaml file. If there isn't one, assume it's
    # called 'template.yml'
    yaml_file_name = None
    yaml_arg_num = 0
    for arg_num in range(1, len(sys.argv)):
        arg = sys.argv[arg_num]
        if arg.endswith('.yml') or arg.endswith('.yaml'):
            if yaml_file_name:
                error('Sorry, only 1 YAML file allowed')
            yaml_file_name = arg
            yaml_arg_num = arg_num
        arg_num += 1
    if not yaml_file_name:
        yaml_file_name = 'template.yml'
    # Does the file exist?
    if not os.path.isfile(yaml_file_name):
        error('%s does not exist' % yaml_file_name)

    # Replace yaml with json...

    # Load the YAML file...
    json_file_name = os.path.splitext(yaml_file_name)[0] + '.json'
    yaml_content = None
    try:
        with open(yaml_file_name, 'r') as stream:
            try:
                yaml_content = yaml.load(stream)
            except yaml.YAMLError as exception:
                error(exception)
    except PermissionError as p_err:
        error(p_err)
    if not yaml_content:
        error('No content loaded from %s' % yaml_file_name)
    # Write as a JSON file...
    try:
        with open(json_file_name, 'w') as json_file:
            json.dump(yaml_content, json_file, indent=2)
    except PermissionError as p_err:
        error(p_err)

    # Now, just re-construct the command-line...
    cmd = 'packer'
    for arg_num in range(1, len(sys.argv)):
        if arg_num == yaml_arg_num:
            cmd += ' %s' % json_file_name
        else:
            cmd += ' %s' % sys.argv[arg_num]

    # ...and run packer...
    completed_process = subprocess.run(cmd.split())

    # Regardless of the outcome, remove the JSON file.
    # This avoids the user accidentally trying to edit it.
    os.remove(json_file_name)

    # Exit with packer's exit code...
    sys.exit(completed_process.returncode)


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
