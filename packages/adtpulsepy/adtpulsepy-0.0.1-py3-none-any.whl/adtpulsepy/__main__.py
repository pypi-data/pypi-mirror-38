#!/usr/bin/python
"""
ADT Pulse CLI - An ADT Pulse alarm Python library command line interface.
"""

import logging
import argparse
import adtpulsepy

_LOGGER = logging.getLogger('adtpulse_cli')


def setup_logging(log_level=logging.INFO):
    """Set up the logging."""
    logging.basicConfig(level=log_level)
    fmt = ("%(asctime)s %(levelname)s (%(threadName)s) "
           "[%(name)s] %(message)s")
    colorfmt = "%(log_color)s{}%(reset)s".format(fmt)
    datefmt = '%Y-%m-%d %H:%M:%S'

    # Suppress overly verbose logs from libraries that aren't helpful
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('aiohttp.access').setLevel(logging.WARNING)

    try:
        from colorlog import ColoredFormatter
        logging.getLogger().handlers[0].setFormatter(ColoredFormatter(
            colorfmt,
            datefmt=datefmt,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        ))
    except ImportError:
        pass

    logger = logging.getLogger('')
    logger.setLevel(log_level)


def get_arguments():
    """Get parsed arguments."""
    parser = argparse.ArgumentParser("AbodePy: Command Line Utility")

    parser.add_argument(
        '-u', '--username',
        help='Username',
        required=True)

    parser.add_argument(
        '-p', '--password',
        help='Password',
        required=True)

    return parser.parse_args()

def call():
    """Execute command line helper."""
    args = get_arguments()


    log_level = logging.DEBUG


    setup_logging(log_level)
    try:
        adt = adtpulsepy.ADTPulse(username=args.username,
                                  password=args.password,
                                  auto_login=True)
        _LOGGER.info("Alarm status is : %s", adt.alarm.status)
        for sensor in adt.alarm.sensors:
            _LOGGER.info("Sensor %s", sensor.name)
            _LOGGER.info("Status %s", sensor.status)
    except adtpulsepy.ADTPulseException as exc:
        _LOGGER.error(exc.message)

def main():
    """Execute from command line."""
    call()


if __name__ == '__main__':
    main()
