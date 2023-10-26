#!/usr/bin/env python3

import os
import argparse
import datetime
import time
import json
import random
import signal
import boto3
from botocore.config import Config


class SignalHandler:
    shutdown_requested = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.request_shutdown)
        signal.signal(signal.SIGTERM, self.request_shutdown)

    def request_shutdown(self, *args):
        print('Request to shutdown received, stopping')
        self.shutdown_requested = True

    def can_run(self):
        return not self.shutdown_requested


def get_random_data():
    current_temperature = round(10 + random.random() * 170, 2)
    if current_temperature > 160:
        status = 'ERROR'
    elif current_temperature > 140 or random.randrange(1, 100) > 80:
        status = random.choice(['WARNING','ERROR'])
    else:
        status = 'OK'
    return {
        'sensor_id': random.randrange(1, 100),
        'current_temperature': current_temperature,
        'status': status,
        'event_time': datetime.datetime.now().isoformat()
    }


def send_data(stream_name, kinesis_client):
    data = get_random_data()
    partition_key = str(data['sensor_id'])
    kinesis_client.put_record(
        StreamName=stream_name,
        Data=json.dumps(data).encode(),
        PartitionKey=partition_key
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_stream', help='output data stream')
    args = parser.parse_args()
    AWS_REGION = os.environ.get('AWS_REGION')
    WAIT4GEN = int(os.environ.get('WAIT4GEN'))
    my_config = Config(
        region_name = AWS_REGION,
        signature_version = 'v4',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    kinesis_client = boto3.client('kinesis', config=my_config)
    signal_handler = SignalHandler()
    while signal_handler.can_run():
        send_data(args.data_stream, kinesis_client)
        time.sleep(WAIT4GEN)
