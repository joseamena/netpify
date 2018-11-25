import logging
import os
import argparse
import fcntl
import asyncio

import configuration
import data_capture
import netpify_service

LOG_FILE_PATH = 'netfipy.log'
PID_FILE = 'netpify.pid'
PIPE_PATH = '/tmp/netpify_pipe'

stop = False

parser = argparse.ArgumentParser(prog='IoTMeter')
parser.add_argument('--reload', action='store_true',
                    default=False,
                    dest='reload',
                    help='reload configuration',
                    required=False)

parser.add_argument('-xc', action='store',
                    dest='cmd',
                    help='Execute command')

parser.add_argument('--configurator', action='store_true',
                    default=False,
                    dest='configurator',
                    help='run configuration helper script',
                    required=False)


def reload():
    pass


def execute_command(command):
    wp = open(PIPE_PATH, 'w')
    wp.write(command)
    wp.close()


@asyncio.coroutine
def netpifier():
    logging.info("Starting")
    global stop
    count = 0
    while not stop:

        time_interval = 1
        if 'time_interval' in configuration.config:
            time_interval = configuration.config['time_interval']

        yield from asyncio.sleep(1)
        count += 1
        if count == time_interval:
            data = data_capture.capture(100)
            netpify_service.send_data(data)
            count = 0


def event_handler():
    global stop
    while not stop:
        fifo = open(PIPE_PATH, 'r')
        data = fifo.read()

        if data == "stop":
            stop = True

        print("read data %s" % data)
        fifo.close()


    print("exiting event handler")

@asyncio.coroutine
def read(loop):
    yield from loop.run_in_executor(None, event_handler)
    print("read done")



if __name__ == "__main__":
    args = parser.parse_args()

    logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG)
    print("Netpify")

    if args.configurator:

        exit(0)

    if args.reload:
        reload()
        logging.info("Reloading configuration")
        exit(0)

    if args.cmd is not None:
        logging.info("Executing command: %s", args.cmd)
        execute_command(args.cmd)
        exit(0)

    fp = open(PID_FILE, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print("Another instance is running")
        exit(-1)

    path = PIPE_PATH
    try:
        os.mkfifo(path)

    except OSError as e:
        logging.warning("failed to create pipe: %s %s", path, e)
        exit(0)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.wait([
                netpifier(),
                read(loop)
            ])
        )
        # yield from loop.run_in_executor(None, event_handler)
        # loop.run_forever()
    except KeyboardInterrupt:
        logging.debug("keyboard interrupt")
    finally:
        logging.debug("terminating program")
        loop.close()
