from Crypto.PublicKey import RSA
from Crypto import Random
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS, pkcs1_15
from Crypto.Hash import SHA256

# Create pair key
def rsa_key_creation(i):
    length = 1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()
    with open('private'+str(i)+'.pem', 'wb') as prv_file:
        #print("{}".format(privatekey.exportKey()), file = prv_file)
        prv_file.write(privatekey.exportKey("PEM"))
    with open('public'+str(i)+'.pem', 'wb') as pub_file:
        #print("{}".format(publickey.exportKey()), file = pub_file)
        pub_file.write(publickey.exportKey("PEM"))

'''
Test function to make sure creation pair key is correct
'''


"""
def encrypt(rsa_publickey, plain_text):
    cipher_text = PKCS1_v1_5.new(rsa_publickey).encrypt(plain_text)
    b64cipher = base64.b64encode(cipher_text)
    return b64cipher


def decrypt(rsa_privatekey, b64cipher):
    decoded_cipher = base64.b64decode(b64cipher)
    plain_text = PKCS1_v1_5.new(rsa_privatekey).decrypt(decoded_cipher, Random.new().read(64))
    return plain_text
"""


def sign(rsa_privatekey, hash):
    #signer = DSS.new(rsa_privatekey, 'fips-186-3')
    signer = pkcs1_15.new(rsa_privatekey)
    signature = signer.sign(hash)
    return signature


def verify(rsa_publickey, signature, hash):
    #verifier = DSS.new(rsa_publickey, 'fips-186-3')
    verifier = pkcs1_15.new(rsa_publickey)
    try:
        verifier.verify(hash, signature)
        return True
    except (ValueError, TypeError):
        return False


'''
Notary system for digitally signed twice
Use dict to temporary store, should use central database
Have many problems with regards to digital signature
So this should be on testing only
'''
dict_digital_twice = dict()


def store_digital_twice(key, signature):
    if key not in dict_digital_twice.keys():
        dict_digital_twice.setdefault(key, [])
        dict_digital_twice[key].append(signature)
    else:
        if len(dict_digital_twice[key]) == 2:
            print("This document already signed twice")
        elif dict_digital_twice[key].count(signature) == 0:
            dict_digital_twice[key].append(signature)
        else:
            print("This signature already exist")


'''
Check valid function still missing alot, as file
can store both signature of same status: Lawyer or Docter
Which should be invalid, and thus promp to sign again
This is only for the current flow thinking only, do not use it
'''
def check_digital_valid(key, hash):
    status = []
    if len(dict_digital_twice[key]) < 2:
        print("Not signed by 2 parties. Please contact to sign")
    else:
        '''
        Since we should use central database to store
        We will create new pair key for sign document
        We can map which publickey belong to docter or lawyer
        '''
        for signature in dict_digital_twice[key]:
            for publickey in publickey_database:
                res = verify(publickey, signature, publickey)
                if res is True:
                    status.append(publickey_statur)
                    break
        if "Doctor" in status and "Lawyer" in status:
            print("Valid")
        else:
            print("Invalid")

 
if __name__ == "__main__":
    #rsa_key_creation(1)
    #rsa_key_creation(2)
    publickey = RSA.importKey(open("public1.pem", encoding = 'ISO-8859-1').read())
    privatekey = RSA.importKey(open("private1.pem", encoding = 'ISO-8859-1').read())
    '''
    text = b'HelloWorld!'
    ct = encrypt(publickey, text)
    print(ct)
    pt = decrypt(privatekey, ct)
    print(pt)
    '''
    message = b'hello'
    hash = SHA256.new(message)
    signature = sign(privatekey, hash)
    print(signature)
    res = verify(publickey, signature, hash)
    print(res)
