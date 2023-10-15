#
# Title : plugin.py for speedtest-cli
# Author: Jack Veraart
# Date  : 2021-05-07
#
# Changelog:
#
# version 2.0.0 : Changed for new Domoticz API
# version 1.0.0 : Initial version

"""
<plugin key="JacksSpeedtest" name="Jacks Speedtest" author="Jack Veraart" version="2.0.0">
    <description>
        <font size="4" color="white">Speedtest</font><font color="white">...Notes...</font>
        <ul style="list-style-type:square">
            <li><font color="yellow">This plugin uses speedtest.py which I downloaded from Matt Martz @ https://github.com/sivel.</font></li>
            <li><font color="yellow">Since speedtest.py takes some time to run I created spawn_bash.sh and speedtest.sh to run it as a detached process.</font></li>
            <li><font color="yellow">Add Admin account details below so I can import icons and create a room.</font></li>
            <li><font color="yellow">To develop your own plugin...check this web site... <a href="https://www.domoticz.com/wiki/Developing_a_Python_plugin" ><font color="cyan">Developing_a_Python_plugin</font></a></font></li>
        </ul>
    </description>
    <params>

        <param field="Username" label="Username." width="120px" default="admin"/>

        <param field="Password" label="Password." width="120px" default="domoticz" password="true"/>

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

StartupOK=0
HomeFolder=''
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

        global StartupOK
        global Debug

        global HomeFolder
        global LocalHostInfo

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
            RoomName        =str(Parameters['Name'])

            LocalHostInfo     = "https://"+Username+":"+Password+"@"+GetDomoticzIP()+":"+GetDomoticzHTTPSPort()
#
# Import all images and build ImageDictionary
#
            StartupOK = ImportImages()
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
            Recreate = False

            RoomIdx=CreateRoom( RoomName, Recreate)
            if (RoomIdx != 0):
                StartupOK = 1
#
# Add all items to Room
#
            if (StartupOK == 1):
                AddToRoom(RoomIdx,Devices[speed_upload_id].ID)
                AddToRoom(RoomIdx,Devices[speed_download_id].ID)
                AddToRoom(RoomIdx,Devices[speed_single_upload_id].ID)
                AddToRoom(RoomIdx,Devices[speed_single_download_id].ID)
                AddToRoom(RoomIdx,Devices[speed_ping_id].ID)
#
# And start the action
#
            Domoticz.Heartbeat(PollInterval)

            if (StartupOK == 1):

                Domoticz.Log('onStart oke !!')
            else:
                Domoticz.Log('ERROR starting up')
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

        if StartupOK == 1: # Startup was fine

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
# ----------------------------------------------------  Basic Management Routines  -----------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetDomoticzHTTPSPort():

    try:
        import subprocess
    except:
        Domoticz.Log("python3 is missing module subprocess")

    try:
        import time
    except:
        Domoticz.Log("python3 is missing module time")

    try:
        Domoticz.Debug('GetDomoticzHTTPSPort check startup file')
        pathpart=Parameters['HomeFolder'].split('/')[3]
        searchfile = open("/etc/init.d/"+pathpart+".sh", "r")
        for line in searchfile:
            if ("-sslwww" in line) and (line[0:11]=='DAEMON_ARGS'):
                HTTPSPort=str(line.split(' ')[2].split('"')[0])
                HTTPSPort = HTTPSPort.replace('\\n','') # remove EOL
        searchfile.close()
        Domoticz.Debug('GetDomoticzHTTPSPort looked in: '+"/etc/init.d/"+pathpart+".sh"+' and found port: '+HTTPSPort)
    except:
        Domoticz.Debug('GetDomoticzHTTPSPort check running process')
        command='ps -ef | grep domoticz | grep sslwww | grep -v grep | tr -s " "'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        timeouts=0

        result = ''
        while timeouts < 10:
            p_status = process.wait()
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                HTTPSPort=str(output)
                HTTPSPort = HTTPSPort[HTTPSPort.find('-sslwww'):]
                HTTPSPort = HTTPSPort[HTTPSPort.find(' ')+1:]
                HTTPSPort = HTTPSPort[:HTTPSPort.find(' ')]
                HTTPSPort = HTTPSPort.replace('\\n','') # remove EOL
            else:
                time.sleep(0.2)
                timeouts=timeouts+1
        Domoticz.Log('GetDomoticzHTTPSPort looked at running process and found port: '+HTTPSPort)

    return HTTPSPort

# --------------------------------------------------------------------------------------------------------------------------------------------------------
def GetImageDictionary():

    import json
    import requests

    try:
        mydict={}

        url=LocalHostInfo+'/json.htm?type=command&param=custom_light_icons'

        response=requests.get(url, verify=False)
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
    try :
        import glob
    except:
        Domoticz.Log("python3 is missing module glob")

    global ImageDictionary
    
    MyStatus=1
    
    ImageDictionary=GetImageDictionary()
    
    if ImageDictionary == {}:
        Domoticz.Log("Please modify your setup to have Admin access. (See Hardware setup page of this plugin.)")      
        MyStatus = 0
    else:

        for zipfile in glob.glob(HomeFolder+"CustomIcons/*.zip"):
            importfile=zipfile.replace(HomeFolder,'')
            try:
                Domoticz.Image(importfile).Create()
                Domoticz.Debug("ImportImages Imported/Updated icons from "  + importfile)
            except:
                MyStatus = 0
                Domoticz.Log("ImportImages ERROR can not import icons from "  + importfile)

        if (MyStatus == 1) : 
            ImageDictionary=GetImageDictionary()
            Domoticz.Debug('ImportImages Oke')

    return MyStatus

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetDomoticzIP():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
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
def CreateRoom(RoomName, Recreate):

    try:
        import json
    except:
        Domoticz.Log("python3 is missing module json")
        
    try:
        import requests
    except:
        Domoticz.Log("python3 is missing module requests")
    
    idx=0

    try:

        Domoticz.Debug('Check if Room Exists')
        
        url=LocalHostInfo+'/json.htm?type=command&param=getplans&order=name&used=true'
        Domoticz.Debug('Check Room '+url)
        response=requests.get(url, verify=False)
        data = json.loads(response.text)

        if 'result' in data.keys():
            for Item in data['result']:
                if str(Item['Name']) == RoomName:
                    idx=int(Item['idx'])
                    Domoticz.Debug('Found Room '+RoomName+' with idx '+str(idx))

        if (idx != 0) and Recreate :
            url=LocalHostInfo+'/json.htm?idx='+str(idx)+'&param=deleteplan&type=command'
            Domoticz.Log('Delete Room '+url)
            response=requests.get(url, verify=False)
            idx = 0
        
        if idx == 0 :
            url=LocalHostInfo+'/json.htm?name='+RoomName+'&param=addplan&type=command'
            Domoticz.Log('Create Room '+url)
            response=requests.get(url, verify=False)
            data = json.loads(response.text)
            Domoticz.Log('CreateRoom Created Room'+str(data))
            idx=int(data['idx'])
    except:
        Domoticz.Log('ERROR CreateRoom Failed')
        idx=0

    Domoticz.Debug('CreateRoom status should not be 0 : '+str(idx))
    
    return idx
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def AddToRoom(RoomIDX,ItemIDX):

    try:
        import json
    except:
        Domoticz.Log("python3 is missing module json")
        
    try:
        import requests
    except:
        Domoticz.Log("python3 is missing module requests")
    
    status=1

    try:
        url=LocalHostInfo+'/json.htm?activeidx='+str(ItemIDX)+'&activetype=0&idx='+str(RoomIDX)+'&param=addplanactivedevice&type=command'
        response=requests.get(url, verify=False)
        data = json.loads(response.text)
    except:
        Domoticz.Log('ERROR AddRoom Failed')
        status=0

    Domoticz.Debug('AddToRoom status should not be 0 : '+str(status))
    
    return status

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
