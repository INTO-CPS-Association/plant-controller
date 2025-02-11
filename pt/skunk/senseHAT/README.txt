Steps to install SenseHAT

Add at the end of /boot/firmware/config.txt

#dtoverlay=w1-gpio
dtoverlay=rpi-sense
dtparam=i2c1_baudrate=400000

-------
Installation notes:
---
sense-hat installation issues:
sudo apt install -y python3-sense-hat (works but not "pip install sense-hat" inside virt env)
If installed in virt env, it gives RTIMU moduleerror in python code

Run all senseHAT code outside python virt env.

Plotting
---

Plotting is slow because all the axis is being redrawn frequently.
Instead only update y-axis data.