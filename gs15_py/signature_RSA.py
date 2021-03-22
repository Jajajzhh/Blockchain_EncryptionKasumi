from Crypto.PublicKey import RSA
import errno
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from hashlib import sha512
from os import mkdir
from os import _exists
#RSA signature
class Sign_hash:
    def __init__(self, usernum):
        #Using Crypto Library to generate, export and import key pair instead of using the generated key in #3 
        dirpriv = 'key/' + usernum +'/privkey.pem'
        dirpub = 'key/' + usernum +'/pubkey.pem'
        try:
            with open(dirpriv, 'r') as f:
                self.keyPair = RSA.importKey(f.read())
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise
                # No private key, generate a new one. This can take a few seconds.
            if not _exists('key/elgamal/' + usernum + '/'):
                mkdir('key/' + usernum + '/')    
            self.keyPair = RSA.generate(bits=1024)
            with open(dirpriv, 'wb') as f:
                f.write(self.keyPair.exportKey('PEM'))
            with open(dirpub, 'wb') as f:
                f.write(self.keyPair.publickey().exportKey('PEM'))
    def sign(self, message):
        #keyPair = RSA.generate(bits=1024)
        print(f"Public key:  (n={hex(self.keyPair.n)}, e={hex(self.keyPair.e)})")
        print(f"Private key: (n={hex(self.keyPair.n)}, d={hex(self.keyPair.d)})")
        # RSA sign the message
        msg = message
        from hashlib import sha512
        hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
        signature = pow(hash, self.keyPair.d, self.keyPair.n)
        print("Signature:", hex(signature))
        return signature

    def verify(self, message, signature):
        #message in bytes
        msg = message
        hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
        hashFromSignature = pow(signature, self.keyPair.e, self.keyPair.n)
        print('Hash1:', hex(hash))
        print('Hash2:', hex(hashFromSignature))
        print("Signature valid:", hash == hashFromSignature)
        if(hash == hashFromSignature):
            return True
        else:
            return False
        
##################

####################
if __name__ == '__main__':
    signature = Sign_hash('1')
    signed = signature.sign(b'A message for sign')
    verify = signature.verify(b'A message for sign',signed)
    print(hex(signed))
#keyPair = RSA.generate(bits=1024)
#print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
#print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")
# RSA sign the message
#msg = b'A message for signing'
#from hashlib import sha512
#hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
#signature = pow(hash, keyPair.d, keyPair.n)
#print("Signature:", hex(signature))
# RSA verify signature
#msg = b'A message for signing'
#hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
##hashFromSignature = pow(signature, keyPair.e, keyPair.n)
#print("Signature valid:", hash == hashFromSignature)
# RSA verify signature (tampered msg)
#msg = b'A message for signing (tampered)'
#hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
#hashFromSignature = pow(signature, keyPair.e, keyPair.n)
#print("Signature valid (tampered):", hash == hashFromSignature)