#!/bin/python
import datetime
import json
import os
from pathlib import Path

import requests
from colored import attr, bg, fg
from lxml import html
from tqdm import tqdm

with open('repositories/bob_pony.json', 'r') as f:
    data = json.load(f)

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
    print(name + "/" + k + ' --> ' + status)
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

def read_dict(data, name=""):
    rname = False
    for k, v in data.items():
        if isinstance(v, dict):
            if rname:
                name = os.path.dirname(name) + '/' + k.replace('/', '\/')
            else:
                name = name + "/" + k.replace('/', '\/')
            name = '/' + name.lstrip('/')
            read_dict(v, name)
        else:
            need_dl = False
            filename = os.path.basename(v)
            filepath = base + '/' + name + "/" + filename
            if filepath.endswith('/'):
                response = requests.get(v)
                webpage = html.fromstring(response.content)
                href = webpage.xpath('//a/@href')
                files = [x for x in href if '../' not in x]
                for f in files:
                    filename = f
                    filepath = base + '/' + name + '/' + k.replace('/', '\/') + '/' + filename
                    dl(filepath, name, k, v, need_dl)
            else:
                dl(filepath, name, k, v, need_dl)
        rname = True

    with open('version.txt', 'w') as f:
        now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        f.write(now)



read_dict(data)
