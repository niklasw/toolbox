#!/usr/bin/env python3

import json
import requests
import uuid

SRV = 'http://ecm:9000'


def submit(task, payload, server_url=SRV):
    url = '/'.join((server_url, task.strip('/')))
    try:
        r = requests.post(url, json=payload)
    except requests.HTTPError:
        print('POST failed')
    if r.status_code != 200:
        print(f'POST failed with status {r.status_code}')
    else:
        print(f'Response from {url} was {r.json()}')
        return r.json()


def fake_id():
    return uuid.uuid1().__str__()


task_name = 'StartSimulation'
session_id = f'equa-internal.{fake_id()}'
job_id = fake_id()
task_id = fake_id()

payload_info = {'model':       'building_1',
                'engineer':    'niklas',
                'customer':    'equa.se',
                'description': 'no description',
                'simType':     'cfd',
                'id':          task_id}

payload = {'session_id':  session_id,
           'job_id':      job_id,
           'task_id':     task_id,
           'info':        json.dumps(payload_info)}

payload_as_json = json.dumps(payload).encode()

print(payload_as_json.decode())

submit(f'esbo/{task_name}', payload)
