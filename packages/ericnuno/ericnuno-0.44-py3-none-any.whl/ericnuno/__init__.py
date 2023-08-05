import paramiko
import time
import os
import subprocess
import telnetlib
import smtplib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver

def email(IP, to, from_field, subject, message):

    subject = subject + "\r\n"
    message = 'Subject: {}\n\n{}'.format(subject, message)
    msg = ("From: " + from_field + "\r\nTo: " + ", ".join(to) + "\r\n" )
    msg = msg + message

    server = smtplib.SMTP(IP, "25")
    server.sendmail(from_field, to, msg)
    server.quit()

def ping(hostname, n=3):
    output = subprocess.run(["ping", hostname, "-n", str(n)], stdout=subprocess.PIPE)
    result = output.stdout.decode()

    #and then check the response...
    if 'Reply from ' + hostname + ': bytes=' in result:
        return True
    elif hostname.count('.') != 3:
        if ': bytes=' in result and 'Reply from ' in result:
            return True
    else:
        return False

def ZipToZone(zip):

    zip = str(zip)
    try:
        req = requests.get('http://www.zip-info.com/cgi-local/zipsrch.exe?tz=tz&zip=' + zip +'&Go=Go')
        req.raise_for_status()
        ZipObj = bs4.BeautifulSoup(req.text, "lxml")

        if "PST" in ZipObj.encode('ascii').decode():
            return("Pacific")
        elif "MST" in ZipObj.encode('ascii').decode():
            return("Mountain")
        elif "CST" in ZipObj.encode('ascii').decode():
            return("Central")
        elif "EST" in ZipObj.encode('ascii').decode():
            return("Eastern")

    except:
        try:
            messagebox.showerror("Error", "Couldn't pull the time zone, please make sure you're connected to the internet and try again.")
        except:
            print("Couldn't pull the time zone, please make sure you're connected to the internet and try again.")
        return

    return

def eprint(Sentence):

    SentLeng = len(Sentence)
    print("="* SentLeng *3)
    print(("=" * SentLeng) + Sentence + ("=" * SentLeng))
    print("="* SentLeng *3)

    return

def ssh_connect(device_ip, username, password):
    print("Connecting to: " + device_ip)
    hostname = device_ip
    port = 22

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)
    channel = client.invoke_shell()

    print("Successfully connected to: " + device_ip)
    return client, channel

def psend(command, channel):

    channel.send(command)

def pwait(waitstr, channel, tout=0, screenprint=False):
    startTime = int(time.time())
    stroutput = ''
    while waitstr not in stroutput:
        currentTime = int(time.time())
        if channel.recv_ready():
            try:
                current = channel.recv(9999).decode()
                stroutput += current
                if current.strip() != '':
                    if screenprint:
                        print(current, end='')
            except:
                continue

        if tout != 0:
            if (currentTime - startTime) > tout:
                try:
                    if current.strip() != '':
                        if screenprint:
                            print(current, end='')
                except:
                    pass
                return stroutput

    return stroutput

def twait(phrase, tn, tout = -1, logging = 'off', rcontent = False, screenprint = False):

    # Adding code to allow lists for phrase
    finalcontent = ' '

    #This is the time of the epoch
    startTime = int(time.time())
    while True:
        # This is the current time
        currentTime = int(time.time())
        if tout != -1:

            # This is the time since the start of this loop
            # if it exceeds the timeout value passed to it
            # then exit with a return of 0
            if (currentTime - startTime) > tout:
                if logging == 'on':
                    #Adding the -e-e-> to differentiate from device output
                    if screenprint:
                        print('-e-e->It has been ' + str(tout) +  ' seconds. Timeout!')
                if rcontent == False:
                    return 0
                else:
                    return 0, finalcontent
        # Eager reading back from the device
        content = (tn.read_very_eager().decode().strip())

        if content.strip() != '':
            finalcontent += content
        # if the returned content isn't blank. This stops
        # it from spamming new line characters
        if content.strip() != '':
            if screenprint:
                print (content, end='')
        # content was found! Return a 1 for success
        if type(phrase) is str:
            if phrase in content:
                if rcontent == False:
                    return 1
                else:
                    return 1, finalcontent

        if type(phrase) is list:

            count = 1
            for p in phrase:
                if p in content:
                    if rcontent == False:
                        return count
                    else:
                        return count, finalcontent
                count+=1

def tsend(phrase, tn):

    #Sends the phrase that was passed to it as bytes
    tn.write(phrase.encode())

    return

def shortfiles(parentdir, extensions=[]):
    TotalFiles = []
    if extensions == []:
        for root, directories, filenames in os.walk(parentdir):
            for filename in filenames:
                TotalFiles.append(filename)

    elif extensions != []:
        for root, directories, filenames in os.walk(parentdir):
            for filename in filenames:
                for ext in extensions:
                    if ext in filename:
                        TotalFiles.append(filename)

    return TotalFiles

def longfiles(parentdir, extensions=[]):
    TotalFiles = []
    if extensions == []:
        for root, directories, filenames in os.walk(parentdir):
            for filename in filenames:
                TotalFiles.append(os.path.join(root, filename))

    elif extensions != []:
        for root, directories, filenames in os.walk(parentdir):
            for filename in filenames:
                for ext in extensions:
                    if ext in os.path.join(root, filename):
                        TotalFiles.append(os.path.join(root, filename))

    return TotalFiles