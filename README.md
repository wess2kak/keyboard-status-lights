# keyboard-status-lights
Blink the keyboard status lights based on hardware device activity


## Usage
`sudo ./kb_leds.py <list of devices separated by spaces>`

Current devices available to monitor include:

 storage

 wireless_rx

 wireless_tx

 ethernet_rx

 ethernet_tx

 cpu_temp

 cpu_usage

cpu_temp and cpu_usage are threshold based, and they require a threshold in the format

`cpu_temp=50`


## Examples

`sudo ./kb_leds.py cpu_usage=50 ethernet_rx wireless_rx`

`sudo ./kb_leds.py wireless_rx wireless_tx storage`

`sudo ./kb_leds.py ethernet_rx ethernet_tx`
