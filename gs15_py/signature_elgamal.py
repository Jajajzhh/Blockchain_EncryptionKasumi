from Crypto.Util.number import *
from Crypto import Random
import Crypto
import libnum
import sys
#import fileio
from random import randint
import hashlib
import os
import sys
#elgamal signature
class Sign_elgamal(object):
        def __init__(self, bits = 512, usernum = 'sign_elgamal'):
                #pgsv the keys g generator, p random prime, x random int private key. h = g**x mod p public key 
                self.bit = bits
                #private key x
                self.dirpriv = 'key/elgamal/' + usernum + '/privkey_x.pem'               
                self.dripub_p = 'key/elgamal/' + usernum + '/pubkey_p.pem'
                self.dripub_h = 'key/elgamal/' + usernum + '/pubkey_h.pem'
                self.dripub_g = 'key/elgamal/' + usernum + '/pubkey_g.pem'
                if not os.path.exists(self.dirpriv):
                        print("creation de cle")
                        self.p = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
                        self.g=2
                        self.x= randint(0, self.p-1)
                        self.h = pow(self.g,self.x,self.p)
                        if not os.path.exists('key/elgamal/' + usernum + '/'):
                                os.mkdir('key/elgamal/' + usernum + '/') 
                        with open(self.dirpriv, 'wb') as f:
                                f.write(int.to_bytes(self.x, bits, byteorder="little"))                              
                        with open(self.dripub_p, 'wb') as f:
                                f.write(int.to_bytes(self.p, bits, byteorder="little"))                        
                        with open(self.dripub_h, 'wb') as f:
                                f.write(int.to_bytes(self.h, bits, byteorder="little"))                         
                        with open(self.dripub_g, 'wb') as f:
                                f.write(int.to_bytes(self.g, bits, byteorder="little"))
                                
                        f.close()	
                else:
                        with open(self.dripub_p, 'rb') as f:
                                self.p = int.from_bytes(f.read(),byteorder="little")
                        with open(self.dripub_g, 'rb') as f:
                                self.g= int.from_bytes(f.read(),byteorder="little")
                        with open(self.dirpriv, 'rb') as f:
                                self.x= int.from_bytes(f.read(),byteorder="little")
                        with open(self.dripub_h, 'rb') as f:
                                self.h = int.from_bytes(f.read(),byteorder="little")
        
        def sign(self, msg):
                e= Crypto.Util.number.getPrime(self.bit, randfunc=Crypto.Random.get_random_bytes)
                # e_1=(gmpy2.invert(e, p-1))
                e_inv=(libnum.invmod(e, self.p-1))
                #D=  bytes_to_long(msg.encode('utf-8')) // if you want direct signing
                D = int.from_bytes(hashlib.sha256(msg).digest(),byteorder='big' )
                Sign_r=pow(self.g, e, self.p)
                Sign_s=((D-self.x*Sign_r)*e_inv) % (self.p-1)
                print ("\nS_1= %s" % Sign_r)
                print ("S_2=%s" % Sign_s)
                return Sign_r, Sign_s
        
        def verify(self, msg, S_r, S_s):
                D = int.from_bytes(hashlib.sha256(msg).digest(),byteorder='big' )
                v_1 = (pow(self.h,S_r,self.p)*pow(S_r,S_s,self.p))%self.p
                v_2 = pow(self.g,D,self.p)
                print ("\nV_1=%s" % v_1)
                print ("\nV_2=%s" % v_2)
                if(v_1 == v_2):
                        print("Signature is valid.")
                else:
                        print("The signature is not valid!!")

                return v_1 == v_2
        
if __name__=='__main__':
        bits=512
        msg="Hello"
        msg_2 = "Hello"
        if (len(sys.argv)>1):
                msg=str(sys.argv[1])
        if (len(sys.argv)>2):
                bits=int(sys.argv[2])
        #elgaml = Sign_elgamal(bits)
        elgaml = Sign_elgamal(bits,'1')
        rr, ss = elgaml.sign(bytes(msg,"utf-8"))
        elgaml = Sign_elgamal(bits, 'example')
        result = elgaml.verify(bytes(msg_2,"utf-8"),rr,ss)

