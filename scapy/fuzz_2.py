from scapy.all import *
from scapy.utils import hexdump
import random
import string

def fuzz_tcp_raw_fuzzing(packet):
    if IP in packet and TCP in packet and Raw in packet:
        
        irc_message = packet[Raw].load.decode('utf-8')
    
        scapy_packet = IP(src=packet[IP].src, dst=packet[IP].dst) / TCP(sport=packet[TCP].sport, dport=packet[TCP].dport) / Raw(load=irc_message)
      
        print("\nOriginal Packet:")
        hexdump(packet)
   
        fuzzed_packet = fuzz(scapy_packet)
        sendp(fuzzed_packet,verbose=False)
       
        print("\nFuzzed Packet(n  1):")
        hexdump(fuzzed_packet)


filter_expression = "host 172.17.0.2 and host 172.17.0.3 and port 6667"
sniff(filter=filter_expression, prn=fuzz_tcp_raw_fuzzing, store=0)
