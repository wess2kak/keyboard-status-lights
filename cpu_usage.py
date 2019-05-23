def get_cpu_usage():
    idle_time_initial = 0
    active_time_initial = 0
    with open('/proc/stat', 'r') as f:
        lines = list(f)
        for line in lines:
            active_time = line.split()
            idle_time_initial = int(active_time[4])
            del active_time[0]  # cpu name
            del active_time[4]  # idle
            for time in active_time:
                active_time_initial += int(time)
            break

    while True:
        active_time_running = 0
        with open('/proc/stat', 'r') as f:
            line = list(f)[0].split()
            idle_time = int(line[4])
            del line[0]  # cpu name
            del line[4]  # idle
            for time in line:
                active_time_running += int(time)
            active_time_delta = active_time_running - active_time_initial
            time_spent_working = active_time_delta - (idle_time - idle_time_initial)
            usage = ((time_spent_working / active_time_delta) * 100) if active_time_delta else 0
            yield usage
            active_time_initial = active_time_running
            idle_time_initial = idle_time
