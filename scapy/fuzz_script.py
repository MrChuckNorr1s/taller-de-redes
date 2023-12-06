#codigo para ambas inyecciones con Fuzzing

from scapy.all import *
from scapy.utils import hexdump
import random
import string

def fuzz_tcp_raw_fuzzing(packet):
    if IP in packet and TCP in packet and Raw in packet:
        # Supongamos que el tr  fico IRC est   codificado en UTF-8
        irc_message = packet[Raw].load.decode('utf-8')

        # Crear un paquete Scapy a partir de la cadena IRC
        scapy_packet = IP(src=packet[IP].src, dst=packet[IP].dst) / TCP(sport=packet[TCP].sport, dport=packet[TCP].dport) / Raw(load=irc_message)

        # Impresi  n del paquete original
        print("\nOriginal Packet:")
        hexdump(packet)

        # Inyecci  n 1: Fuzzing en el mensaje IRC
        fuzzed_packet = fuzz(scapy_packet)
        send(fuzzed_packet)

        # Impresi  n del paquete despu  s de la inyecci  n 1
        print("\nFuzzed Packet(n°1):")
        hexdump(fuzzed_packet)

        # Inyecci  n 2: T  cnica de fuzzing tradicional en el campo Raw
        fuzzed_message = ''.join(random.choice(string.ascii_letters) for _ in range(len(irc_message)))
        fuzzed_packet = packet.copy()
        fuzzed_packet[Raw].load = fuzzed_message.encode('utf-8')
        send(fuzzed_packet)

        # Impresi  n del paquete despu  s de la inyecci  n 2
        print("\nFuzzed Packet (Traditional Fuzzing, n°2):")
        hexdump(fuzzed_packet)

# Filtra el tr  fico entre el servidor (172.17.0.2) y el cliente (172.17.0.3) IRC
filter_expression = "host 172.17.0.2 and host 172.17.0.3 and port 6667"
sniff(filter=filter_expression, prn=fuzz_tcp_raw_fuzzing, store=0)
