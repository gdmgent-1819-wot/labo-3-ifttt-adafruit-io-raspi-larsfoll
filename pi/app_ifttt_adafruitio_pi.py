import random
import sys
import time
from sense_hat import SenseHat
from time import sleep
import requests

sense = SenseHat()

from Adafruit_IO import MQTTClient

ADAFRUIT_IO_KEY = '176cba4c23c74d88a7bc4a68178b8f58'

ADAFRUIT_IO_USERNAME = 'larsfoll'

red = (255, 0, 0)
white = (255, 255, 255)

def connected(client):
    print('Connected to Adafruit IO!  Listening for DemoFeed changes...')
    client.subscribe('DemoFeed')

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    sense.show_message(payload)
    for x in range(5):
        sense.clear(red)
        sleep(1)
        sense.clear(white)
        sleep(1)

def pushed_down():
    print('Down')

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

client.connect()

client.loop_background()

sense.stick.direction_middle = pushed_middle
