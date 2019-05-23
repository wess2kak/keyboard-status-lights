from time import sleep

def get_storage_activity(interface):
 storage_devices = []
 interface_present = False
 with open('/proc/diskstats', 'r') as f:
  lines = list(f)
  for line in lines:
   storage_devices.append(line.split()[2])
   if line.split()[2] == interface:
    interface_present = True
  if not interface_present:
   return print('Could not find interface: ' + interface)

 ms_spent_doing_io = 0
 while True:
  with open('/proc/diskstats', 'r') as f:
   lines = list(f)
   for line in lines:
    if line.split()[2] == interface:
     line_segments = line.split()
     ms_spent_doing_io = int(line_segments[12])
     break
   yield ms_spent_doing_io

