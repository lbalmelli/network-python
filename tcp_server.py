import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((bind_ip,bind_port))
    server.listen(5)

    print("[*] listening on {}, port:{}".format(bind_ip,bind_port))

except socket.gaierror as err:
    print("address-related error: {}".format(err))

# Client-handling thread

def handling_client(client_socket):
    # receive from client and print

    try:
        request = client_socket.recv(1024)
        print("[*] Received: {}".format(request))

        # send a packet
        client_socket.send("ACK!".encode('utf-8'))

    except:
        print("Some error occurred!")
    finally:
        client_socket.close()

# This is the main loop

while True:

    # The socket must be bound to an address and listening for connections. 
    # The return value is a pair (conn, address) where conn is a new socket 
    # object usable to send and receive data on the connection, and address 
    # is the address bound to the socket on the other end of the connection.

    client, addr = server.accept()

    print(addr)
    print("[*] Accepted connection from: {}, {}".format(addr[0], addr[1]))

    # spin up client thread
    client_handler = threading.Thread(target=handling_client,args=(client,))
    client_handler.start()

