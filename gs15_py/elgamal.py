import random
import math
import sys
import os
class PrivateKey(object):
	def __init__(self, p=None, g=None, x=None, iNumBits=0):
		self.p = p
		self.g = g
		self.x = x
		self.iNumBits = iNumBits

class PublicKey(object):
	def __init__(self, p=None, g=None, h=None, iNumBits=0):
		self.p = p
		self.g = g
		self.h = h
		self.iNumBits = iNumBits

# computes the greatest common denominator of a and b.  assumes a > b
def gcd( a, b ):
		while b != 0:
			c = a % b
			a = b
			b = c
		#a is returned if b == 0
		return a

#computes base^exp mod modulus
def modexp( base, exp, modulus ):
		return pow(base, exp, modulus)

#solovay-strassen primality test.  tests if num is prime
def SS( num, iConfidence ):
		#ensure confidence of t
		for i in range(iConfidence):
				#choose random a between 1 and n-2
				a = random.randint( 1, num-1 )

				#if a is not relatively prime to n, n is composite
				if gcd( a, num ) > 1:
						return False

				#declares n prime if jacobi(a, n) is congruent to a^((n-1)/2) mod n
				if not jacobi( a, num ) % num == modexp ( a, (num-1)//2, num ):
						return False

		#if there have been t iterations without failure, num is believed to be prime
		return True

#computes the jacobi symbol of a, n
def jacobi( a, n ):
		if a == 0:
				if n == 1:
						return 1
				else:
						return 0
		#property 1 of the jacobi symbol
		elif a == -1:
				if n % 2 == 0:
						return 1
				else:
						return -1
		#if a == 1, jacobi symbol is equal to 1
		elif a == 1:
				return 1
		#property 4 of the jacobi symbol
		elif a == 2:
				if n % 8 == 1 or n % 8 == 7:
						return 1
				elif n % 8 == 3 or n % 8 == 5:
						return -1
		#property of the jacobi symbol:
		#if a = b mod n, jacobi(a, n) = jacobi( b, n )
		elif a >= n:
				return jacobi( a%n, n)
		elif a%2 == 0:
				return jacobi(2, n)*jacobi(a//2, n)
		#law of quadratic reciprocity
		#if a is odd and a is coprime to n
		else:
				if a % 4 == 3 and n%4 == 3:
						return -1 * jacobi( n, a)
				else:
						return jacobi(n, a )


#finds a primitive root for prime p
#this function was implemented from the algorithm described here:
#http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
def find_primitive_root( p ):
		if p == 2:
				return 1
		#the prime divisors of p-1 are 2 and (p-1)/2 because
		#p = 2x + 1 where x is a prime
		p1 = 2
		p2 = (p-1) // p1

		#test random g's until one is found that is a primitive root mod p
		while( 1 ):
				g = random.randint( 2, p-1 )
				#g is a primitive root if for all prime factors of p-1, p[i]
				#g^((p-1)/p[i]) (mod p) is not congruent to 1
				if not (modexp( g, (p-1)//p1, p ) == 1):
						if not modexp( g, (p-1)//p2, p ) == 1:
								return g

#find n bit prime
def find_prime(iNumBits, iConfidence):
		#keep testing until one is found
		while(1):
				#generate potential prime randomly
				p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
				#make sure it is odd
				while( p % 2 == 0 ):
						p = random.randint(2**(iNumBits-2),2**(iNumBits-1))

				#keep doing this if the solovay-strassen test fails
				while( not SS(p, iConfidence) ):
						p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
						while( p % 2 == 0 ):
								p = random.randint(2**(iNumBits-2), 2**(iNumBits-1))

				#if p is prime compute p = 2*p + 1
				#if p is prime, we have succeeded; else, start over
				p = p * 2 + 1
				if SS(p, iConfidence):
						return p
#generates public key K1 (p, g, h) and private key K2 (p, g, x)
def generate_keys(iNumBits=256, iConfidence=32):
		#p is the prime
		#g is the primitve root
		#x is random in (0, p-1) inclusive
		#h = g ^ x mod p
		p = find_prime(iNumBits, iConfidence)
		g = find_primitive_root(p)
		g = modexp( g, 2, p )
		x = random.randint( 1, (p - 1) // 2 )
		h = modexp( g, x, p )
		publicKey = PublicKey(p, g, h, iNumBits)
		privateKey = PrivateKey(p, g, x, iNumBits)
		return {'privateKey': privateKey, 'publicKey': publicKey}
#Use the fonction above to store the key values (p, g, h, x) g generator, p random prime, x random int private key. h = g**x mod p public key 
def create_keypair(iNumBits=256, iConfidence=16, usernum='test_elgamal'):
	keypair = generate_keys(iNumBits,iConfidence)	
	private = keypair['privateKey']
	pub = keypair['publicKey']
	print('p: ',pub.p)
	print('g: ',pub.g)
	print('h: ',pub.h)
	print('x: ',private.x)
    #print(elgamal.test())
	dirpriv = 'key/elgamal/' + usernum +'/privkey_x.pem'
	dripub_p = 'key/elgamal/' + usernum +'/pubkey_p.pem'
	dripub_h = 'key/elgamal/' + usernum +'/pubkey_h.pem'
	dripub_g = 'key/elgamal/' + usernum +'/pubkey_g.pem'
	if not os.path.exists('key/elgamal/' + usernum + '/'):
		os.mkdir('key/elgamal/' + usernum + '/') 
	with open(dirpriv, 'wb') as f:
		f.write(int.to_bytes(private.x, iNumBits, byteorder="little"))
	with open(dripub_p, 'wb') as f:
		f.write(int.to_bytes(pub.p, iNumBits, byteorder="little"))
	with open(dripub_h, 'wb') as f:
		f.write(int.to_bytes(pub.h, iNumBits, byteorder="little"))
	with open(dripub_g, 'wb') as f:
		f.write(int.to_bytes(pub.g, iNumBits, byteorder="little"))
	f.close()	
    


if __name__ == '__main__':
    #keypair = generate_keys(512,32)
	create_keypair(512,4)
    #private = keypair['privateKey']
    #public = keypair['publicKey']
    #print(private.p)
    #print(public.p)
    #print(elgamal.test())

    

