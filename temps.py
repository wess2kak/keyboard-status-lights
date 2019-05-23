from os import path, listdir


def get_cpu_temps():
    file_to_read = None
    if path.exists('/sys/class/thermal/thermal_zone0'):
        return  # i don't have a computer with this
    elif path.exists('/sys/class/hwmon/'):
        for directory in listdir('/sys/class/hwmon/'):
            with open('/sys/class/hwmon/' + directory + '/name', 'r') as name_file:
                if name_file.read().rstrip() == 'coretemp':
                    for file in listdir('/sys/class/hwmon/' + directory):
                        if file.startswith('temp') and file.endswith('label'):
                            with open('/sys/class/hwmon/' + directory + '/' + file, 'r') as f:
                                if f.read().startswith('Core 0'):
                                    file_to_read = '/sys/class/hwmon/' + directory + '/' + file.split('_')[0] + '_input'
                                    break
    if not file_to_read:
        return print('Could not find temperature interfaces.')

    while True:
        with open(file_to_read, 'r') as f:
            yield int(int(f.read().lstrip()) / 1000)
