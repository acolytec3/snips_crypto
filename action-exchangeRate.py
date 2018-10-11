#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from coinmarketcap import Market
import io
import coinDict

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


coins = Market()
coinList = coins.listings()['data']

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

def exchangeRate(hermes, intentMessage):
        quoteCurrency = intentMessage.slots.quoteCurrency[0].slot_value.value.value
        baseCurrency = intentMessage.slots.baseCurrency[0].slot_value.value.value
	print(quoteCurrency)
	print(baseCurrency)

	result = next((x for x in coinList if x['symbol'] == 'BTC'),None)
	rate = coins.ticker(result['id'])['data']['quotes'][config['global']['quote']]['price']
	print(rate)
	try:
	        return 'One ' + coinDict.coins[baseCurrency] + ' is equal to ' + str(round(rate,2)).encode('UTF-8') + ' in ' + coinDict.coins[quoteCurrency]
	except:
		return 'That data is not currently available'

def exchangeRate_callback(hermes, intentMessage):
        message = exchangeRate(hermes, intentMessage)
        hermes.publish_end_session(intentMessage.session_id, message)


if __name__ == "__main__":
	config = read_configuration_file(CONFIG_INI)
        with Hermes("localhost:1883") as h:
                h.subscribe_intent("konjou:exchangeRate",exchangeRate_callback).start()











