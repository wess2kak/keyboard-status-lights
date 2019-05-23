from os import path, listdir

def get_cpu_temps():
 file_to_read = None
 if path.exists('/sys/class/thermal/thermal_zone0'):
  return # i don't have a computer with this
 elif path.exists('/sys/class/hwmon/hwmon0/'):
  for directory in listdir('/sys/class/hwmon/hwmon0/'):
   if directory.startswith('temp') and directory.endswith('label'):
    with open('/sys/class/hwmon/hwmon0/' + directory, 'r') as f:
     if f.read().startswith('Core 0'):
      file_to_read = '/sys/class/hwmon/hwmon0/' + directory.split('_')[0] + '_input'
      break
 else:
  return print('Could not find temperature interfaces.')

 while True:
  with open(file_to_read, 'r') as f:
   yield int(int(f.read().lstrip()) / 1000)
