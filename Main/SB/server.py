import socket

localIP = "0.0.0.0"
localPort = 20001
bufferSize = 1024

msgFromServer = "(21, 13)"


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    address = bytesAddressPair[1]
    bytesToSend = str.encode(msgFromServer)
    # Broadcasting location
    UDPServerSocket.sendto(bytesToSend, address)
    print(f"Sent to {address} data {msgFromServer}.")