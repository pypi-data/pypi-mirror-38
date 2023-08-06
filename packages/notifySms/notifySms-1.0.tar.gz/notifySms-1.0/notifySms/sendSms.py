'''
    This program helps to send sms notification to specified mobile.

    usage :
    1. Using Program to send sms
        python sendSms.py [<Message needs to be sent>]
    2. Using module in other script to nofiy via sms
       from sendSms import send_sms
       send_sms(<msg>,[<To Number>])
'''
import sys
import json
import logging
import base64
import platform
import os
from requests.exceptions import ConnectionError
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.http.http_client import TwilioHttpClient

logging.basicConfig(level=logging.ERROR, format=" [%(asctime)s][%(levelname)s] %(message)s")

CFGFILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
logging.debug("Loading configuration file {} ".format(CFGFILE))

try:
    CONFIG = json.loads(open(CFGFILE).read())
    logging.debug(CONFIG)
except IOError:
    logging.critical("Configuration file not found! \
    Please make sure config.json file is in same directory")
    sys.exit(1)

client = ""
try:
    proxy_client = TwilioHttpClient()
    # assuming your proxy is available via the standard env var https_proxy:
    ## (this is the case on pythonanywhere)
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(base64.b64decode(CONFIG['account']), base64.b64decode(CONFIG['token']), http_client=proxy_client)
except KeyError:
    try:
        client = Client(base64.b64decode(CONFIG['account']), base64.b64decode(CONFIG['token']))
    except TypeError:
        logging.error("Please check your config file as properly base64 encoded content")
except TypeError:
    logging.error("Please check your config file as properly base64 encoded content")

def send_sms(msg_body, to_num=None):
    '''
    This function is used to send message with give mobile number and message
    '''
    try:
        if to_num == None:
            to_num = base64.b64decode(CONFIG['to_default'])
        logging.debug("To : {}, From : {}, Message is : {}".format(to_num, CONFIG['from'], msg_body))
        client.messages.create(to=to_num, from_=CONFIG['from'], body=msg_body)
    except ConnectionError:
        logging.error("Opps !! Check you Internet connection. \n{}".format(sys.exc_info()))
    except TwilioRestException:
        logging.error("Opps!! Check your credentials in config file : \
         {} or server issue \n{}".format(CFGFILE, sys.exc_info()))
    except TypeError:
        logging.error("Please check your config file as properly base64 encoded content")
    except:
        logging.error("Something unexpected happend! Check error \n{}".format(sys.exc_info()))
    else:
        logging.info("Message has been sent sucessfully")

def usage():
    ''' This is the help function to print usage

    This program helps to send sms notification to specified mobile.

    usage :
    1. Using Program to send sms
        python sendSms.py [<Message needs to be sent>]
    2. Using module in other script to nofiy via sms
       from sendSms import send_sms
       send_sms(<msg>,[<To Number>])
    '''

if __name__ == '__main__':
    logging.debug("Inside main function")
    msg = "Default msg : " + str(platform.uname())
    if len(sys.argv) > 1:
        msg = ' '.join(sys.argv[1:])
    else:
        usage()
    send_sms(msg)
