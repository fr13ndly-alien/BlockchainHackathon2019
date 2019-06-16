from Crypto.Cipher import AES
import random
import hashlib
from Crypto.Hash import SHAKE128

"""
Create symmetric key AES 256 based on public address and private key
Should not involve private key
"""


def create_symmetric_key():
    '''
    Shuffle byte of 2 keys for random
    '''
    public_content = open("publickey", "rb").read()
    private_content = open("privatekey", "rb").read()
    byte_generate_new_key = public_content + private_content
    byte_to_list = byte_generate_new_key = list(byte_generate_new_key.decode('utf8'))
    random.shuffle(byte_to_list)
    result = ''.join(byte_to_list)
    '''
    Using Shake algorithm to customize output bytes length, can change to SHA256
    '''
    shake = SHAKE128.new()
    shake.update(result.encode('utf8'))
    byte_actual_use = shake.read(32) # get 32 bytes for key
    cipher = AES.new(byte_actual_use, AES.MODE_EAX)
    nonce = cipher.nonce
    tag = cipher.digest() # tag for verification, have error in using this value, will use new_tag when encrypt
    with open("key.bin", "wb") as f_out:
        [f_out.write(x) for x in (nonce, tag, byte_actual_use)] # make the file more information than needed for customer to not meddle with file


def load_key():
    with open("key.bin", "rb") as f_in:
        nonce, tag, key = [f_in.read(x) for x in (16, 16, 32)] # need to hide these information somewhere else
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher


def encrypt_data_hash():
    data = 'Hello World!' # modify later to load from file
    cipher = load_key()
    cipher_text, new_tag = cipher.encrypt_and_digest(data.encode('utf8'))
    sha_256 = hashlib.sha256()
    sha_256.update(cipher_text)
    hash_value = sha_256.hexdigest()
    return cipher_text, hash_value, new_tag # modify later to write into new file


def decrypt_data(cipher_text, new_tag):
    cipher = load_key() # the library require must first initialized or update to use decrypt
    result = cipher.decrypt_and_verify(cipher_text, new_tag)
    return result.decode('utf8')


if __name__ == '__main__':
    create_symmetric_key()
    cipher_text, hash_value, new_tag = encrypt_data_hash()
    data = decrypt_data(cipher_text, new_tag)
    print(data)
