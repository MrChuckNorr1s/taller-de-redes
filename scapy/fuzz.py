from scapy.all import *

def fuzzing(packet):
    modified_packet=Ether(packet[Ether]) / IP(dst=packet[IP].dst,src=packet[IP].src)
    print("Modificando paquete")
    # PAQUETE MODIFICAD
    modified_packet=fuzz(modified_packet)
    print("Paquete modificado") 
    ls(modified_packet)
    # ENVIAMOS EL PAQUETE
    send(modified_packet, verbose=False)

def packet_callback(packet):
    print("Paquete Capturado")
    print(packet.summary())

    fuzzing(packet)

sniff(iface='eth0',filter="tcp and host {} and port {}".format('172.17.0.2', 6667),prn=packet_callback)
