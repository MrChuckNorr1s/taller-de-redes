#Codigo con librerías de Scapy para capturar tráfico entre el servidor y cliente
from scapy.all import sniff

# Define a callback function to process intercepted packets
def packet_callback(packet):
    # Print detailed information about each packet
    print("Packet details:")
    print(packet.show())

# Start sniffing on the specified interface and call the callback for each pack>
sniff(iface="eth0", prn=packet_callback)
