#!/usr/bin/env python

import sys
import logging
import logging.config
import elb


def main():
    kwargs = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kwargs)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
    elb.get_instances("facedetect-worker")


if __name__ == '__main__':
    main()
