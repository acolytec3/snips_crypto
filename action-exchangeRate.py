#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import ccxt

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

exchange = ccxt.coinbase()

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
        fromCurrency =intentMessage.slots.from_currency[0].slot_value.value.value
        toCurrency = intentMessage.slots.to_currency[0].slot_value.value.value
	rate = exchange.fetch_ticker(fromCurrency+'/'+toCurrency)['info']['spot']['data']['amount']
        return 'One ' + fromCurrency + ' is equal to ' + rate + ' in ' + toCurrency

def exchangeRate_callback(hermes, intentMessage):
        message = exchangeRate(hermes, intentMessage)
        hermes.publish_end_session(intentMessage.session_id, message)


if __name__ == "__main__":
#       config = read_configuration_file(CONFIG_INI)

        with Hermes("192.168.1.16:1883") as h:
                h.subscribe_intent("konjou:exchange_rate",exchangeRate_callback).start()










