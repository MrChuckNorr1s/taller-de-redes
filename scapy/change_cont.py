from scapy.all import *

def modify_privmsg(packet):
    modified = False  # Flag to track if the packet has been modified
    if IP in packet and TCP in packet and Raw in packet:
        # Check if it's a PRIVMSG request
        if b"PRIVMSG" in packet[Raw].load and b":hola" in packet[Raw].load:
            modified_payload = packet[Raw].load.replace(b":hola", b":chao")
            packet[Raw].load = modified_payload
            print("Modified PRIVMSG Request:")
            print(modified_payload.decode('utf-8'))
            modified = True
            sendp(packet, verbose=False) 
        # Check if it's a PRIVMSG response
        elif b"PRIVMSG" in packet[Raw].load and b":hola" in packet[Raw].load:
            modified_payload = packet[Raw].load.replace(b":hola", b":chao")
            packet[Raw].load = modified_payload
            print("Modified PRIVMSG Response:")
            print(modified_payload.decode('utf-8'))
            modified = True
            sendp(packet, verbose=False) 
    return packet, modified  # Return the modified packet and flag

# Function to sniff packets
def sniff_packets():
    # Callback function for intercepted packets
    def packet_callback(packet):
        print("Received Packet:")
        print(packet.show())

        # Use the modify_privmsg function to modify the payload
        modified_packet, is_modified = modify_privmsg(packet)

        if is_modified:
            print("\n  Packet Modified!")
            print(" ^`^t" * 50)

    # Start sniffing on the specified interface and call packet_callback for each packet
    sniff(iface="eth0", prn=packet_callback, store=0, filter="tcp port 6667")
 
# Call the function to start sniffing and modifying packets
sniff_packets()
