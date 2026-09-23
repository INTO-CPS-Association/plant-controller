# Termination resistors
When a RS485 bus line becomes long, it is necessary to terminate it with 
120 Ohm resistors. This ensures signal integrity.

What long constitutes is use case dependent. For the Plant Controller 
termination resistors shouldn't be theoretically be necessary unless the line
is longer than 2km. But, if your line is very long, and you are experiencing
problems with the signal to and from parts connected to the RS485 bus, 
connecting termination resistors might help.

The resistors won't be under very heavy load so basic 1/2 watt 5% leaded
resistors will do the trick.