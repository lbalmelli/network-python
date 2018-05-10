import sys
import socket
import getopt
import threading
import subprocess

class NetCat:

    #define some global variables
    listen 		= False
    command		= False
    upload		= False
    execute		= ""
    target		= ""
    upload_dest	= ""
    port		= 0

    def usage(self):

        print("\nNetCat class (1-21-2018) - Laurent Balmelli (python3 version) - Original Code from Black Hat Pyhton")
        print("\tUsage: python3 netcat.py -t target_host -p port")
        print("\t-l --listen - listen on [host]:[port] for incoming connections.")
        print("\t-e --execute=file_to_run - execute file on the server upon receiving a connection.")
        print("\t-c --command - initialize a command shell.")
        print("\t-u --upload=destination - upon connection upload file to server and write to desination.")
        print("\n")

    def start(self, argv):	

        if not len(argv[1:]):	
            self.usage()

        # read command line options

        try:
            opts,args = getopt.getopt(argv[1:],"hle:t:p:cu",
                                                  ["help","listen","execute","target","port","command","upload"])

            #print(opts)
            #print(args)

        except getopt.GetoptError as err:
            print("error: {}.".format(err))
            self.usage()


        for o,a in opts:

            if o in ("-h", "--help"):
                self.usage()
            elif o in ("-l", "--listen"):
                self.listen = True
            elif o in ("-e", "--execute"):
            	self.execute = a
            elif o in ("-c", "--commandshell"):
                self.command = True
            elif o in ("-u", "--upload"):
                self.upload_dest = a
                print("file ",a)
            elif o in ("-t", "--target"):
                self.target = a
            elif o in ("-p", "--port"):
                try:
                    self.port = int(a)
                except ValueError:
                    print("Value {} for [port] is not valid. Exiting.".format(a))
                    sys.exit()
            else:
                # The simple form, assert expression, is equivalent to
                # if __debug__:
            # if not expression: raise AssertionError
                assert False, "Unhandled option."

        # listen or send data from stdin?

        if not self.listen and len(self.target) and self.port > 0:
            print("read in the buffer from the commandline")
            print("this will block, so send CRTL-D if not sending input to stdin")
            print("")
            buffer = sys.stdin.read()
            # send data off
            self.client_sender(buffer)

        # listen and upload, exec commands, drop shell

        if self.listen:
            print("starting server loop")
            self.server_loop()

    def client_sender(self,buffer):
        #
        # Client function that create a socket and sends the bufgfer to target and port that were passed
        # by argument to the netcat comment. Then, the function waits for data, prints the response and
        # get input from the user to send it again.

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # connect to target host and send the buffer
            client.connect((self.target,self.port))

            #print(buffer)

            if len(buffer):
                client.send(buffer)

            # wait for data back

            while True:

                recv_len = 1
                response = ""

                while recv_len:

                    data = client.recv(4096)
                    data_str = data.decode('ascii')
                    #print("data received:", data_str)

                    recv_len = len(data_str)
                    response += data_str	# concat the response by blocks of 4096 bytes

                    if recv_len < 4096:	# we have all the data
                        break

                print(response, end='')

                # wait for more input from the user

                buffer = input("")
                #buffer = "ls"
                buffer += "\n"

                #print("raw_input:",buffer)
                # send it off
                client.send(buffer.encode('utf-8'))

        except:
            print("[*] Exception raised! Exiting.")
            client.close()

    def server_loop(self):

        # if not target is defined, listen to all interfaces
        # https://stackoverflow.com/questions/39314086/what-does-it-mean-to-bind-a-socket-to-any-address-other-than-localhost

        if not len(self.target):
            self.target = "0.0.0.0"

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.target,self.port))
        server.listen(5)
        
        while True:
            client_socket, addr = server.accept()
            print("[*] Accepted connection from: {}, {}".format(addr[0], addr[1]))
            
            # create thread
            # spin up client thread
            client_thread = threading.Thread(target=self.client_handler,args=(client_socket,))
            client_thread.start()            
            
    def run_command(self, command):
      	
      	command = command.rstrip()

      	try:
      		output	= subprocess.check_output(command, stderr = subprocess.STDOUT, shell=True)

      	except:
      		output = "Failed to execute command.\r\n"

      	return output

    def client_handler(self, client_socket):

    	#client for upload

    	if len(self.upload_dest):

    		file_buffer = ""

    		# read data 
    		while True:
    			data = client_socket.recv(1024)

    			if not data:
    				break
    			else:
    				file_buffer += data

			# now we take these bytes and write them out
    		try:
    			print("writing file %s", self.upload_dest)
    			file_desc = open(self.upload_dest, "wb")
    			file_desc.write(file_buffer)
    			file_desc.close()

    			# acknowledge that we write the file out
    			str_answer = "saved to file: #s\r\n" % self.upload_dest
    			str_answer = str_answer.encode('utf-8')
    			client_socket.send(str_answer)

    		except:
    			str_answer = "Failed to save file to %s\r\n" %self.upload_dest 
    			str_answer = str_answer.encode('utf-8')
    			client_socket.send()

    	# if a command shell was requested

    	if len(self.execute):
    		print("command: %s"%self.execute)
    		output = self.run_command(self.execute)
    		client_socket.send(output)

    	if self.command:
    		while True:

    			# show prompt;
    			client_socket.send("<type command> ".encode('utf-8'))

    			# receive until you get line feed
    			cmd_buffer = ""
    			while "\n" not in cmd_buffer:
    				cmd_buffer += client_socket.recv(1024).decode('ascii')
    				#print("cmd buffer:",cmd_buffer)	
    			# send back command buffer
    			response = self.run_command(cmd_buffer)

    			# send back response
    			client_socket.send(response)


#
#	
#

c = NetCat()
c.start(sys.argv)