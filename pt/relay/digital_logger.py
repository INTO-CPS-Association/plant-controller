from gpiozero import LED
from time import sleep

aquarium_pump = LED(16)

aquarium_pump.on()

while True:
    aquarium_pump.off()
    sleep(600)
    aquarium_pump.on()
    sleep(5)
