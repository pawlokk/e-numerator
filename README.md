# e-numerator
basic python script that simplifies solving of capture the flag challenges

usage: solver.py [-h] -ip IP -n HOSTNAME [-s SUBDOMAIN] [-u USERNAME] [-d DIRECTORY] [-r ROCKYOU]

options:
  -h, --help            show this help message and exit
  -ip IP, --ip IP       box IP address
  -n HOSTNAME, --hostname HOSTNAME
                        box hostname
  -s SUBDOMAIN, --subdomain SUBDOMAIN
                        path to subdomain bruteforce wordlist
  -u USERNAME, --username USERNAME
                        path to ssh bruteforce login wordlist
  -d DIRECTORY, --directory DIRECTORY
                        path to directory bruteforce wordlist
  -r ROCKYOU, --rockyou ROCKYOU
                        path to rockyou file (or any other used for password bruteforcing)
