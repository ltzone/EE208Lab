import math
from tqdm import tqdm
import random


class Bitarray:
	def __init__(self, size):
		""" Create a bit array of a specific size """
		self.size = size
		self.bitarray = bytearray(int(math.ceil(size/8.)))

	def set(self, n):
		""" Sets the nth element of the bitarray """

		index = int(n / 8)
		position = n % 8
		self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)

	def get(self, n):
		""" Gets the nth element of the bitarray """
		
		index = int(n / 8)
		position = n % 8
		return (self.bitarray[index] & (1 << (7 - position))) > 0 

def hash_1(string):
	sed=20000819;has=0
	for i in string:
		has=has*sed+ord(i)
	return has

def hash_2(key):
	has = 0
	for i in range(len(key)):
		has = ord(key[i]) + (has << 6) + (has << 16) - has;
	return has

def hash_3(string):
	has = 0
	for i in string:
		has=((has<<(ord(i)&7))+(has>>(ord(i)&3)))^ord(i)
	return has

def hash_4(key):
	fnv_prime = 0x811C9DC5
	hash = 0
	for i in range(len(key)):
		hash *= fnv_prime
		hash ^= ord(key[i])
	return hash

def hash_5(key):
	BitsInUnsignedInt = 4 * 8
	ThreeQuarters 	= int((BitsInUnsignedInt  * 3) / 4)
	OneEighth 		= int(BitsInUnsignedInt / 8)
	HighBits  		= (0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth)
	hash  			= 0
	test  			= 0

	for i in range(len(key)):
		hash = (hash << OneEighth) + ord(key[i])
		test = hash & HighBits
		if test != 0:
			hash = (( hash ^ (test >> ThreeQuarters)) & (~HighBits));
	return (hash & 0x7FFFFFFF)

def hash_7(key):
	hash = 0xAAAAAAAA
	for i in range(len(key)):
		if ((i & 1) == 0):
			hash ^= ((hash <<  7) ^ ord(key[i]) * (hash >> 3))
		else:
			hash ^= (~((hash << 11) + ord(key[i]) ^ (hash >> 5)))
	return hash

def hash_8(key):
	hash = 0
	x	 = 0
	for i in range(len(key)):
		hash = (hash << 4) + ord(key[i])
		x = hash & 0xF0000000
		if x != 0:
			hash ^= (x >> 24)
		hash &= ~x
	return hash

def hash_6(key):
	hash = len(key);
	for i in range(len(key)):
		hash = ((hash << 5) ^ (hash >> 27)) ^ ord(key[i])
	return hash
	
def hash_9(string):
	has1=0;has2=0;
	for i in string:
		has1=(has1<<8)+(ord(i)<<(ord(i)&7))+(~(has1>>(has1&3)))
		has2=has2*(((1<<15)-1)&has1) + (ord(i)^(has2>>4))
	return has1^has2