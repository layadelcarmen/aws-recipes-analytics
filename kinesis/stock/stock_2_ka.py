#!/usr/bin/env python3

import os
import argparse
import datetime
import time
import json
import random
import signal


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
    return {
        'event_time': datetime.datetime.now().isoformat(),
        'ticker': random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV']),
        'price': round(random.random() * 100, 2)
    }


def save_data(file_path, f_prefix, f_id_fmt, f_suffix, cnt_lines):
    data_path = time.strftime(f"{file_path}/{f_prefix}_{f_id_fmt}{f_suffix}")
    with open(data_path, 'a') as data_file:
        for line in range(cnt_lines):
            data = get_random_data()
            json.dump(data, data_file)
            data_file.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('f_prefix', help='prefix of file names')
    parser.add_argument('cnt_lines', help='amount of lines per addition', type=int)
    args = parser.parse_args()
    file_path = os.environ.get('DATA_PATH')
    f_id_fmt = os.environ.get('FILEID_FORMAT')
    f_suffix = os.environ.get('FNAME_SUFFIX')
    wait4gen = int(os.environ.get('WAIT4GEN'))
    signal_handler = SignalHandler()
    while signal_handler.can_run():
        save_data(file_path, args.f_prefix, f_id_fmt, f_suffix, args.cnt_lines)
        time.sleep(wait4gen)
