import logging
import os.path

channel = "#elb-bot"
username = "elb-bot-user"
hookaddress = "https://COMPANY.slack.com/services/hooks/incoming-webhook?token=TOKEN"
autoscale_group_name = "autoscale_group_name"
loglevel = logging.INFO


if os.path.isfile("config_dev.py"):
    try:
        from config_dev import *
    except ImportError as e:
        pass
