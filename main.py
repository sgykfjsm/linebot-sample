from flask import Flask, request, abort
# from business_connect.event import send_messages
import json
import os
import requests

app = Flask('__main__')

CHANNEL_ID = os.getenv('CHANNEL_ID')
# CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
CHANNEL_MID = os.getenv('CHANNEL_MID')
HTTPS_PROXY = os.getenv('FIXIE_URL')


@app.route('/linebot/callback', methods=['POST'])
def callback():
    print request.headers
    if request.headers.get('Content-Type') != 'application/json' \
            or 'X-LINE-ChannelSignature' not in request.headers:
        abort(403)

    post_data = request.get_json()
    # debug
    print json.dumps(post_data, indent=4, sort_keys=True)
    for d in post_data.get('result'):
        to = [d['content']['from']]
        to_channel = '1383378250'
        event_type = "138311608800106203"
        content = d['content']
        endpoint = 'https://trialbot-api.line.me/v1/events'
        headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                'X-Line-ChannelID': CHANNEL_ID,
                'X-Line-ChannelSecret': CHANNEL_SECRET,
                'X-Line-Trusted-User-With-ACL': CHANNEL_MID,
                }

        data = json.dumps({
            'to': to,
            'toChannel': to_channel,
            'eventType': event_type,
            'content': content
            })

        proxy = {"https": HTTPS_PROXY}
        res = requests.post(endpoint, data=data, headers=headers, proxies=proxy)

        if res.status_code != 200:
            print res.json().get('statusMessage', '')

        print res.text
        print res.status_code
