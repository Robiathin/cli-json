#!/usr/bin/env python
# Copyright (c) 2016 Robert Tate <rob@rtate.se>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import sys
import json
import getopt

VERSION = "v0.1.1"

def die(msg):
    sys.stderr.write(msg + "\n")
    exit(1)

def usage():
    usage = """Usage:
    If -f is not specified cli-json.py will read from STDIN

    -i arg          Specify the number of spaces to indent with.
    -f arg          Specify a file containing JSON to format.
    -c              Colour output
    -h, --help      Print this message.
    -v, --version   Print version information"""
    print(usage)

opts, args = getopt.getopt(sys.argv[1:], "hci:f:v", ["help", "version"])

has_file = False
indent_size = 4
color_output = False

for o, a in opts:
    if o == "-c":
        color_output = True
    elif o == "-f":
        file_arg = a
        has_file = True
    elif o == "-i":
        try:
            indent_size = int(a)
        except ValueError:
            die("Invalid argument for -i!")

        if indent_size < 0:
            die("Invalid argument for -i!")
    elif o in ("-h", "--help"):
        usage()
        exit()
    elif o in ("-v", "--version"):
        print("cli-json.py version: " + VERSION)
        print("Copyright (c) 2016 Robert Tate")
        print("This software is available under the ISC license.")
        exit()
    else:
        die("Unrecognized argument found!")

# If no file is provided use STDIN for JSON source
if has_file:
    with open(file_arg, "r") as json_file:
        data = json_file.read().replace("\n", "")
else:
    data = sys.stdin.read()

if not data.strip():
    exit()

try:
    parsed_data = json.loads(data)
except ValueError:
    exit(1)

def prep_arg(arg):
    # Hack to work with both 2.X and 3.X
    if isinstance(arg, basestring) if sys.version_info < (3, 0) else isinstance(arg, str):
        arg = arg.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
        return "\"%s\"" % arg
    elif type(arg) is bool:
        return "true" if arg else "false"
    elif arg is None:
        return "null"

    return str(arg)

def print_indent(indent_level):
    for i in range(indent_level):
        for j in range(indent_size):
            sys.stdout.write(" ")

def color_key(arg):
    return "\033[1;31m%s\033[0m" % arg

def color_value(arg):
    if arg == "true" or arg == "false":
        return "\033[1;32m%s\033[0m" % arg
    elif arg == "null":
        return "\033[1;36m%s\033[0m" % arg
    else:
        try:
            float(arg)
            return "\033[1;35m%s\033[0m" % arg
        except ValueError:
            return "\033[1;34m%s\033[0m" % arg

# Recursively parse and print a formatted version of the JSON
def node_iterate(arg, start_indented, indent_level):
    if type(arg) is list:
        if start_indented:
            print_indent(indent_level - 1)

        sys.stdout.write("[\n")

        for i, value in enumerate(arg):
            if type(value) is list or type(value) is dict:
                node_iterate(value, True, indent_level + 1)
            else:
                print_indent(indent_level)
                sys.stdout.write(color_value(prep_arg(value)) if color_output else prep_arg(value))

            if (i + 1) != len(arg):
                sys.stdout.write(",")

            sys.stdout.write("\n")

        print_indent(indent_level - 1)
        sys.stdout.write("]")
    elif type(arg) is dict:
        if start_indented:
            print_indent(indent_level - 1)

        sys.stdout.write("{\n")

        for i, key in enumerate(arg):
            print_indent(indent_level)
            sys.stdout.write((color_key(prep_arg(key)) if color_output else prep_arg(key)) + ": ")

            if type(arg[key]) is list or type(arg[key]) is dict:
                node_iterate(arg[key], False, indent_level + 1)
            else:
                sys.stdout.write(color_value(prep_arg(arg[key])) if color_output else prep_arg(arg[key]))

            if (i + 1) != len(arg):
                sys.stdout.write(",")

            sys.stdout.write("\n")

        print_indent(indent_level - 1)
        sys.stdout.write("}")

node_iterate(parsed_data, False, 1)

sys.stdout.write("\n")
