from scapy.all import sniff, IP, TCP, Raw

def modificar3(packet):
    if IP in packet and TCP in packet and packet[IP].src == "172.17.0.3" and packet[IP].dst == "172.17.0.2" and packet[TCP].dport == 58382:
        # Check if the Raw layer and payload are present
        if Raw in packet and packet[Raw].load:
            # Get the original payload as bytes
            original_payload = packet[Raw].load

            # Find the index of "PONG" in the payload
            pong_index = original_payload.find(b"PONG")

            if pong_index != -1:
                # Replace "PONG" with "PING"
                modified_payload = original_payload[:pong_index] + b'PING' + original_payload[pong_index + 4:]

                # Update the Raw layer with the modified payload
                packet[Raw].load = modified_payload

                return packet

    return None

# Callback function for intercepted packets
def packet_callback(packet):
    print("Received Packet:")
    print(packet.show())

    if 'TCP' in packet and Raw in packet:
        # Check if the Raw layer and payload are present
        if packet[Raw].load:
            # Convert the payload to a string before printing
            original_payload_str = packet[Raw].load.decode('utf-8')
            print("Original Payload:")
            print(original_payload_str)

            # Use the modificar3 function to modify the payload
            modified_packet = modificar3(packet)

            if modified_packet:
                # Convert the modified payload to a string before printing
                modified_payload_str = modified_packet[Raw].load.decode('utf-8')

                # Print the modified payload
                print("Modified Payload:")
                print(modified_payload_str)
                print("\n  Paquete Modificado!")
                print(" ^`^t" * 50)

# Start sniffing on the specified interface and call packet_callback for each packet
sniff(iface="eth0", prn=packet_callback, filter="tcp port 6667")
