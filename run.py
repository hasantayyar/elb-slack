#!/usr/bin/env python

import sys
import logging
import logging.config
import elb
import config
import requests

def main():
    kwargs = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': config.loglevel,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kwargs)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(config.loglevel)
    instances = elb.get_instances(config.autoscale_group_name)
    if instances:
      for x, i in enumerate(instances):
        output = "#{} - {}".format((x+1), i.launch_time)
        print(output)
        r = requests.post(config.hookaddress, json={"text": output , "channel": config.channel, "username": config.username})
        print(r.status_code)

if __name__ == '__main__':
    main()
