import socket

localIP = "0.0.0.0"

localPort = 65001

bufferSize = 1024


# msgFromServer = "Hello UDP Client"

# bytesToSend = str.encode(msgFromServer)


def create_server():
    # Create a datagram socket
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.settimeout(0)
    udp_server_socket.setblocking(False)

    # Bind to address and ip

    udp_server_socket.bind((localIP, localPort))

    print("UDP server up and listening")

    # Listen for incoming datagrams
    return udp_server_socket


def example_listen(UDPServerSocket):
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        data = message.decode("utf-8").split(";")
        [x, y, z] = [float(a) for a in data]

        # clientIP = "Client IP Address:{}".format(address)

        print("Got: {:.3f}, {:.3f}, {:.3f}".format(x, y, z))
        # print(clientMsg)
        # print(clientIP)

        # Sending a reply to client

        # UDPServerSocket.sendto(bytesToSend, address)
