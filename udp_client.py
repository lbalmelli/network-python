import socket

target_host = "0.0.0.0"
target_port = 9999

try:
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    client.sendto("AAABBBCCC".encode('utf-8'),(target_host,target_port))
    data, addr = client.recvfrom(4096)

    print(data)
    #print(response.decode('utf-8'))

except socket.timeout:
    print("Connection timeout. Exiting.")
    exit(0)

except socket.error as msg:
    print("Exception error: %s" % msg)

except socket.gaierror:
    print("Address-related error.")