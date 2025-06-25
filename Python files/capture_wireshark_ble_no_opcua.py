"""
Run 'wireshark --update-interval 25 -i COM5-4.4 -k -w live_capture.pcapng'
before running this code, to capture the packets exchanged between the app and the
cellphone app using a nrf52840 dongle on port COM5-4.4, wait until you see the BTATT packets in wireshark GUI
PS: If you want to capture using more than one nrf52840 dongle, just add <-i COM<X>> after the <-i COM5-4.4>
"""
import pyshark
import asyncio
import time
from threading import Thread
from pynput.keyboard import Key, Listener

loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)

stop = False
read_time = 1.05

def sniffer_ble():
    time.sleep(1)

    pcap_file ='live_capture.pcapng'
    while True:
        cap = pyshark.FileCapture(pcap_file,eventloop=loop,display_filter='btatt.handle==0x0014', keep_packets=False)

        for pkt in cap:
            try:
                # Device MAC Address
                device_address = pkt.btle.peripheral_bd_addr
                
                value = pkt.btatt.value.split(':')
                timestamp = pkt.sniff_time.replace(microsecond=0)

                # Voltage (in V)
                value_bytes = bytes.fromhex(value[8])
                voltage = int.from_bytes(value_bytes, byteorder='little')

                # Power (in W)
                value_bytes = bytes.fromhex(value[6]+value[7])
                power = int.from_bytes(value_bytes, byteorder='big')/1000
                
                print(f"Device (MAC): {device_address}")
                print(f"[{timestamp}] Voltage: {voltage} V, Consumption: {power} W\n")
            except AttributeError:
                pass  # ignora pacotes que não têm valor ATT
            except IndexError:
                pass
            while stop:
                time.sleep(0.01)
            time.sleep(read_time)

def change_read_time(key):
    global stop, read_time
    if key == Key.delete:
        exit = False
        while not exit:
            stop = True
            try:
                read_time = float(input("Change read time value to: "))
            except ValueError:
                pass
            stop = False
            key = None
            exit = True

def key_listener():
    # Collect all event until released
    with Listener(on_press = change_read_time) as listener:   
        listener.join()

if __name__ == "__main__":
    Thread(target=key_listener).start()
    Thread(target=sniffer_ble, daemon = True).start()
    
    
