import socket 
import random

from common_code import *

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = ("172.16.80.252", PORT)
FORMAT = 'utf-8'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

filters = ["R" , "D"]

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    key = []
    filters_used = []
    for i in range(FIRST_KEY_LENGTH):
        msg = conn.recv(1).decode(FORMAT)
        choice = random.choice(filters)
        filters_used.append(choice)
        if choice.lower() == msg.lower():
            if msg.islower():
                key.append(0)
            else:
                key.append(1)
        else:
            key.append(random.choice([0,1]))

    #getting list of filters used
    accepted_filters = []
    final_key = []
    for i in range(FIRST_KEY_LENGTH):
        msg = conn.recv(1).decode(FORMAT)
        if msg == filters_used[i]:
            accepted_filters.append("1")
            final_key.append(key[i])
        else:
            accepted_filters.append("0")
    
    #returning the accepted filters
    conn.send("".join(accepted_filters).encode(FORMAT))
    print("".join(map(str,final_key)))

    batch_size = int(conn.recv(2).decode(FORMAT))

    final_key = "".join(map(str,final_key))
    final_key = generate_key(final_key)    
    print(f"Final key created using the binary key with key batch : {KEY_BATCH} is : {final_key}")


    final_message = conn.recv(batch_size * len(final_key)).decode(FORMAT)
    print(f"Batch Size of the message received: {batch_size}")
    print(f"Message received: {final_message}")
    print(f"Message decrypted using the key {final_key} is: {xor_encrypt(final_message, final_key)}")

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)



print("[STARTING] server is starting...")
start()