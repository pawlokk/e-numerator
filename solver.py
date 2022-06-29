#!/usr/bin/python3
import os
import nmap3
from pythonping import ping
import subprocess
import re
import colorama
from colorama import Fore, Back, Style

colorama.init()
print(Fore.GREEN)
targetip = input("@@Provide target IP: ")
hostname = input("@@Provide hostname: ")
print(Style.RESET_ALL)
print('\n')

# print("Creating /etc/hosts entry for target...")
# hostscommand = 'echo %s %s >> /etc/hosts'%(targetip,hostname)
# os.system(hostscommand)
print(Fore.GREEN)
print("@@Checking host availability ...")
print(Style.RESET_ALL)
pingcommand = 'ping %s -c 1'%(targetip)
os.system(pingcommand)


print(Fore.GREEN)
print("@@Discovering open ports ...")
print(Style.RESET_ALL)
nmapinitial = """nmap -p- --open -v -n %s -oG %s.ini | grep open | awk '{print $1}' | grep [[:digit:]]""" %(targetip,hostname)
open_ports = os.popen(nmapinitial).read()
print(open_ports)

temp = re.findall(r'\d+', open_ports)
temp1 = list(map(int, temp))
ports = str(temp1).strip("[]").replace(" ","")


with open('nmap.comp', 'w') as f:
	print(Fore.GREEN)
	print("@@Initializing standard scan ...")
	print(Style.RESET_ALL)
	nmapcomp = """nmap -p%s -sC -sV -vv -oN nmap.std %s""" %(ports,targetip)
	# print(nmapcomp)
	output_nmapcomp = os.popen(nmapcomp).read()
	print(output_nmapcomp)
	f.write('{}\n'.format(output_nmapcomp))

with open('nmap.comp', 'r') as f:
	for line in f:
		if "ssh" in line and "open" in line:
			os.popen("""hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt -P ~/rockyou.txt ssh://%s -o hydra.log"""%(targetip))
		if "HTTP" in line and "open" in line:
			os.popen("""gobuster dir --wordlist=/usr/share/seclists/Discovery/Web-Content/directory-list-1.0.txt --url=http://%s -x txt,sh,py,jpg,png""" %(hostname))

