#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from lxml import html
import requests

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def airTokenBalance_callback(hermes, intentMessage):
	url = 'https://console.snips.ai/api/login'
	values = {'email': config['secret']['username'], 'password': config['secret']['password']}
	r = requests.post(url,data=values)
	tree = html.fromstring(r.content)
	tokens = tree.xpath('//*[@id="react_div"]/div/header/div[2]/div[2]/a/div/div[1]/text()')
	message = 'Your current snips air token balance is ' + tokens
        hermes.publish_end_session(intentMessage.session_id, message)


if __name__ == "__main__":
	config = read_configuration_file(CONFIG_INI)
        with Hermes("localhost:1883") as h:
                h.subscribe_intent("konjou:airTokenBalance",airTokenBalance_callback).start()











