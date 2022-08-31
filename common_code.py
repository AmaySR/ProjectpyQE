# common code for both

PADDING_LITRAL = "*"
KEY_BATCH = 7

FIRST_KEY_LENGTH = 500

def binaryToDecimal(binary): 
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal   


def generate_key(key):
    final_key = []
    for i in range(0,len(key),KEY_BATCH):
        final_key.append(binaryToDecimal(int(key[i : i+KEY_BATCH])))
    return final_key


def xor_encrypt(message,final_key):
    encrypted_msg = ""
    for i in range(len(message)):
        encrypted_msg += chr(ord(message[i])^final_key[i % len(final_key)])
    return encrypted_msg
