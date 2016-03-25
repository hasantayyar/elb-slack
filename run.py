#!/usr/bin/env python

import sys
import logging
import logging.config
import aws


def main():
    kwargs = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kwargs)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)


if __name__ == '__main__':
    main()
