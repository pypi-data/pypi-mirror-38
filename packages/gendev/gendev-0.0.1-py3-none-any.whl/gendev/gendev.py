import os
import errno
import fire
import json
import yaml
import shutil
from time import sleep
import logging
import uuid
from boto3 import session
from botocore.exceptions import ClientError
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import subprocess
import psutil
import random


logging.basicConfig(
    format='%(asctime)s|%(name).10s|%(levelname).5s: %(message)s',
    level=logging.WARNING)
log = logging.getLogger('device')
log.setLevel(logging.DEBUG)


DEFINITION_FILE = 'greengo.yaml'
MAGIC_DIR = '.device'
STATE_FILE = os.path.join(MAGIC_DIR, 'device_state.json')

DEPLOY_TIMEOUT = 400  # Timeout, seconds


class GroupCommands(object):
    def __init__(self):
        super(GroupCommands, self).__init__()

        s = session.Session()
        self._region = s.region_name
        if not self._region:
            log.error("AWS credentials and region must be setup. "
                      "Refer AWS docs at https://goo.gl/JDi5ie")
            exit(-1)

        log.info("AWS credentials found for region '{}'".format(self._region))

        self._gg = s.client("greengrass")
        self._iot = s.client("iot")
        self._lambda = s.client("lambda")
        self._iam = s.client("iam")
        self._iot_endpoint = self._iot.describe_endpoint()['endpointAddress']
        self._dynamodb = s.resource('dynamodb')

        try:
            with open(DEFINITION_FILE, 'r') as f:
                self.group = self.group = yaml.safe_load(f)
        except IOError:
            log.error("Group definition file `greengo.yaml` not found. "
                      "Create file, and define the group definition first. "
                      "See https://github.com/greengo for details.")
            exit(-1)
        print(self.group['Device'])
        # self.name = self.group['Group']['name']
        # self._LAMBDA_ROLE_NAME = "{0}_Lambda_Role".format(self.name)

        self.id = ''

        _mkdir(MAGIC_DIR)
        self.state = _load_state()

    def monitor(self):
        if not _state_exists():
            self._create()
        else:
            print(self.state['device'])

    def _create(self):
        deviceTable = self._dynamodb.Table('gen-device')
        self.group['Device']['id'] = str(uuid.uuid4())
        Item=self.group['Device']
        self.state['device'] = Item
        _update_state(self.state)
        deviceTable.put_item(
            Item=Item
        )

def _state_exists():
    return os.path.exists(STATE_FILE)


def _load_state():
    if not _state_exists():
        log.debug("Device state file {0} not found, assume new device.".format(STATE_FILE))
        return {}
    log.debug("Loading device state from {0}".format(STATE_FILE))
    with open(STATE_FILE, 'r') as f:
        return State(json.load(f))


def _update_state(group_state):
    if not group_state:
        os.remove(STATE_FILE)
        log.debug("State is empty, removed state file '{0}'".format(STATE_FILE))
        return

    with open(STATE_FILE, 'w') as f:
        json.dump(group_state, f, indent=2,
                  separators=(',', ': '), sort_keys=True, default=str)
        log.debug("Updated group state in state file '{0}'".format(STATE_FILE))


def _mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if not (exc.errno == errno.EEXIST and os.path.isdir(path)):
            raise


class State(dict):

    def __missing__(self, k):  # noqa
        v = self[k] = type(self)()
        return v


def main():
    fire.Fire(GroupCommands)


if __name__ == '__main__':
    main()

