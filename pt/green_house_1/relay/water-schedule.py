from datetime import datetime
from time import sleep
from gpiozero import LED
import schedule

#use GPIO16 (pin-36 on RPi5)
aquarium_pump = LED(16)

def water_plants():
    aquarium_pump.on()
    print(f"pump turned on at: {datetime.now().isoformat()}")
    sleep(10)
    aquarium_pump.off()
    print(f"pump turned off at: {datetime.now().isoformat()}")

# Set the time for the function to run
#run_time = datetime.time(hour=13, minute=52, second=0)

# Schedule the job
#schedule.every().day.at("14:50").do(water_plants)
schedule.every(30).minutes.do(water_plants)

# Loop to keep the script running
while True:
    schedule.run_pending()
    sleep(10)
