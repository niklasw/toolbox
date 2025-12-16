#!/usr/bin/env python3

import json
import random
import magic
import string
import requests
import uuid
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta
from aws_s3_utils import upload_to_s3


def post(server_url, path='', params=None,
         headers='', payload=None, method=requests.post):
    url = '/'.join((server_url, path.strip('/')))
    print('Request sent to', url)
    try:
        r = method(url, json=payload, params=params, timeout=2)
    except Exception as e:
        print(e)
        print('POST failed')
        return {}
    if r.status_code != 200:
        print(f'POST failed with status {r.status_code}')
    else:
        try:
            response_payload = r.json()
        except:
            response_payload = r.content
        return response_payload


def get(*args, **kwargs):
    return post(*args, **kwargs, method=requests.get)


def random_key(length):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))


def assert_file_type(data: bytes, expected_mime: str):
    mime_type = magic.from_buffer(data, mime=True)
    return mime_type == expected_mime


class reolink:
    def __init__(self, url, user, password):
        self.user = user
        self.url = url
        self.password = password
        self.url_login = f'{self.url}/api.cgi?cmd=Login'
        self.token = None
        self.lease_time = 0
        self.last_login = None

    def login_body(self):
        user = {'Version': '0',
                'userName': self.user,
                'password': self.password}
        return [{'cmd': 'Login', 'param': {'User':user}}]

    def is_token_still_valid(self):
        if self.last_login is not None and self.token:
            token_age = datetime.now() - self.last_login
            return token_age < timedelta(seconds=self.lease_time-99)

    def do_login(self):
        if self.is_token_still_valid():
            return
        credentials = post(self.url,
                           path='api.cgi',
                           params={'cmd':'Login'},
                           payload=self.login_body())
        # [{'cmd': 'Login', 'code': 0, 'value':
        #     {'Token': {'leaseTime': 3600, 'name': '63f343a87def2fb'}}}]
        try:
            token = credentials[0].get('value').get('Token')
            self.token = token.get('name')
            self.leas_time = token.get('leaseTime')
        except:
            print('Could not get auth token from', credentials)
            return
        print('Login sucessful')
        self.last_login = datetime.now()

    def get_abilities(self):
        """https://IPC_IP/api.cgi?cmd=GetAbility&token=TOKEN"""
        response = post(self.url,
                        path='api.cgi',
                        params={'cmd': 'GetAbility',
                                'token': self.token})
        return response

    def get_photo(self):
        """https://192.168.1.238/cgi-bin/api.cgi
           ?cmd=Snap&channel=0 &rs=flsYJfZgM6RTB_os&token=TOKEN"""
        parms = {'cmd': 'Snap',
                 'channel': 0,
                 'rs': random_key(16),  # 'flsYJfZgM6RTB_os',
                 'token': self.token}
        response = post(self.url,
                        path='api.cgi',
                        params=parms)
        return response

    def take_photo(self, path=Path('/tmp')):
        filename=datetime.now().strftime('snap_%Y%m%d-%H:%M:%S.png')
        file_path = Path(path, filename)
        img = self.get_photo()
        if img and assert_file_type(img, 'image/jpeg'):
            with file_path.open('wb') as img_file:
                img_file.write(img)
            return file_path


if __name__ == '__main__':
    r1 = reolink('http://strudeviken.hetsa.nu:18080',
                 'spanare', 'utsiktKanonvallen')
    r1.do_login()
    # cando = r1.get_abilities()
    filename = r1.take_photo()

    if filename:
        s3_bucket = 'nikwik-photos'
        target_path = Path('PhotoAlbum/strudeviken', filename.name)
        upload_to_s3(filename.as_posix(), s3_bucket, target_path.as_posix())

