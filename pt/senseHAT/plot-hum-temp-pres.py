from time import sleep
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from sense_hat import SenseHat

time_step=0.1 #seconds
samples=16
precision=2 #number of decimal digits
humidity_list = [0 for x in range(0,samples)]
temperature_list = [0 for x in range(0,samples)]
pressure_list = [0 for x in range(0,samples)]

sense = SenseHat()


gs = gridspec.GridSpec(2,2)
plt.ion()
fig = plt.figure()
fig.text(0.5, 0.04, r'$\Leftarrow$ rolling samples', ha='center', va='center')

def collect_humidity() -> None:
    # gives relative humidity in percentage terms
    humidity = sense.get_humidity()
    del humidity_list[0]
    humidity_list.append(round(humidity,precision))
    #print(humidity_list)

def collect_temperature() -> None:
    # gives temperature in degrees forenheit
    temperature = sense.get_temperature()
    del temperature_list[0]
    temperature_list.append(round(temperature,precision))
    #print(temperature_list)

def collect_pressure() -> None:
    # gives pressure in milli bars
    pressure = sense.get_pressure()
    del pressure_list[0]
    pressure_list.append(round(pressure,precision))
    #print(temperature_list)

def update_subplot(x_pos,y_pos,data, title, ylabel) -> None:
    ax = plt.subplot(gs[x_pos,y_pos])
    ax.clear()
    ax.plot(data, 'ro', data, 'k')
    xticks = [x for x in range(0,samples+1,2)]
    ax.axis((xticks[0],xticks[-1],
              0.9*min(data), 1.1*max(data)
              ))
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    #ax.set_xlabel(r'$\Leftarrow$ rolling samples')
    ax.grid(True)
    ax.set_xticks(xticks)
    labels = [x-(samples-1) for x in xticks]
    labels[0] = 'oldest'
    labels[-1] = 'latest'
    ax.set_xticklabels(labels, rotation=90)
    fig.canvas.draw()
    fig.canvas.flush_events()
    
while True:
    collect_humidity()
    update_subplot(0,0,humidity_list,'Humidity','Percentage (%)')

    collect_temperature()
    update_subplot(0,1,temperature_list,'Temperature','Degrees Forenheit')

    collect_pressure()
    update_subplot(1,0,pressure_list,'Pressure','Millibars')
    
    sleep(time_step)

# refs
# https://www.raspberrypi.com/documentation/accessories/sense-hat.html
# https://raspberrytips.com/sense-hat-tutorial-2/