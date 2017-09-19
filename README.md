# WifiHack
Use Python to get Wifi Handshakes using the Deauthentification Method. WifiHack is a python program designed in Linux, for Linux, that uses the Aircrack-ng package and all it's tools. If you start it up, it will start sending deauthentification packets to every wifi access point that it can identify. During that time, it will attempt to get a handshake and save that handshake to a file so that you can crack later. This is a HIGHLY customizable python program. Written in Python3.

# Dependencies
Paramiko

Netifaces

# Functions(Predefined)
### startup()
Sets up everything you need to capture handshakes. Creates a folder called "Handshakes", then It will start up your wireless interface, putting it in monitor mode. Then it starts airodump-ng and saves all the information regarding the SSIDS in the vicinity in a file called Everything-01.csv.
### pidof()
Effective process killer. Usually called when airodump-ng needs to be killed because it cannot close on it's own. sleeptime is the argument, telling it how long it should lay dormant.
### crackinfo()
Checks The Everything.csv file and pulls BSSID, SSID, and CHANNEL captured within. This allows for you to take that information and start cracking each Access Point systematically.
### cracking() and deauth()
Individiually monitors an Access Point while simultaneously running a deauth attack of 100 packets against that Access Point. Moves on to the next Access Point in the list. Saves that information in a file.
### handcheck()
Systematically looks at each file and checks to see if that file contains the handshake. If it does, it moves that file to the shakes folder. VERY IMPORTANT: This holds the files that have the actual Handshake, which you will need for cracking that Access Point's password.
### sendoff()
Completely optional. Sends all of the files in the "Handshakes/shakes" folder to a remote destination of your choosing, using the Paramiko module.

# Future Notes
This program is still very much in development, future changes will include, bug fixes, email support, accessibility improvements, etc. Feedback for future releases is appreciated.
