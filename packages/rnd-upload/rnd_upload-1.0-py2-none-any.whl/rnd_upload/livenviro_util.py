import os
import sys
from terminaltables import AsciiTable


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def f_blue(line):
    return "{0}{1}{2}".format(bcolors.OKBLUE, line, bcolors.ENDC)


def display_config(config):
    data = [["Item", "Value"]]

    for key, value in config.iteritems():
        data.append([key, value])

    table = AsciiTable(data)
    table.title = f_blue(" Configuration ")

    print("\n")
    print(table.table)


def get_config_filename():
    """
    Extracts the config filename from the arguments passed when calling the script

    :return string: config_filename
    """
    if len(sys.argv) != 2:
        print("Invalid number of arguments")
        print("Usage: {0} <config file name>".format(sys.argv[0]))

        sys.exit(0)
    else:
        config_filename = sys.argv[1]
        if not os.path.isfile(config_filename):
            print("Config file {0} doesn't exist".format(config_filename))
            sys.exit(0)
        else:
            return config_filename
