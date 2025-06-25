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
import opcua
import sys

loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)

stop = False
read_time = 1.05

def sniffer_ble():
    # OPC server setup
    server = opcua.Server()
    server.set_server_name("BLEdata")
    server.set_endpoint("opc.tcp://127.0.0.1:4841")

    # Security policy and settings
    #server.load_certificate("server_cert.pem")
    #server.load_private_key("server_key.pem")
    #server.set_security_policy([opcua.ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,])
    server.set_security_policy([opcua.ua.SecurityPolicyType.NoSecurity,])

    # Register the OPC UA namespace
    idx = server.register_namespace("http://127.0.0.1:4841")
    server.start()

    # Setup nodes
    objects = server.get_objects_node()
    BLEsniffer = objects.add_object(idx, "BLEdata")

    # Add power consumption variable node and set it to write mode
    device_id = ""
    devices = dict()
    # Optimise this to read a csv file containing the Smart plug's MAC addresses
    while device_id != "q":
        device_id = input("Tap the MAC address of the devices to be read (enter 'q' when finished): ")
        if device_id != "q":
            # Add power
            power_conso = BLEsniffer.add_variable(idx, "Power_Conso_"+device_id, 0)
            power_conso.set_writable(writable=True)
            # Add voltage
            voltage = BLEsniffer.add_variable(idx, "Voltage_"+device_id, 0)
            voltage.set_writable(writable=True)
            
            devices[device_id] = [power_conso, voltage]
        
    print(devices)
    # Wait a few seconds to give wireshark time to save the packets into the .pcapng file
    time.sleep(4)

    # Path to pcapng file
    pcap_file ='live_capture.pcapng'
    
    while True:
        # Start capturing
        cap = pyshark.FileCapture(pcap_file,eventloop=loop,display_filter='btatt.handle==0x0014', keep_packets=False)

        # Read each packet inside cap file
        for pkt in cap:
            try:
                # Get the Device (Smart Plug) MAC Address
                device_address = pkt.btle.peripheral_bd_addr

                # Since the packet value contains all values in Hexadecimal separated by a ':',
                # when can convert it into a list and then isolate the values that interest us
                values_hex = pkt.btatt.value.split(':')

                # Get timestamp
                timestamp = pkt.sniff_time.replace(microsecond=0)

                # Get Voltage (in V)
                value_bytes = bytes.fromhex(values_hex[8]) # Convert into bytes
                voltage = int.from_bytes(value_bytes, byteorder='little') # little endien order

                # Power (in W)
                value_bytes = bytes.fromhex(values_hex[6]+values_hex[7])
                power = int.from_bytes(value_bytes, byteorder='big')/1000 # big endien order

                # ---- Running OPC UA variable writing ----
                # Set power_conso value for this specific MAC
                devices[device_address][0].set_value(power)
                # Set voltage value for this specific MAC
                devices[device_address][1].set_value(voltage)
                
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
    """
    Used for allowing the user to change the 'read_time' reading frequency
    on the run when the 'delete' button is pressed
    """
    global stop, read_time
    if key == Key.delete:
        stop = True
        try:
            read_time = float(input("Change read time value to: "))
        except ValueError:
            pass
        stop = False
        key = None

def quit_program(key):
    if key == Key.x:
        sys.exit()

def key_listener():
    # Collect all event until released
    with Listener(on_press = change_read_time) as listener:   
        listener.join()

if __name__ == "__main__":
    Thread(target=key_listener).start()
    Thread(target=sniffer_ble, daemon = True).start()
    
    
