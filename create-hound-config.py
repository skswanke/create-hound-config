#!/usr/bin/env python3

import sys
import os
import re
import json

if len(sys.argv) < 2:
    sys.exit("Needs Git directory path.")

DIRECTORY = sys.argv[1]

REPOS = [os.path.join(DIRECTORY, o)
         for o in os.listdir(DIRECTORY)
         if os.path.isdir(os.path.join(DIRECTORY, o))]

HOUND_JSON = {
    "max-concurrent-indexers" : 2,
    "dbpath" : "data",
    "repos" : {}
}

def main():
    for repo in REPOS:
        git_config_location = repo + "/.git/config"
        with open(git_config_location) as config:
            for line in config:
                if "url" in line:
                    repo_name = repo.split('/')[4].split('.')[0]
                    git_url = re.search(r"git.*?\.git", line)
                    if git_url:
                        repo_json = {
                            repo_name: {
                                "url": git_url.group(0)
                            }
                        }
                        HOUND_JSON["repos"].update(repo_json)

    output_json = json.dumps(HOUND_JSON)
    with open("config.json", "w") as out_file:
        out_file.write(output_json)

    sys.exit("Hound config written to config.json in this folder.")

if __name__ == "__main__":
    main()
