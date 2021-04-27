This Domoticz plugin was developed on a Raspberry Pi and may work on other platforms also.

This plugin creates and updates 5 Custom Sensors for the next speeds : 

 - ping             shows ping response
 - uplink           shows the uplink speed
 - downlink         shows the downlink speed
 - upload file      shows how fast a single file can be uploaded
 - download file    shows how fast a single file can be downloaded

The plugin also creates a room with the name you enter for your hardware item.

Updates are done every 5 minutes and each update takes about a minute.

Since this minute would cause a hanging Domoticz the plugin does not get the data it itself.
The plugin starts a detached process which gets the data and posts it back.
To enable this posting of data please go in Domoticz to Setup > Settings > Local Networks > and add the IP address of your Domoticz host.

The detached process uses speedtest.py from https://github.com/sivel/speedtest-cli which is installed by this plugin for you.

Before installing make sure that the requests module is installed :
sudo apt-get install python3-requests
( When already installed it will skip installation and explain it is already installed )

To install the plugin you need to get the contents in your plugin folder :

On a Raspberry Pi you could :

Start a terminal and go to your plugins folder and the next will get it for you into a speedtest folder : 

 ....../plugins$ git clone https://github.com/JackV2020/Domoticz-Speedtest.git speedtest

later when you want to check for updates you go into the folder and issue git pull :

 ....../plugins/speedtest$ git pull

To get it into Domoticz restart your domoticz like :

    sudo systemctl restart domoticz

After this you can add a device of the Type 'Jacks Speedtest'.

Thanks for reading and enjoy.
