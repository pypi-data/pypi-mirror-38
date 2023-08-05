from __future__ import print_function

from   itertools import chain, islice
from   random import randint
import subprocess
import sys
from   time import sleep

import click
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


def send_it(endpoint, logs):
    r = requests.post(endpoint, json={"lines": logs})
    assert r.status_code == 200, r.status_code
    assert r.json()['lines'] == len(logs), 'Line counts failed to match'


has_binary = lambda s: "\x00" in s or any(ord(x) > 0x80 for x in s)


@click.command()
@click.argument('filename') # /dev/stdin
@click.option('--from-beginning', default=False, type=bool)
@click.option('--batch-size', default=10, type=int)
@click.option('--endpoint', default='https://feed.ihan.ee/feed', type=str)
@click.option('--sleep-interval', default=10, type=int)
def live(filename, from_beginning, batch_size, endpoint, sleep_interval):
    # WIP this can't detect the end of a stream when
    # gunzip -c data is being piped in.
    # If filename is /dev/stdin don't use tail, just use
    # something in python to follow stdin.
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
        except UnicodeDecodeError as exc:
            eprint('Compressed logs are not supported')
            sleep(randint(30, 60))
            continue

        if  has_binary(''.join(logs)):
            eprint('Compressed logs are not supported')
            sleep(randint(30, 60))
            continue

        while True:
            try:
                send_it(endpoint, logs)
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

if __name__ == '__main__':
    live()
