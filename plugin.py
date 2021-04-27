#
# Title : plugin.py for speedtest-cli
# Author: Jack Veraart
#
#     - Version info
#
#  version 1.0 (2021-05-07) : Initial Version

"""
<plugin key="JacksSpeedtest" name="Jacks Speedtest" author="Jack Veraart" version="1.0">
    <description>
        <font size="4" color="white">Speedtest</font><font color="white">...Notes...</font>
        <ul style="list-style-type:square">
            <li><font color="yellow">This plugin uses speedtest.py which I downloaded from Matt Martz @ https://github.com/sivel.</font></li>
            <li><font color="yellow">Since speedtest.py takes some time to run I created spawn_bash.sh and speedtest.sh to run it as a detached process.</font></li>
            <li><font color="yellow">To enable the detached process to send data back please go to Setup > Settings > Local Networks > and add the IP address of your Domoticz host.</font></li>
            <li><font color="yellow">When you have a Password on your Domoticz, enter an admin Username and Password below so the plugin can create a room with the name you enter above.</font></li>
            <li><font color="yellow">To develop your own plugin...check this web site... <a href="https://www.domoticz.com/wiki/Developing_a_Python_plugin" ><font color="cyan">Developing_a_Python_plugin</font></a></font></li>
        </ul>
    </description>
    <params>

        <param field="Username" label="Username." width="120px" default="view"/>

        <param field="Password" label="Password." width="120px" default="view" password="true"/>

        <param field="Mode6" label="Debug." width="75px">
            <options>
                <option label="True"  value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import sys

#
# Start...
#
PollInterval=10
HeartBeatCounterMax=6*5   # update ecery 10 * 6 * 5 = 300 seconds = 5 minutes
HeartBeatCounter=0

PluginStartUp=0
HomeFolder=''
Username=''
Password=''
Debug=''

MyIPPort=0
LocalHostInfo=''

ImageDictionary={}

speed_ping_id=1
speed_ping_name='Ping'
speed_ping_units='ms'
speed_ping_image='JVCloud'

speed_upload_id=2
speed_upload_name='Up Link'
speed_upload_units='Mbit/s'
speed_upload_image='JVCloud'

speed_download_id=3
speed_download_name='Down Link'
speed_download_units='Mbit/s'
speed_download_image='JVCloud'

speed_single_upload_id=4
speed_single_upload_name='Upload'
speed_single_upload_units='Mbit/s'
speed_single_upload_image='JVCloud'

speed_single_download_id=5
speed_single_download_name='Download'
speed_single_download_units='Mbit/s'
speed_single_download_image='JVCloud'

# --------------------------------------------------------------------------------------------------------------------------------------------------------

class BasePlugin:
    enabled = False
    def __init__(self):

        return

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onStart(self):

        global PluginStartUp
        global Debug

        global HomeFolder
        global Username
        global Password
        global MyIPPort
        global LocalHostInfo
        global piholeAddress

        Debug=Parameters["Mode6"]
#
# self.pollinterval is adviced to be maximum 30 seconds and is interval in which onHeartbeat is called
#
        self.pollinterval = PollInterval

        if Debug == 'Debug':
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()
        else:
            Domoticz.Debugging(0)

        Domoticz.Log('onStart called')

        try:
            HomeFolder=Parameters['HomeFolder']
            Username=Parameters["Username"]
            Password=Parameters["Password"]
#
# Get my own IP port and contruct LocalHostInfo
#
            MyIPPort=GetDomoticzPort()

            LocalHostInfo='http://'+Username+':'+Password+'@localhost:'+MyIPPort
#
# Import all images and build ImageDictionary
#
            ImportImages()
#
# Create the items from the config and delete items which are no longer in the config
#
            CreateDevice(speed_ping_id,speed_ping_name,"Custom",speed_ping_image,'Ping to nearest speedtest host',speed_ping_units,0)

            CreateDevice(speed_upload_id,speed_upload_name,"Custom",speed_upload_image,'Total upload speed',speed_upload_units,0)
            CreateDevice(speed_download_id,speed_download_name,"Custom",speed_download_image,'Total download speed',speed_download_units,0)

            CreateDevice(speed_single_upload_id,speed_single_upload_name,"Custom",speed_single_upload_image,'Upload speed for a single file',speed_single_upload_units,0)
            CreateDevice(speed_single_download_id,speed_single_download_name,"Custom",speed_single_download_image,'Download speed for a single file',speed_single_download_units,0)
#
# (Re-)Create Room
#
#            RoomIdx=CreateRoom(LocalHostInfo, RoomName, Recreate)
            RoomIdx=CreateRoom(LocalHostInfo, Parameters["Name"] , False)
#
# Add all items to Room
#
            AddToRoom(LocalHostInfo,RoomIdx,Devices[speed_upload_id].ID)
            AddToRoom(LocalHostInfo,RoomIdx,Devices[speed_download_id].ID)
            AddToRoom(LocalHostInfo,RoomIdx,Devices[speed_single_upload_id].ID)
            AddToRoom(LocalHostInfo,RoomIdx,Devices[speed_single_download_id].ID)
            AddToRoom(LocalHostInfo,RoomIdx,Devices[speed_ping_id].ID)
#
# And start the action
#
            Domoticz.Heartbeat(PollInterval)

            Domoticz.Log('onStart oke !!')

            PluginStartUp = 1

        except:

            Domoticz.Log('ERROR starting up, ............................'+'Unexpected error: '+ str(sys.exc_info()[0]))

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called")

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onHeartbeat(self):

        global HeartBeatCounter

        Domoticz.Debug("-----onHeartbeat called")

        if PluginStartUp == 1: # Startup was fine

            if HeartBeatCounter == 0:

                Domoticz.Debug("-----onHeartbeat acting")

                StartSpeedTest()

                HeartBeatCounter = HeartBeatCounterMax

            else :

                Domoticz.Debug("-----onHeartbeat counter "+ str(HeartBeatCounter))

                HeartBeatCounter = HeartBeatCounter - 1

# --------------------------------------------------------------------------------------------------------------------------------------------------------

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Log( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Log("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Log("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Log("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Log("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Log("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Log("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Log("Device LastLevel: " + str(Devices[x].LastLevel))
    return

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  File Inspection Routines  ------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetDomoticzPort():
#
# ServiceName should be the same as foldername where domoticz is installed.
#
    ServiceName=HomeFolder.split('/')[-4]
    searchfile = open("/etc/init.d/"+ServiceName+".sh", "r")
    for line in searchfile:
        if ("-www" in line) and (line[0:11]=='DAEMON_ARGS'):
            IPPort=line.split(' ')[2].split('"')[0]
    searchfile.close()
    Domoticz.Debug(' GetDomoticzPort looked in: '+"/etc/init.d/"+ServiceName+".sh"+' and found port: '+str(IPPort))
    return IPPort

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Image Management Routines  -----------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def GetImageDictionary(HostInfo):
#
# HostInfo : http(s)://user:pwd@somehost.somewhere:port
#
    import json
    import requests

    try:
        mydict={}

        url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?type=custom_light_icons'
        username=HostInfo.split(':')[1][2:]
        password=HostInfo.split(':')[2].split('@')[0]

#        Domoticz.Log('....'+url+'....'+username+'....'+password+'....')

        response=requests.get(url, auth=(username, password))
        data = json.loads(response.text)
        for Item in data['result']:
            mydict[str(Item['imageSrc'])]=int(Item['idx'])

    except:
        mydict={}

    return mydict

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def ImportImages():
#
# Import ImagesToImport if not already loaded
#
    import glob

    global ImageDictionary

    ImageDictionary=GetImageDictionary(LocalHostInfo)

    if ImageDictionary == {}:
        Domoticz.Log("ERROR I can not access the image library. Please modify the hardware setup to have the right username and password.")
    else:

        for zipfile in glob.glob(HomeFolder+"CustomIcons/*.zip"):
            importfile=zipfile.replace(HomeFolder,'')
            try:
                Domoticz.Image(importfile).Create()
                Domoticz.Debug("Imported/Updated icons from "  + importfile)
            except:
                Domoticz.Log("ERROR can not import icons from "  + importfile)

        ImageDictionary=GetImageDictionary(LocalHostInfo)

#        Domoticz.Log('ImportImages: '+str(ImageDictionary))

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Device Creation Routines  ------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def CreateDevice(deviceunit,devicename,devicetype,devicelogo="",devicedescription="",sAxis="",InitialValue=0.0):

    if deviceunit not in Devices:

        if ImageDictionary == {}:
            firstimage=0
            firstimagename='NoImage'
            Domoticz.Log("ERROR I can not access the image library. Please modify the hardware setup to have the right Username and Password.")
        else:
            firstimage=int(str(ImageDictionary.values()).split()[0].split('[')[1][:-1])
            firstimagename=str(ImageDictionary.keys()).split()[0].split('[')[1][1:-2]
            Domoticz.Debug("First image id: " + str(firstimage) + " name: " + firstimagename)

        if firstimage != 0: # we have a dictionary with images and hopefully also the image for devicelogo

            try:

                deviceoptions={}
                deviceoptions['Custom']="1;"+sAxis
                Domoticz.Device(Name=devicename, Unit=deviceunit, TypeName=devicetype, Used=1, Image=ImageDictionary[devicelogo], Description=devicedescription).Create()
                Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=str(InitialValue))
                Domoticz.Log("Created device : " + devicename + " with '"+ devicelogo + "' icon and options "+str(deviceoptions)+' Value '+str(InitialValue))
            except:

# when devicelogo does not exist, use the first image found, (TypeName values Text and maybe some others will use standard images for that TypeName.)

                try:
                    Domoticz.Device(Name=devicename, Unit=deviceunit, TypeName=devicetype, Used=1, Image=firstimage, Description=devicedescription).Create()
                    Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=str(InitialValue))
                    Domoticz.Log("Created device : " + devicename+ " with '"+ firstimagename + "' icon and Value "+str(InitialValue))
                except:
                    Domoticz.Log("ERROR Could not create device : " + devicename)
#
# Devices are created with as prefix the name of the Hardware device as you named it during adding your hardware
# The next replaces that prefix, also after every restart so names are fixed
#
    try:

# Note that deviceoptions needs to be a python dictionary so first create a dictionary and fill it with 1 entry

        deviceoptions={}
        deviceoptions['Custom']="1;"+sAxis

        NewName = devicename
        Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=Devices[deviceunit].sValue, Name=NewName, Options=deviceoptions, Description=devicedescription)
    except:
        dummy=1

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateRoom(HostInfo,RoomName, Recreate):
#
# HostInfo : http(s)://user:pwd@somehost.somewhere:port
#
    import json
    import requests

    idx=0

    try:

        username=HostInfo.split(':')[1][2:]
        password=HostInfo.split(':')[2].split('@')[0]

        Domoticz.Debug('Find Room')

        url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?type=plans&order=name&used=true'
        response=requests.get(url, auth=(username, password), timeout=5)
        data = json.loads(response.text)
        if 'result' in data.keys():
            for Item in data['result']:
                if str(Item['Name']) == RoomName:
                    idx=int(Item['idx'])


        if (idx != 0) and Recreate :
            Domoticz.Log('Delete Room')
            url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?idx='+str(idx)+'&param=deleteplan&type=command'
            response=requests.get(url, auth=(username, password), timeout=5)
            idx = 0

        if idx == 0 :

            Domoticz.Log('Create Room')

            url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?name='+RoomName+'&param=addplan&type=command'
            response=requests.get(url, auth=(username, password), timeout=5)
            data = json.loads(response.text)
            idx=int(data['idx'])

    except:
        idx=-1

 #   Domoticz.Log(str(idx))

    return idx
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def AddToRoom(HostInfo,RoomIDX,ItemIDX):
#
# HostInfo : http(s)://user:pwd@somehost.somewhere:port
#
    import json
    import requests

    idx=0

    try:

        username=HostInfo.split(':')[1][2:]
        password=HostInfo.split(':')[2].split('@')[0]

        Domoticz.Debug('Add Item To Room')

        url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?activeidx='+str(ItemIDX)+'&activetype=0&idx='+str(RoomIDX)+'&param=addplanactivedevice&type=command'
#        Domoticz.Log(url)
        response=requests.get(url, auth=(username, password), timeout=5)
        data = json.loads(response.text)
#        Domoticz.Log(str(data))

    except:
        idx=-1

 #   Domoticz.Log(str(idx))

    return idx
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Update Device Routines  --------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def StartSpeedTest():

    import subprocess
    import shlex
    import time

    command = HomeFolder + 'spawn_bash.sh speedtest.sh'
    command = command + ' '  + str(Devices[speed_ping_id].ID)
    command = command + ' '  + str(Devices[speed_upload_id].ID)
    command = command + ' '  + str(Devices[speed_download_id].ID)
    command = command + ' '  + str(Devices[speed_single_upload_id].ID)
    command = command + ' '  + str(Devices[speed_single_download_id].ID)

#    Domoticz.Log(command)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    timeouts=0

    result = ''
    while timeouts < 10:
        p_status = process.wait()
#            Domoticz.Log('Command: '+command)
        output = process.stdout.readline()
#            Domoticz.Log('Output: '+str(output))
        if output == '' and process.poll() is not None:
            break
        if output:
            result=str(output.strip())
            timeouts=10
        else:
            time.sleep(0.2)
            timeouts=timeouts+1

    return

# --------------------------------------------------------------------------------------------------------------------------------------------------------
