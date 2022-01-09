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

def dl(filepath, name, k, url, need_dl):
    if Path(filepath).is_file():
        Path(filepath).resolve(strict=True)
        status = '%sPRESENT%s' % (fg('green'), attr('reset'))
    else:
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        status = '%sMISSING%s' % (fg('red'), attr('reset'))
        need_dl = True
    if not urlparse(url).scheme:
        need_dl = False
    print(name.replace('/', ' - ') + " - " + k + ' --> ' + status)
    if need_dl:
        # Streaming, so we can iterate over the response.
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            err_msg = 'The following error happen when trying to download the file:'
            err_code = '%s - %s' % (response.status_code, response.reason)
            print('%sWARNING%s - %s %s' % (fg('yellow'), attr('reset'), err_msg, err_code))
            return
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

def read_dict(data, name, repository, dl_url):
    rname = False
    for k, v in data.items():
        if isinstance(v, dict):
            if rname:
                name = os.path.dirname(name) + '/' + k.replace('/', '\/')
            else:
                name = name + "/" + k.replace('/', '\/')
            name = name.lstrip('/')
            read_dict(v, name, repository, dl_url)
        else:
            filepath = base + "/" + repository + urlparse(v).path
            url = v
            if not urlparse(url).scheme and dl_url:
                url = dl_url.rstrip('/')
                path = v.lstrip('/')
                url = url + '/' + path
            need_dl = False
            if filepath.endswith('/'):
                response = requests.get(url)
                webpage = html.fromstring(response.content)
                href = webpage.xpath('//a/@href')
                files = [x for x in href if '../' not in x]
                for f in files:
                    filepath = base + "/" + repository + urlparse(url).path + f
                    dl(filepath, name, k, url, need_dl)
            else:
                dl(filepath, name, k, url, need_dl)
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
                    dl_url = ""
                    if 'README' in repo_data:
                        data['README'] = repo_data['README']
                    if 'download_url' in repo_data:
                        dl_url = repo_data['download_url']
                    read_dict(
                        data=data,
                        name="",
                        repository=Path(repo_data['repository']).stem,
                        dl_url=dl_url
                    )

load_repositories()
