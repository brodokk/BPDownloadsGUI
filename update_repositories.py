#!/bin/python
import datetime
import json
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from colored import attr, bg, fg
from lxml import html
from tqdm import tqdm

base = 'files'

def dl(filepath, name, k, v, need_dl):
    if Path(filepath).is_file():
        Path(filepath).resolve(strict=True)
        status = '%sPRESENT%s' % (fg('green'), attr('reset'))
    else:
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        status = '%sMISSING%s' % (fg('red'), attr('reset'))
        need_dl = True
    print(name.replace('/', ' - ') + " - " + k + ' --> ' + status)
    if need_dl:
        url = v
        # Streaming, so we can iterate over the response.
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(filepath, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")

def read_dict(data, name, repository):
    rname = False
    for k, v in data.items():
        if isinstance(v, dict):
            if rname:
                name = os.path.dirname(name) + '/' + k.replace('/', '\/')
            else:
                name = name + "/" + k.replace('/', '\/')
            name = name.lstrip('/')
            read_dict(v, name, repository)
        else:
            filepath = base + "/" + repository + urlparse(v).path
            need_dl = False
            if filepath.endswith('/'):
                response = requests.get(v)
                webpage = html.fromstring(response.content)
                href = webpage.xpath('//a/@href')
                files = [x for x in href if '../' not in x]
                for f in files:
                    filepath = base + "/" + repository + urlparse(v).path + f
                    dl(filepath, name, k, v, need_dl)
            else:
                dl(filepath, name, k, v, need_dl)
        rname = True

    with open('version.txt', 'w') as f:
        now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        f.write(now)

def load_repositories():
    with open('repositories.json') as f:
        repositories = json.load(f)
        for repo_name, repo_data in repositories.items():
            if 'repository' in repo_data:
                with open(repo_data['repository']) as f:
                    data = json.load(f)
                    if 'README' in repo_data:
                        data['README'] = repo_data['README']
                    read_dict(data, "", Path(repo_data['repository']).stem)

load_repositories()
