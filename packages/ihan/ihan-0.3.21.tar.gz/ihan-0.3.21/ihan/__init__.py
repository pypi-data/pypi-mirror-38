from __future__ import print_function

from   itertools import chain, islice
import json
from   os.path import expanduser, join
from   random import randint
import subprocess
import sys
from   time import sleep


import requests


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def group(num_items, iterable):
    iterable = iter(iterable)

    while True:
        chunk = islice(iterable, num_items)

        try:
            first_element = next(chunk)
        except StopIteration:
            return

        yield chain((first_element,), chunk)


def send_it(endpoint, api_key, api_secret, logs):
    r = requests.post(endpoint, json={'lines': logs,
                                      'api_key': api_key,
                                      'api_secret': api_secret})
    assert r.status_code == 200, r.status_code
    assert r.json()['lines'] == len(logs), 'Line counts failed to match'


has_binary = lambda s: "\x00" in s or any(ord(x) > 0x80 for x in s) # noqa:E731


def feed_file(filename, from_beginning, batch_size, endpoint, sleep_interval,
              backfill):
    try:
        config_file = join(expanduser("~"), ".ihan/config")
        api = json.loads(open(config_file, 'r').read())
        assert len(api['api_key']) > 10 and len(api['api_secret']) > 10
    except Exception as exc:
        print(exc)
        print("Please run this first: ihan login")
        return

    filename = '/dev/stdin' if filename.strip() == '-' else filename
    # WIP this can't detect the end of a stream when
    # gunzip -c data is being piped in.
    # If filename is /dev/stdin don't use tail, just use
    # something in python to follow stdin.
    if backfill:
        proc = subprocess.Popen(['cat',
                                 filename],
                                stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(['tail',
                                 '--lines=+0' if from_beginning else '-n 1000',
                                 '--follow=name',
                                 '--retry',
                                 '--quiet',
                                 '--silent',
                                 '--sleep-interval=%d' % sleep_interval,
                                 filename],
                                stdout=subprocess.PIPE)

    for n_batch, lines in enumerate(group(batch_size,
                            iter(proc.stdout.readline, ''))):
        eprint('batch: ' + str(n_batch))
        # Don't let a few binary bytes stop this in its tracks.
        try:
            logs = list([l.rstrip().decode('utf-8') for l in lines])
        except (AttributeError, # Python 3
                UnicodeDecodeError) as exc: # Python 2
            eprint('Compressed logs are not supported')
            sleep(randint(30, 60))
            continue

        if  has_binary(''.join(logs)):
            eprint('Compressed logs are not supported')
            sleep(randint(30, 60))
            continue

        while True:
            try:
                send_it(endpoint, api['api_key'], api['api_secret'], logs)
                sleep(0.25) # WIP: Make this optional
                break
            except (KeyError,
                    ValueError,
                    AssertionError,
                    requests.exceptions.ConnectionError) as exc:
                eprint(exc)

                # WIP: Set configuration for this
                _interval = randint(10, 180)
                eprint('Sleeping for ' + str(_interval) + 's')
                sleep(_interval)