import socket 
import threading 
import time

HOST = "0.0.0.0"
PORT = 9001


# Function to handle each client communication
def handle_client(client_socket, client_address):
    print(f"Sto gestendo il client: {client_address} in un thread separato")
    
    time.sleep(10)
    
    # Close connection when communication is finished
    client_socket.close()
    
    
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
        
        # Handle client and then come back to accepting new clients
        t = threading.Thread(target=handle_client, args=(client_socket, client_address))
        t.start()
        
        # Print the address to verify the connection works
        print(f"Success! New connection from: {client_address}")
        

    
    
main()