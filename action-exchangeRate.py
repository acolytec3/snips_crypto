#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import ccxt
import io
import coinList

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

marketName = ''
exchange = ''

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
	try:
		rate = exchange.fetch_ticker(baseCurrency+'/'+quoteCurrency)['info']['spot']['data']['amount']
	        return 'One ' + coinList.coins[baseCurrency] + ' is equal to ' + rate + ' in ' + coinList.coins[quoteCurrency]
	except ccxt.errors.ExchangeError:
		return "That exchange rate is not available on this exchange"
	except:
		return 'That data is not currently available'

def exchangeRate_callback(hermes, intentMessage):
        message = exchangeRate(hermes, intentMessage)
        hermes.publish_end_session(intentMessage.session_id, message)


if __name__ == "__main__":
#	config = read_configuration_file(CONFIG_INI)
	exchange = ccxt.coinbase()
        with Hermes("local:1883") as h:
                h.subscribe_intent("konjou:exchangeRate",exchangeRate_callback).start()











