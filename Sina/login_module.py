#!/usr/bin/env python
# -*- coding: utf-8 -*-
from weibo import *
import requests
app_key = "3561655282"
app_secret = '045767fc5b4503e50ccc7be96c00e871'
call_back = "https://api.weibo.com/oauth2/default.html"
client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=call_back)
with open('accessToken.txt') as f:
    for at in f:
        try:
            url = 'https://api.weibo.com/2/place/poi_timeline.json'
            params= {
                'access_token': at.strip(),
                'poiid': 'B2094650D165ABFB449D',
                'count': 50,
                'page': 1
            }
            req = requests.get(url=url, params=params,verify=True)
            print req.content
        except Exception as e:
            time.sleep(5)
