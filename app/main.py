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

import os
import asyncio
import logging
import kopf
import pykube
from pykube.exceptions import ObjectDoesNotExist
from helpers import Sender

SLACK_URL = os.getenv('SLACK_URL')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')

logger = logging.getLogger()


@kopf.on.startup()
def configure(settings: kopf.OperatorSettings, **_):
    settings.posting.level = logging.INFO
    settings.watching.connect_timeout = 1 * 60
    settings.watching.server_timeout = 10 * 60
    # settings.posting.enabled = False


@kopf.on.event('', 'v1', 'pods')
def event(event, **kwargs):
    sender = Sender(
        channel_type='slack',
        slack_url=SLACK_URL,
        slack_channel=SLACK_CHANNEL
    )
    api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())

    try:
        namespace = event['object']['metadata']['namespace']
        pod = pykube.Pod.objects(api, namespace=namespace).get_by_name(event['object']['metadata']['name'])
        pod_status_phase = pod.obj['status']['phase']
        if pod_status_phase == 'Failed':
            pod_status_reason = pod.obj['status']['reason']
        else:
            pod_status_reason = None
        logger.info(f'Got pod event. Pod={namespace}/{pod}, phase={pod_status_phase}, reason={pod_status_reason}.')

        if pod_status_reason == 'Shutdown':
            logger.warning(f'Deleting pod {namespace}/{pod}, phase={pod_status_phase}, reason={pod_status_reason}, ready={pod.ready}.')
            pod.delete()
            sender.send(f'*pod:* {namespace}/{pod}\n *status:* {pod_status_phase}\n *reason:* {pod_status_reason}\n *action:* deleted')
    except ObjectDoesNotExist as e:
        logger.warning(f'Pod does not exists. Details: {e}')
    except Exception as e:
        logger.error(f'Exception. Details: {e}')

    api.session.close()


@kopf.on.login()
def login(**kwargs):
    return kopf.login_with_service_account(**kwargs)


def main():
    asyncio.run(kopf.operator(
        # registry=kopf.OperatorRegistry(),
        clusterwide=True,
        standalone=True,
    ))


main()
