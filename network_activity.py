def get_network_activity(interface, rx_or_tx):
    with open('/proc/net/dev', 'r') as f:
        interface_present = False
        for line in f.readlines():
            if line.split()[0][:2] == interface:
                interface_present = True
        if not interface_present:
            return print('Could not find interface: ' + interface)

        rx_bytes = None
        tx_bytes = None
    while True:
        with open('/proc/net/dev', 'r') as f:
            lines = list(f)
            for line in lines:
                if line[:2] == interface:
                    line_segments = line.split()
                    rx_bytes = int(line_segments[1])
                    tx_bytes = int(line_segments[9])
                    break
            yield tx_bytes if rx_or_tx == 'tx' else rx_bytes
