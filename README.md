# Voltcraft-SEM6000-BTLE-Sniffing
  Repository containing nRF52840 dongle files for Sniffing BTLE data with Wireshark. <br/>
  I used the official guide of the nRF52840 dongle from Nordic Semiconductior and its files as base and I added a guide to sniff data from a Voltcraft SEM6000 BT plug.

## How to Set Up 
  You can find a How to setup guide in french at the [doc/Guide - Bluetooth LE Sniffing - FR.docx](https://github.com/GlennSR/Voltcraft-SEM6000-BT-LE-Sniffing/blob/master/doc/Guide%20-%20Bluetooth%20LE%20Sniffing.docx) path.<br/>
  Below is a english translation of this guide

## Introduction
  This document shows how to configure the nrf52840 dongle to perform BT Sniffing between a central device and a peripheral, which will be considered here as a phone with the Voltcraft SEM6000 App and a Voltcraft SEM6000 power consumption measurement plug.

## What do you need
-	Dongle nRF52840 or nRF52840 DK
-	Voltcraft SEM6000 Smartplug
-	Cellphone with Voltcraft SEM6000 App
-	Wireshark v3.4.1 or later
-	Python v3.6 or later (v3.9.8 recommended)
-	nRF Connect for Desktop Software

## Installation
  Download the firmware "nRF Sniffer for Bluetooth LE v4.x" or later and extract the files to a folder of your choice. In the following sections, this folder will be referenced as *Sniffer_Software.*

## Program the dongle
  Connect the nRF52840 Dongle or DK to the PC and open the nRF Connect for Desktop software, then follow the steps:<br/>
	Open the "Programmer" tool.<br/>
  ![image](https://github.com/user-attachments/assets/c088a491-8071-48f3-829c-4a45a5190877)<br/>

  Select the device on the list<br/>
  ![image](https://github.com/user-attachments/assets/48d87650-0771-4eb9-8898-ce9713ea1157)

  Then, locate the firmware HEX file for your DK or dongle by clicking on "Add file > Browse"<br/>
  All firmware HEX files are located in *Sniffer_Software/hex/*. Use the suitable file for your DK or dongle:<br/>
  ![image](https://github.com/user-attachments/assets/587d829e-bab3-440c-88d5-fd058d0dac88)<br/>
  ![image](https://github.com/user-attachments/assets/9532e9da-aa0e-49df-a4cb-f20a896b66d5)<br/>

  Once you added the *.hex* file to the list, click on "Write" to download it to the dongle.<br/>
  ![image](https://github.com/user-attachments/assets/b7d5051f-7ecd-4bbb-a895-aae25afe4026)<br/>

  If everything was done properly, the device name on the "Select Device" list will change to "nRF Sniffer for Bluetooth LE"<br/>
  ![image](https://github.com/user-attachments/assets/a547d0dc-0f00-4a67-9a1e-f9bdfbc4ef87)<br/>
  You can close nRF Connect for Desktop.

  The flowing section was copied from the 2.2 sector on the [nRF_Sniffer_BLE_UG_v4.0.0.pdf](https://docs.nordicsemi.com/bundle/nrfutil_ble_sniffer_pdf/resource/nRF_Sniffer_BLE_UG_v4.0.0.pdf) official document from Nordic Semiconductor.
  
  ## Installing the nRF Sniffer capture tool
The nRF Sniffer for Bluetooth LE software is installed as an external capture plugin in Wireshark.
To install the nRF Sniffer capture tool, complete the following steps:
1. Install the Python requirements:<br/>
  a) Open a command window in the *Sniffer_Software/extcap/* folder.<br/>
  b) Type *pip3 install -r requirements.txt* to install the requirements.<br/>
  c) Close the command window.<br/>
2. Copy the nRF Sniffer capture tool into Wireshark's folder for personal external capture plugins:<br/>
  a) Open Wireshark.<br/>
  b) Go to **Help > About Wireshark** (on Windows or Linux) or **Wireshark > About Wireshark** (on macOS).<br/>
  ![image](https://github.com/user-attachments/assets/70a742e8-f792-4afd-98e2-7e1fed74f6fa)<br/>
  c) Select the **Folders** tab.<br/>
  d) Double-click the location for the **Personal Extcap path** to open this folder.<br/>
  ![image](https://github.com/user-attachments/assets/ba8749fd-5010-4e1d-af71-88d3b20623dc)<br/>
  e) Copy the contents of the Sniffer_Software/extcap/ folder into this folder.<br/>
  ![image](https://github.com/user-attachments/assets/c86fdd18-0112-4ac0-86ef-1c85182212b8)<br/>
3. Make sure that the nRF Sniffer files can be run correctly:<br/>
  a) Open a command window in Wireshark's folder for personal external capture plugins.<br/>
  b) Run the nRF Sniffer tool to list available interfaces.<br/>
     On Windows, type *nrf_sniffer_ble.bat --extcap-interfaces*. On macOS or Linux, type *nrf_sniffer_ble.sh --extcap-interfaces*.<br/>
     You should see a series of strings, similar to what is shown in the following screenshot.<br/>
  ![image](https://github.com/user-attachments/assets/e1f20289-eddf-42dc-9192-c998f09dd7bf)<br/>
  c) If the previous step returned an error, verify that Python 3 is accessible.
     On Windows, enter *python --version*. On macOS or Linux, enter *python3*. If the command cannot be found or the version is wrong, make sure that Python v3.6 or later is in your path and that it is the first Python version in the path.<br/>
  d) For macOS or Linux: Verify that the *nrf_sniffer_ble.sh* file has the `x` permission.<br/>
     If the `x` permission is missing, add it using *chmod +x nrf_sniffer_ble.sh*.<br/>
4. Enable the nRF Sniffer capture tool in Wireshark:<br/>
  a) Refresh the interfaces in Wireshark by selecting **Capture > Refresh Interfaces** or pressing **F5**.<br/>
    You should see that nRF Sniffer is displayed as one of the interfaces on the start page.<br/>
  b) Select **View > Interface Toolbars > nRF Sniffer for Bluetooth LE** to enable the nRF Sniffer interface.<br/>
  ![image](https://github.com/user-attachments/assets/32086e5c-402d-490a-b01d-648dd174592c)<br/>
  You can also add a profile in Wireshark for displaying the data recorded by the nRF Sniffer for Bluetooth LE in a convenient way. Follow the steps on the 2.3 section of the official document

## Capture Voltcraft BTLE packets with nRF52840 and Wireshark
Finally, to capture the BTLE packets exchanged between the app and the plug, on Wireshark select *nRF Sniffer for Bluetooth LE COMX* interface and click *Capture* at the top left.<br/>
![image](https://github.com/user-attachments/assets/bd2258cf-4490-44f1-a1cf-572f8841fee4)<br/>
The capture window will open and all the BT packets near the dongle will be displayed, now you need to filter them to show just the packets from the smartplug.<br/>
First, connect the plug to the phone using the app. Then, in the Wireshark *Device* list select "Voltcraft ... " , if it does not appear, close the app on the mobile and do *Refresh*, then reopen the app, repeat this until the device is displayed in the list.<br/>
![image](https://github.com/user-attachments/assets/c7faec42-5904-463e-b5ad-e74092550803)<br/>
Once the device has been selected, you will see several packets of the type *LE LL* which are advertisement packets emitted by the plug but which do not contain the consumption values that we need.<br/>
The packages that contain these values are of type *ATT*, if they are not present in the list, close the app on the mobile and reopen it, repeat this until you see the packets in the list.<br/>
![image](https://github.com/user-attachments/assets/b033459c-4fdf-42e8-ae29-21fee917ab2a)<br/>
The *Rcvd Handle Value Notification package, Handle 0x0014* contains the consumption values in Hexadecimal format.<br/>
(Optional) Apply the **BTATT** filter to display only *ATT* packages in the list.<br/>
![image](https://github.com/user-attachments/assets/1182362e-14f7-427a-947b-d3016348985d)<br/>
To capture packets from other Voltcraft plugs, you will need one dongle per plug, then, on Wireshark, select a *Device* for each *interface* (dongle port).

## Python script to send the BT LE data to Node-Red on OPCUA
Since my main objective was to send the consumption values to a Node-Red flow to be later saved on a database, I created a Python program that sends these info via a OPCUA server.<br/><br/>
A Python script [capture_wireshark_ble.py](https://github.com/GlennSR/Voltcraft-SEM6000-BT-LE-Sniffing/blob/master/Python%20files/capture_wireshark_ble.py) has been written to allow reading of *ATT, Handle 0x0014* packets from Wireshark with power consumption information.<br/>
Before running this script, open a command prompt in the folder containing the python script and type the command `wireshark --update-interval 25 -i COM<X>-4.4 -k -w live_capture.pcapng` replacing <X> with the port number of the connected device, for more details on how to run this command with multiple dongles, see the python script.<br/>
This command will launch Wireshark and will start capturing the BTLE packets and saving them in a file called *live_capture.pcapng*. Filter the packets using the Device list to show only the smartplug's packets and check that the *ATT* packets are present.<br/>
After that, you need to launch the python script with the IDE of your choice, the script will open the *.pcapng* file, read only the *ATT, Handle 0x0014* packets (Consumption information), open an OPCUA server and publish the information on this server.<br/>
![image](https://github.com/user-attachments/assets/2ae98451-ae43-4f69-97b9-f9a4dde2f9cf)

## Android Emulator with Virtual Machine
The problem with using a cellphone to open the Voltcraft app is that if we close the app the data is no longer exchanged.
To solve this problem, we could emulate an Android device with the app that works exactly as a cellphone/tablet and that won't stop communicating with the smartplug. To do that, we need to create a VM with bluetooth. <br/>
The VM was created using Oracle VirtualBox, an Android ISO and the bluetooth driver was installed using a USB-Bluetooth Adapter. The compatible USB adapters that I recommend are:<br/>
-	EDIMAX BT-8500  [Buy here](https://www.conrad.fr/fr/p/edimax-bt-8500-cle-bluetooth-5-0-2266203.html)
-	Renkforce 4.0 +EDR [Buy here](https://www.conrad.fr/fr/p/cle-bluetooth-4-0-edr-renkforce-3-mbit-s-10-m-1491408.html)<br/>

Follow the video below to know how to emulate an Android with the Voltcraft SEM6000 app.<br/>
#### [VIDEO TUTORIAL](https://www.youtube.com/watch?v=CJZ1dVJn46s)







