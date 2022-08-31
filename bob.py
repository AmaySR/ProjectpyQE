import socket
import random
import math

from common_code import *

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'

SERVER = "172.16.80.252"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
filters = ["R" ,"D"]

def send(unencrypted_msg):
    #generate random key and send
    message = ""
    key = []
    filters_used = []
    for _ in range(FIRST_KEY_LENGTH):
        ch = random.choice([0,1])
        key.append(ch)
        fil = random.choice(filters)
        filters_used.append(fil)
        if ch == 0:
            message+=fil.lower()
        else:
            message +=fil
        
    message = message.encode(FORMAT)
    client.send(message)

    #send list of filters
    client.send("".join(filters_used).encode(FORMAT))

    #receiving accepted filters
    final_key = []
    for i in range(FIRST_KEY_LENGTH):
        msg = client.recv(1).decode(FORMAT)
        if msg == "1":
            final_key.append(key[i])

    print("".join(map(str,final_key)))


    size = len(unencrypted_msg)

    final_key = "".join(map(str,final_key))
    final_key = generate_key(final_key)    
    print(f"Final key created using the binary key with key batch : {KEY_BATCH} is : {final_key}")


    key_len = len(final_key)
    print(f"Length of final key: {key_len}")

    batch_size = math.ceil(size/key_len)
    client.send(str(batch_size).encode(FORMAT))

    print(f"Size of the message: {size}")

    unencrypted_msg = unencrypted_msg + "*"*(batch_size*500 - size)

    print(f"Size of the message after padding: {len(unencrypted_msg)}")

    print(f"Batch size: {batch_size}")

    print(f"Padding Litral: {PADDING_LITRAL}")

    encrypted_msg = xor_encrypt(unencrypted_msg,final_key)
    print(f"Encrypted message: {encrypted_msg}")
    client.send(encrypted_msg.encode(FORMAT))

if __name__ == "__main__":
    unencrypted_msg = str(input("Enter message: "))
    send(unencrypted_msg)