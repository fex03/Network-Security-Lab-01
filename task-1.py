#TCP: Line based server
import socket 
import threading 
import time

HOST = "0.0.0.0"
PORT = 9001

# Dictionary to store key-value, preventing race conditions issu
kv_store = {}
store_lock = threading.Lock()

# Function to handle each client communication
def handle_client(client_socket, client_address):
    print(f"Sto gestendo il client: {client_address} in un thread separato")
    
    # Create buffer to receive multiple commands in the same connection
    buffer=""
    
    # Continous loop to keep receiving data
    while(True):
        data = client_socket.recv(4096)
        if not data:
            break
        
        # Convert to ascii and append new data to buffer
        buffer += data.decode('ascii')
        
        # 2. Process ALL complete commands currently stored in the buffer
        while '\n' in buffer:
            # Extract one line, and keep the remainder in buffer
            line, buffer = buffer.split('\n', 1)
            
            # Skip empty lines (e.g., if the user just pressed Enter)
            if not line:
                continue
            
            # 'line' is your actual command string (e.g., "PING" or "ECHO hello")
            print(f"Received command: {line}")
            
            # Dividing the row in max 3 parts
            tokens = line.split(' ', 2)
            command = tokens[0] # This is the principal commmand
            
            response = ""
            
            if command == "PING":
                response = "PONG"
            elif command == "ECHO":
                
                # Verifing if some txt is entered after the ECHO command
                if len(tokens) > 1:
                    
                    # We take everything after first space
                    txt = line.split(' ',1)[1]
                    response = txt
                 
            elif command == "SET":
                if len(tokens) == 3: # With a correct input this command has exactly 3 parts: SET <key> <value>
                    with store_lock:
                        kv_store[tokens[1]] = tokens[2]
                        response = "OK"
                else:
                    response = "ERR"  
            
            elif command == "GET":
                if len(tokens) >= 2: # Error handling on lacking parts input
                      with store_lock:
                          response = kv_store.get(tokens[1], "NOT_FOUND")
                else:
                    response = "ERR"
                    
                       
            # Wrong command
            else:
                response = "ERR"        
                
            
            # Temporary test response:
            client_socket.sendall(f"{response}\n".encode('ascii'))

    
    # Close connection when communication is finished
    client_socket.close()
    print(f"Connection closed for client: {client_address}.")
    
    
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