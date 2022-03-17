#!/usr/bin/env python3
# coding: utf-8
# File              : backup.py
# Original Author   : abusesa (https://github.com/abusesa/github-backup)
# Modified by       : Justin Greever (https://github.com/jgreever/github-backup)
# Last Modified     : 2022-03-16
# Description       : Backup a GitHub repository
# Requires          : Python 3.6+
# ----------------------------------------------------------------------------- #
# License:
# The MIT License (MIT)
#
# Copyright (c) 2015 abusesa (https://github.com/abusesa/github-backup)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------- #


# Import modules
import argparse
import configparser
import json
import os
import re
import subprocess
import sys
import urllib.parse

import requests


# Version
__version__ = '1.1.0'


# Function: import_json_config() - import a JSON config file
def import_json_config():
    config = configparser.ConfigParser()
    config.read("config.json")
    return config


# Function: get_json() - get a JSON response
def get_json(url, token):
    while True:
        response = requests.get(
            url, headers={"Authorization": "token {0}".format(token)}
        )
        response.raise_for_status()
        yield response.json()
        if "next" not in response.links:
            break
        url = response.links["next"]["url"]


# Function: check_name() - check if a name is valid
def check_name(name):
    if not re.match(r"^\w[-.\w]*$", name):
        raise RuntimeError("invalid name '{0}'".format(name))
    return name


# Function: mkdir() - create a directory
def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print("Directory already exists: {0}".format(directory))


# function: backup() - backup a repository
def backup(repo_name, repo_url, to_path, username, token, typeof):
    parsed = urllib.parse.urlparse(repo_url)
    modified = list(parsed)
    modified[1] = "{username}:{token}@{netloc}".format(
        username=username, token=token, netloc=parsed.netloc
    )
    repo_url = urllib.parse.urlunparse(modified)
    repo_path = os.path.join(to_path, username, repo_name)
    if os.path.exists(repo_path):
        print("Repository already exists: {0}".format(repo_path))
        if typeof == "clone":
            subprocess.call(
                [
                    "git",
                    "pull",
                    "--quiet",
                ],
                cwd=repo_path
            )
    else:
        mkdir(repo_path)
        if typeof == "clone":
            subprocess.call(
                [
                    "git",
                    "clone",
                    "--quiet",
                    repo_url,
                    repo_path,
                ]
            )
        elif typeof == "backup":
            subprocess.call(
                [
                    "git",
                    "init",
                    "--bare",
                    "--quiet"
                ],
                cwd=repo_path
            )
            subprocess.call(
                [
                    "git",
                    "fetch",
                    "--quiet",
                    "--force",
                    "--prune",
                    "--tags",
                    repo_url,
                    "refs/heads/*:refs/heads/*",
                ],
                cwd=repo_path,
            )


# Function: main() - main function
def main():
    print("\nbackup.py - GitHub Repository Backup")
    print("====================================\n")

    # If user already has config.json setup with the token, directory, and owner
    # then we can simply start  by typing './backup.py', otherwise we
    # need to set up the config.json file or get the information from the user
    # via command line arguments.
    parser = argparse.ArgumentParser(
        description="Backup or Clone repositories from GitHub to local directory"
    )
    parser.add_argument(
        "--config",
        "-c",
        help="Path to config file (default: config.json)",
        default="config.json",
    )
    parser.add_argument(
        "--directory",
        "-d",
        help="Path to backup location (default: read from config.json)",
    )
    parser.add_argument(
        "--owners",
        "-o",
        help="GitHub repositories for specific owner (default: read from config.json)",
    )
    parser.add_argument(
        "--token",
        "-t",
        help="GitHub token (default: read from config.json)",
    )
    parser.add_argument(
        "--type",
        "-y",
        help="Type of backup (default: read from config.json)",
        choices=["backup", "clone"],
    )
    parser.add_argument(
        "--version",
        "-V",
        help="Print version and exit",
        action="version",
        version="Version: %(prog)s {0}".format(__version__),
    )

    # Get the arguments from the command line or from the config.json file
    args = parser.parse_args()
    with open(args.config, "rb") as f:
        config = json.loads(f.read())

    # If the user has set up the config.json file, we can extract the token,
    # directory, and owner from the config.json file otherwise we will get the
    # information from the user via command line arguments.
    # Check for user input before checking in the config.json file for the
    # token, directory, and owner. (NOTE: Testing .env for holding the token)
    if args.token:
        token = args.token
    elif os.environ.get("GITHUB_TOKEN"):
        os.environ['GITHUB_TOKEN'] = config["token"]
        token = config["token"]
    elif config["token"]:
        token = config["token"]
    else:
        token = input("GitHub token: ")

    if args.directory:
        directory = args.directory
    elif config["directory"]:
        directory = config["directory"]
    else:
        directory = input("Backup location: ")

    if args.owners:
        owners = args.owners
    elif config["owners"]:
        owners = config["owners"]
    else:
        owners = input("GitHub owners: ")

    if args.type:
        typeof = args.type
    elif config["type"]:
        typeof = config["type"]
    else:
        typeof = input("Type of backup (backup/clone): ")

    # If the directory doesn't exist, we need to create it.
    if mkdir(directory):
        print("Created directory {0}".format(directory), file=sys.stderr)

    # Login to GitHub and get the list of repositories for each owner.
    user = next(get_json("https://api.github.com/user", token))
    print("Logged in as {0}\n".format(user["login"]))
    for page in get_json("https://api.github.com/user/repos", token):
        for repo in page:
            name = check_name(repo["name"])
            owner = check_name(repo["owner"]["login"])
            clone_url = repo["clone_url"]

            # If owner is not in the list, skip it
            if owners and owner not in owners:
                continue

            # If the owner is in the list of owners, then we can mirror the
            # repository and print the output to the console.
            if owners and owner in owners:
                if typeof == "clone":
                    print("Cloning {0}/{1}".format(owner, name))
                    backup(name, clone_url, directory, user["login"], token, typeof)
                elif typeof == "backup":
                    print("Backing up {0}/{1}".format(owner, name))
                    backup(name, clone_url, directory, user["login"], token, typeof)
                else:
                    print("Invalid type: {0}".format(typeof))
                print("Finished Processing {0}/{1}\n".format(owner, name))


# If this script is being run directly, then run the main function.
if __name__ == "__main__":
    main()
