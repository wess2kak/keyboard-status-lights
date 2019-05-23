#!/usr/bin/python3
# Polls for network activity and switches on/off keyboard status lights
# Uses the first 3 network interfaces found and assigns them to the LEDs
# in the list KB_LEDS
from sys import argv
DEVICES = ['storage', 'wireless_rx', 'wireless_tx', 'ethernet_rx', 'ethernet_tx', 'cpu_temp', 'cpu_usage']
KB_LEDS = ['numlock', 'capslock', 'scrolllock']

if len(argv) < 2:
 print('Use 1 to 3 arguments for devices to watch, in the order\n' + ', '.join(KB_LEDS).upper() + '\nPossible devices include:\n ' + '\n '.join(DEVICES))
 exit()

def is_int(n):
 try:
  int(n)
  return True
 except:
  return False

def switch_led(index, state):
 """Writes 'state' to the corresponding keyboard LED device file"""
 with open('/sys/class/leds/input2::%s/brightness' % KB_LEDS[index], 'a') as f:
  f.write(state)

devices_to_watch = {}
count = 0
for arg in argv[1:]:
 if arg.startswith('cpu'):
  if '=' not in arg or not is_int(arg.split('=')[1]):
   print(arg + ' requires a threshold integer in the format `cpu_usage=50`')
   exit()
 if arg.startswith('storage'):
  current_arg = arg.split('=')[0]
 else:
  current_arg = arg
 if current_arg in DEVICES:
  devices_to_watch[count] = {'name': arg.lower()}
  count += 1
 else:
  print(arg + ' not a valid device!\nPossible devices include:\n ' + '\n '.join(DEVICES))
  exit()
 if count >= 3:
  break # only accept up to 3 arguments

from time import sleep
SLEEP_TIME = 1/30 # 30hz is about as fast as it can visibly blink
print(devices_to_watch)

# only import required generators
for dev in devices_to_watch:
 if devices_to_watch[dev]['name'].startswith('storage'):
  from storage_activity import get_storage_activity
  devices_to_watch[dev]['gen'] = get_storage_activity(devices_to_watch[dev]['name'].split('=')[1])
 elif devices_to_watch[dev]['name'].startswith('wireless') or devices_to_watch[dev]['name'].startswith('ethernet'):
  from network_activity import get_network_activity
  if devices_to_watch[dev]['name'].endswith('tx'):
   devices_to_watch[dev]['gen'] = get_network_activity('wl' if devices_to_watch[dev]['name'].startswith('w') else 'en', 'tx')
  else:
   devices_to_watch[dev]['gen'] = get_network_activity('wl' if devices_to_watch[dev]['name'].startswith('w') else 'en', 'rx')
 elif devices_to_watch[dev]['name'].startswith('cpu_temps'):
  from temps import get_cpu_temps
  devices_to_watch[dev]['gen'] = get_cpu_temps()
 elif devices_to_watch[dev]['name'].startswith('cpu_usage'):
  from cpu_usage import get_cpu_usage
  devices_to_watch[dev]['gen'] = get_cpu_usage()

#initialize device values
for dev in devices_to_watch:
 devices_to_watch[dev]['value'] = next(devices_to_watch[dev]['gen'])
 devices_to_watch[dev]['state'] = '0' # off

while True:
 for dev in devices_to_watch:
  current_value = next(devices_to_watch[dev]['gen'])
  if devices_to_watch[dev]['value'] != current_value and devices_to_watch[dev]['state'] != '1':
   switch_led(dev, '1') # on
   devices_to_watch[dev]['state'] = '1'
   devices_to_watch[dev]['value'] = current_value
  elif devices_to_watch[dev]['state'] != '0':
   switch_led(dev, '0') # off
   devices_to_watch[dev]['state'] = '0'
 sleep(SLEEP_TIME)
