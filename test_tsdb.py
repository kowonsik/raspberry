# -*- coding: utf-8 -*-
# test.py

import time
import requests
import json

url = "http://logger-001-4242.keti.stalk.megdatahub.com/api/put"

data = {
    "metric": "foo.bar",
    "timestamp": time.time(),
    "value": 1977,
    "tags": {
       "host": "mypc"
    }
}

ret = requests.post(url, data=json.dumps(data))
print ret.text
