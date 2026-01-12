import os
import getpass
try:
    from scapy.all import IP, TCP, send
except Exception:
    # scapy not available; provide harmless stubs so the script can run
    IP = None
    TCP = None
    def send(*args, **kwargs):
        print("Warning: scapy not installed; network send() disabled")
        return None

from random import randint

pas = getpass.getpass("send password: ")


keys = ["1","2","3","4","5","6","7","8","9","0",
        "a","b","c","d","e","f","g","h","i","j",
        "k","l","m","n","o","p","q","r","s","t",
        "u","v","w","x","y","z",]

pwg = ""

while pas != pwg:
    pwg = ""
    for i in range(len(pas)):
        guess_pass = keys[randint(0, 4)]
        pwg  = str(guess_pass) + str(pwg)
        print(pwg)
        print("Attack... please wait!")
        os.system("cls")
        
print(f"This password is cracked:{pwg}")

