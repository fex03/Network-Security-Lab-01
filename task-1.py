import socket 
import threading 

HOST = "0.0.0.0"
PORT = 9001

def main():
    # Create the socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind to host and port
    server.bind((HOST, PORT))
    
    # Start listening
    server.listen(5)
    print("Server is listening on port 9001...")
    
    #Accept connections in a loop
    while(True):
        # The code will pause on the next line until a client connects
        client_socket, client_address = server.accept()
        
        # Print the address to verify the connection works
        print(f"Success! New connection from: {client_address}")
        

    
main()