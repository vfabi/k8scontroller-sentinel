#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @project: k8scontroller-sentinel
    @copyright: © 2021 by vfabi
    @author: vfabi
    @support: vfabi
    @initial date: 2021-09-05 11:23:27
    @license: this file is subject to the terms and conditions defined
        in file 'LICENSE.txt', which is part of this source code package
    @description:
    @todo:
"""

import json
import sys
import requests


class Sender:

    def __init__(self, channel_type='slack', **kwargs):
        if channel_type == 'slack':
            self.channel_type = 'slack'
            self.slack_url = kwargs['slack_url']
            self.slack_channel = kwargs['slack_channel']
        else:
            raise Exception('This channel_type is not implemented.')

    def sendSlack(self, message):
        url = self.slack_url
        message = (message)
        title = ('kubernetes event :zap:')
        slack_data = {
            'username': 'k8scontroller-sentinel',
            'icon_emoji': ':jack_o_lantern:',
            'channel': self.slack_channel,
            'attachments': [
                {
                    'color': '#9733EE',
                    'fields': [
                        {
                            'title': title,
                            'value': message,
                            'short': 'false',
                        }
                    ]
                }
            ]
        }
        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': 'application/json', 'Content-Length': byte_length}
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

    def send(self, message):
        if self.channel_type == 'slack':
            self.sendSlack(message)
