from gpiozero import LED
from time import sleep

channel_1 = LED(26)
channel_2 = LED(20)
channel_3 = LED(21)

# Channels are active low which means
#ON - turns off the output
#OFF - turns on the output

channel_1.on()
channel_2.on()
channel_3.on()
sleep(4)
channel_1.off()
channel_2.off()
channel_3.off()
sleep(4)
