import argparse
import json
import os
import sys
import shutil
import requests
import traceback
import urllib.parse as parse
import urllib.request as request
from http import HTTPStatus
from git import Repo

base_url = ""
private_token = ""
url =  base_url + "/api/v4/projects?private_token=" + private_token


def get_projects(url):
    print(url)
    response = requests.get(url)
    print(response)
    projects = json.loads(response.text)

    while response.headers["X-Next-Page"]:
        next_page = response.headers["X-Next-Page"]
        response = requests.get(url + "&page=" + next_page)
        print(response)
        projects += json.loads(response.text)
        num_projects = len(projects)
        for i, p in enumerate(projects):
            pdir = p['name']
            try:
                os.mkdir(pdir)
                repo = Repo.clone_from(p['ssh_url_to_repo'], pdir)
                origin = repo.remote('origin')
                for f in origin.fetch():
                    pass
                print('Cloned {} of {}: {}'.format(i+1, num_projects, pdir))
            except Exception as error:
                print('Error while cloning {}:\n{!s}\n{}'
                      .format(pdir, error, traceback.format_exc()))
                continue

get_projects(url)
