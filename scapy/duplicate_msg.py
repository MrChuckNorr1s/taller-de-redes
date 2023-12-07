from scapy.all import *

def duplicate_private_message(packet):
    if IP in packet and TCP in packet and Raw in packet and b"PRIVMSG" in packet[Raw].load:
        # Check if the Raw layer and payload are present
        if packet[Raw].load:
            # Decode the payload to a string
            original_payload = packet[Raw].load.decode('utf-8')

            # Extract the PRIVMSG content
            privmsg_start = original_payload.find("PRIVMSG")
            privmsg_end = original_payload.find("\r\n", privmsg_start)
            privmsg_content = original_payload[privmsg_start:privmsg_end]

            # Create a duplicated packet with the modified PRIVMSG content
            duplicated_payload = original_payload.replace(privmsg_content, f"{privmsg_content} (Duplicated)")
            duplicated_packet = packet.copy()
            duplicated_packet[Raw].load = bytes(duplicated_payload, 'utf-8')

            # Print details of the original and duplicated packets
            print("Original Packet:")
            print(packet.show())
            print("\nDuplicated Packet:")
            print(duplicated_packet.show())

            return duplicated_packet
    
    return None

# Callback function for intercepted packets
def packet_callback(packet):
    duplicated_packet = duplicate_private_message(packet)
    
    if duplicated_packet:
        print("\nPrivate Message Duplicated!")
        print(" ^`^t" * 50)
        sendp(duplicated_packet,verbose=False)
# Start sniffing on the specified interface and call packet_callback for each packet
sniff(iface="eth0", prn=packet_callback, filter="tcp port 6667")
