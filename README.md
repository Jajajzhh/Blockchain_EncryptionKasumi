# Blockchain_EncryptionKasumi
A tool which enables encryption Kasumi, together with RSA and Elgamal signature, and a simulated blockchain
Projet_GS15
ZHOU HUHENG
1. Introduction:
This is the project I’ve done alone for the course GS15, it is realised in Python and I used a
few Python Modules that are to help me realise this project faster and more efficiently,
considering I was doing this project alone.
Requirements:
sympy
Crypto
libnum
hashlib
flask
(binascii
random
argparse
textwrap
json
datetime) Python 3.0 standard library included
If the project does not run, there might be modules that need to be installed. Run pip install
-r requirements.txt to install them. Please run the files in the same directory where the files
are located.
**This project is tested with the newest version of Python: Python 3.9.0
Python grammar changes very fast and compatibility with lower versions is not
assured. **
This project includes encryption, decryption of KASUMI, generation of private/public key pair
through big prime numbers, a hash function that modifies MD5 hash with a sponge structure,
signature digital through 2 ways: RSA and Elgamal, and finally a simulation of Blockchain
that could be run in 2 ways: by Command line tool and by Flusk server. Now I would go into
a bit more detail about the structure of my project, and how I realised each function.

2. General file structure:
The different functions are realised in different files for clairency, each file’s use is clearly
indicated by their name. We have:
● Kasumi_mod.py that only takes care of the core algorithme of KASUMI, with the
modifications demanded in the subject of course included.
● Inversion.py that calculates the module inverse of a number.
● Kasumi_io.py uses the previous files and functions to build the encryption system in
3 ways: ECB, CBC, PCBC.
● elgamal.py generates random big prime numbers to construct a public_private key
pair:( p, g, h, x )
● eponge_md5.py consists of the Modified MD5 hash function.● signature_elgamal, signature_RSA contains corresponding functions for the 2
methods of signature.
● blockchain_sans_node.py is the file that includes the blockchain functions. It does
not allow registration of different nodes, just a very simple simulation of a blockchain
system on one PC only. For the purpose of speed, the condition of passing a hash is
set to ‘00’. It could be modified to be more strict but takes more time in return.
● fileio.py is a simple interface to read and write data with, in order to simplify the
Command Line Interface function.
● cli.py is the point of entry, the command line interface for our program, it gathers all
the other fonctionnalites and handles user input.
● ./key directory contains all the keys to read from and write to.
● ./io_data contains all the data the program will read from and write to.
3. User manuel:
#To run the project, run the file cli.py with the newest python compiler. Assure that the other
files are under the same directory.
#After starting the cli you will enter into the interface. The options #1 and #2 are for
encryption and decryption KASUMI of files through 3 modes that could be chosen. You
would be prompted to input the mode, filename to read from, filename to write to. There
would be no choice of mode during decryption because it uses the encryption mode you
selected to decrypt.
#To test the function with a bigger file, I have a text file of a few paragraphs from [A
Christmas Carol], around 4kb. The file is named C_D for Charles Dickens.
#’3’ generates key pairs. You have to enter the name of the directory the keys are stored,
the number of bits and the confidence for the algorithme.
#’4’ generates a hash of 128 bits from any input file. As it is a sponge structure, it is very
easy to modify the number of output bits to 64 * n bits. Here it’s not yet implemented due to
lack of time.
#5, #6 generates and verifies a signature from. You have to select the mode to
use(rsa/elgamal in undercase), the file to read from, the key pair to use. Only one signature
is allowed for each mode as I find defining a new signature file brings too much trouble for
me and for the user. You get the correct response if you verify with the same key, and
naturally the false response with another key
#7, #8 does the same thing, but through 2 different ways. #7 starts a blockchain simulation in
Console. You have 3 commands: mine, display, valid. Mine creates a new block, verifies the
proof of work, then adds it to the blockchain. display shows all the contents, and valid checks
for validation of the chain.
#8 starts a flusk server, we can do the same thing through Postman or even Chrome, just
with these queries:http://127.0.0.1:5000/mine_block
http://127.0.0.1:5000/get_chain
http://127.0.0.1:5000/vali
