#!/usr/bin/python3
# Polls for network activity and switches on/off keyboard status lights
# Uses the first 3 network interfaces found and assigns them to the LEDs
# in the list KB_LEDS
from sys import argv
from time import sleep

DEVICES = ['storage', 'wireless_rx', 'wireless_tx', 'ethernet_rx', 'ethernet_tx', 'cpu_temp', 'cpu_usage']
KB_LEDS = ['numlock', 'capslock', 'scrolllock']

if len(argv) < 2:
    print('Use 1 to 3 arguments for devices to watch, in the order\n'
          + ', '.join(KB_LEDS).upper() + '\nPossible devices include:\n ' + '\n '.join(DEVICES))
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


watched_devices = {}
count = 0
for arg in argv[1:]:
    current_arg = arg
    if arg.startswith('cpu'):
        if '=' not in arg or not is_int(arg.split('=')[1]):
            print(arg + ' requires a threshold integer in the format `cpu_usage=50`')
            exit()
        current_arg = arg.split('=')[0]

    if arg.startswith('storage'):
        current_arg = arg.split('=')[0]

    if current_arg in DEVICES:
        watched_devices[count] = {'name': arg.lower()}
        count += 1
    else:
        print(current_arg + ' not a valid device!\nPossible devices include:\n ' + '\n '.join(DEVICES))
        exit()
    if count >= 3:
        break  # only accept up to 3 arguments

SLEEP_TIME = 1 / 30  # 30hz is about as fast as it can visibly blink

# only import required generators
for dev in watched_devices:
    if watched_devices[dev]['name'].startswith('storage'):
        from storage_activity import get_storage_activity

        watched_devices[dev]['gen'] = get_storage_activity(watched_devices[dev]['name'].split('=')[1])

    elif watched_devices[dev]['name'].startswith('wireless') or watched_devices[dev]['name'].startswith('ethernet'):
        from network_activity import get_network_activity

        if watched_devices[dev]['name'].endswith('tx'):
            watched_devices[dev]['gen'] = get_network_activity(
                'wl' if watched_devices[dev]['name'].startswith('w') else 'en', 'tx')
        else:
            watched_devices[dev]['gen'] = get_network_activity(
                'wl' if watched_devices[dev]['name'].startswith('w') else 'en', 'rx')

    elif watched_devices[dev]['name'].startswith('cpu_temp'):
        from temps import get_cpu_temps

        watched_devices[dev]['gen'] = get_cpu_temps()

    elif watched_devices[dev]['name'].startswith('cpu_usage'):
        from cpu_usage import get_cpu_usage

        watched_devices[dev]['gen'] = get_cpu_usage()

# initialize device values and turn off all LEDS
for i in range(3):
    switch_led(i, '0')
for dev in watched_devices:
    watched_devices[dev]['value'] = next(watched_devices[dev]['gen'])
    watched_devices[dev]['state'] = '0'  # off
    watched_devices[dev]['threshold'] = int(watched_devices[dev]['name'].split('=')[1]) if \
        watched_devices[dev]['name'].startswith('cpu') else 0

while True:
    for dev in watched_devices:
        current_value = next(watched_devices[dev]['gen'])

        if watched_devices[dev]['threshold']:  # if the device uses a threshold parameter to decide whether to be on
            if not watched_devices[dev]['value'] == current_value:  # first check if anything changed
                watched_devices[dev]['value'] = current_value  # new value set to the changed value
                if current_value > watched_devices[dev]['threshold']:
                    if not watched_devices[dev]['state'] == '1':
                        switch_led(dev, '1')  # on
                        watched_devices[dev]['state'] = '1'
                else:
                    if not watched_devices[dev]['state'] == '0':
                        switch_led(dev, '0')  # off
                        watched_devices[dev]['state'] = '0'

        else:  # if the device does not use a threshold but simply checks for a change
            if not watched_devices[dev]['value'] == current_value:
                watched_devices[dev]['value'] = current_value
                if not watched_devices[dev]['state'] == '1':
                    switch_led(dev, '1')  # on
                    watched_devices[dev]['state'] = '1'
            else:
                if not watched_devices[dev]['state'] == '0':
                    switch_led(dev, '0')  # off
                    watched_devices[dev]['state'] = '0'

    sleep(SLEEP_TIME)
