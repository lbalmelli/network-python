import socket

target_host = "0.0.0.0"
target_port = 9999

try:
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((target_host,target_port))

    input_str = input("enter message:")
    
    if input_str == '':
        client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n".encode('utf-8'))
    else:
        client.send(input_str.encode('utf-8'))

    response = client.recv(4096)
    print(response.decode('utf-8'))

except socket.timeout:
    print("Connection timeout. Exiting.")
    exit(0)

except socket.error as msg:
    print("Exception error: %s" % msg)

except socket.gaierror:
    print("Address-related error.")
