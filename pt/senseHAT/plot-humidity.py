# source: http://www.suppertime.co.uk/blogmywiki/2016/11/raspberrypi-sensehat-live-pressure-graphs/

from time import sleep
from queue import Queue
import numpy as np
import matplotlib.pyplot as plt
from sense_hat import SenseHat

sense = SenseHat()
humidity_list = Queue(10)
humidity_list = [0 for x in range(0,9)]

plt.ion()
fig = plt.figure()
plt.subplot(2,1,1)

def humidity():
    # gives relative humidity in percentage terms
    humidity = sense.get_humidity()
    del humidity_list[0]
    humidity_list.append(round(humidity,2))
    print(humidity_list)

def update_plot():
    plt.clf()
    plt.plot(humidity_list, 'ro')
    plt.axis((0,10,
              0.8*min(humidity_list), 1.2*max(humidity_list)
              ))
    plt.xlabel('sample')
    plt.ylabel('')
    fig.canvas.draw()
    fig.canvas.flush_events()
    
while True:
    humidity()
    update_plot()
    sleep(1)
