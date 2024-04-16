from Crypto.Cipher import AES
import sys

key = sys.argv[1].encode('utf-8')

def encrypt(msg):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('utf-8'))
    return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.decode('utf-8')
    except:
        return False

while True:
    line = sys.stdin.readline().strip()
    if line == "":
        break
    elif line == "exit":
        break

    command, *args = line.split()
    if command == "encrypt":
        msg = " ".join(args)
        nonce, ciphertext, tag = encrypt(msg)
        print(f"{nonce.hex()} {ciphertext.hex()} {tag.hex()}")
    elif command == "decrypt":
        nonce_hex, ciphertext_hex, tag_hex = args
        nonce = bytes.fromhex(nonce_hex)
        ciphertext = bytes.fromhex(ciphertext_hex)
        tag = bytes.fromhex(tag_hex)
        plaintext = decrypt(nonce, ciphertext, tag)
        print(plaintext)
