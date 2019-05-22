# Polls for network activity and switches on/off keyboard status lights
# Uses the first 3 network interfaces found and assigns them to the LEDs
# in the list kb_leds
from time import sleep
kb_leds = ['numlock', 'capslock', 'scrolllock']
SLEEP_TIME = 1/30 # 30hz is about as fast as it can visibly blink

def switch_led(index, state):
 """Writes 'state' to the corresponding keyboard LED device file"""
 with open('/sys/class/leds/input2::%s/brightness' % kb_leds[index], 'a') as f:
  f.write(state)

interface_total_bytes = {}
with open ('/proc/net/dev', 'r') as f:
 for line in f.readlines()[2:5]: # Add together rx + tx bytes for given interface
  interface_total_bytes[line.split()[0]] = int(line.split()[1]) + int(line.split()[9])

while True:
 with open('/proc/net/dev', 'r') as f:
  lines = list(f)
  for line in lines:
   line_segments = line.split()
   if line_segments[0] in interface_total_bytes.keys():
    total_bytes = int(line_segments[1]) + int(line_segments[9])
    interface_index = list(interface_total_bytes.keys()).index(line_segments[0])
    if total_bytes != interface_total_bytes[line_segments[0]]:
     interface_total_bytes[line_segments[0]] = total_bytes
     switch_led(interface_index, '1') # LED on if bytes incremented
    else:
     switch_led(interface_index, '0') # LED off if bytes did not change
  sleep(SLEEP_TIME)
