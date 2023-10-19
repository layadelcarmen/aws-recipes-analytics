#!/usr/bin/env python3

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

def save_data(file_path, f_prefix, f_suffix, f_id_fmt, cnt_lines):
    data_path = time.strftime(f"{file_path}/{f_prefix}_{f_id_fmt}{f_suffix}")
    with open(data_path, 'a') as data_file:
        for line in range(cnt_lines):
            data = get_random_data()
            json.dump(data, data_file)
            data_file.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='path of the files to generate')
    parser.add_argument('f_prefix', help='prefix of file names')
    parser.add_argument('f_id_fmt', help='strftime format for the file ID')
    parser.add_argument('f_suffix', help='suffix of file names')
    parser.add_argument('cnt_lines', help='amount of lines per addition', type=int)
    parser.add_argument('wait4gen', help='seconds to wait before new generation', type=int)
    args = parser.parse_args()
    signal_handler = SignalHandler()
    while signal_handler.can_run():
        save_data(args.file_path, args.f_prefix, args.f_id_fmt, args.f_suffix, args.cnt_lines)
        time.sleep(args.wait4gen)