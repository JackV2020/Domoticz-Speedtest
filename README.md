This plugin creates and updates 5 Custom Sensors for the next speeds : 

 - ping
 - uplink
 - downlink
 - upload file
 - download file

The plugin also creates a room with the name you enter for your hardware item.

Updates are done every 5 minutes and each update takes about a minute.

Since this minute would cause a hanging Domoticz the plugin does not get the data it itself.
The plugin starts a detached process which gets the data and posts it back.
To enable this posting of data please go in Domoticz to Setup > Settings > Local Networks > and add the IP address of your Domoticz host.

To install the plugin you need to get the contents of the zip file speedtest.zip

On a Raspberry Pi you could :

Start a terminal and go to your plugins folder and the next command will download a zip file, unpack and remove the zipfile : 

    wget https://raw.githubusercontent.com/JackV2020/Domoticz-Speedtest/main/speedtest.zip && unzip speedtest.zip && rm speedtest.zip

Now to get it into Domoticz restart your domoticz like :

    sudo systemctl restart domoticz

After this you can add a device of the Type 'Jacks Speedtest'.

When you do not like the Type name 'Jacks Speedtest' feel free to edit plugin.py and modify it before you actually add your hardware.


Thanks for reading and enjoy.
