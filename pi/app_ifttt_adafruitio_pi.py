import random
import os
import sys
import time
from sense_hat import SenseHat
from time import sleep
import requests

sense = SenseHat()

from Adafruit_IO import Client, MQTTClient, Data

ADAFRUIT_IO_KEY = '176cba4c23c74d88a7bc4a68178b8f58'

ADAFRUIT_IO_USERNAME = 'larsfoll'

ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/cByhjCUEILFL022WIX_nLV'

red = (255, 0, 0)
white = (56, 56, 56)

timer_start = 0
timer_stop = 0

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def connected(client):
    print('Connected to Adafruit IO!  Listening for start-alarm changes...')
    client.subscribe('start-alarm')

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def alarm(client, feed_id, payload):
    global timer_start
    timer_start = time.time()
    os.system('omxplayer bell.mp3 &')
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    sense.show_message(payload, scroll_speed=0.01)
    for x in range(5):
        sense.clear(red)
        sleep(.5)
        sense.clear(white)
        sleep(.5)

def stop_alarm():
    global timer_stop
    timer_stop = time.time()
    reaction_time = timer_stop - timer_start
    reaction_time = round(reaction_time, 2)
    print(reaction_time)
    os.system('kill $(pgrep omxplayer)')
    data = Data(value=reaction_time)
    aio.create_data('stop-alarm', data)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = alarm

client.connect()

client.loop_background()

while True:
    for event in sense.stick.get_events():
        action = format(event.action)
        direction = format(event.direction)
        if direction == 'middle' and action == 'released':
            stop_alarm()
    pass
