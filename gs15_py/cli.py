import argparse
import sys
import textwrap
#Import all the function files
import kasumi_io as Kasumi
import fileio 
import eponge_md5
import signature_RSA
import signature_elgamal
import elgamal as key_generate
import blockchain_sans_node as bl
def chiffreKasumi(inputfile, outputfile, mode, key=0x9900aabbccddeeff1122334455667788, iv=0x121a12340987198 ):
    inputfile = fileio.readfile(inputfile)  
    kasumsym = Kasumi.Kasumi_symtrique(key)
    if mode == 'ecb':
        msg_enc = kasumsym.encryption_ecb(inputfile)
    elif mode == 'cbc':
        msg_enc = kasumsym.encryption_cbc(inputfile,iv)
    elif mode == 'pcbc':
        msg_enc = kasumsym.encryption_pcbc(inputfile,iv)
    else:
        msg_enc = kasumsym.encryption_ecb(inputfile)
    print(inputfile)
    print(msg_enc)
    fileio.writefile(outputfile,msg_enc)
    return msg_enc
def dechifKasumi(inputfile, outputfile, mode, key=0x9900aabbccddeeff1122334455667788, iv=0x121a12340987198 ): 
    inputfile = fileio.readfile(inputfile)   
    kasumsym = Kasumi.Kasumi_symtrique(key)
    if mode == 'ecb':
        msg_dec = kasumsym.decryption_ecb(inputfile)
    elif mode == 'cbc':
        msg_dec = kasumsym.decryption_cbc(inputfile,iv)
    elif mode == 'pcbc':
        msg_dec = kasumsym.decryption_pcbc(inputfile,iv)
    else:
        msg_dec = kasumsym.decryption_ecb(inputfile)
    print(inputfile)
    print(msg_dec)
    fileio.writefile(outputfile,msg_dec)
    return msg_dec
    
def signature(inputfile, mode_signature, key='1'):
    inputfile = fileio.readfile(inputfile)
    if mode_signature == 'elgamal':
        signature = signature_elgamal.Sign_elgamal(512,key)
        rr, ss = signature.sign(inputfile)
        fileio.writefile('rr_signed', rr.to_bytes(128,byteorder='big'))
        fileio.writefile('ss_signed', ss.to_bytes(128,byteorder='big'))
    else:
        signature = signature_RSA.Sign_hash(key)
        signed = signature.sign(inputfile)
        fileio.writefile('rsa_signed', signed.to_bytes(128,byteorder='big'))
    return signature

def blockchain_Cli():
    blmode = 'def'
    blockchain = bl.Blockchain() 
    while blmode != 'quit':
        print("Vous etes dans la mode BlockChain_CLI, choisir une commande: mine/display/valid/quit")
        print("\nmine pour creer un nouveau block avec emprinte de travail. display affiche tous les blocks. valid verifie la validite")
        blmode = input('/>')
        if blmode == 'mine':
            blockchain.mine_block_cli()
        elif blmode == 'display':
            blockchain.display()
        elif blmode == 'valid':
            blockchain.valid()
        else:
            blockchain.display()

if __name__ == "__main__":
    # Banner
    print('''
    .d8888b.   .d8888b.   d888  888888888       
    d88P  Y88b d88P  Y88b d8888  888             
    888    888 Y88b.        888  888             
    888         "Y888b.     888  8888888b.       
    888  88888     "Y88b.   888       "Y88b      
    888    888       "888   888         888      
    Y88b  d88P Y88b  d88P   888  Y88b  d88P      
    "Y8888P88  "Y8888P"  8888888 "Y8888P"
    ''')
    menu = {}
    menu['[1]'] = "Chiffrement KASUMI"
    menu['[2]'] = "Dechiffrement KASUMI"
    menu['[3]'] = "Gneneration PUBLIC KEY PRIVATE KEY PAIR by ElGAMAL"
    menu['[4]'] = "Generattion Hash Par SPONGE_MODIFIED_MD5"
    menu['[5]'] = "Generattion d'un SIGNATURE"
    menu['[6]'] = "Verification d'un SIGNATURE"
    menu['[7]'] = "Commence BLOCKCHAIN par CLI"
    menu['[8]'] = "Commence BLOCKCHAIN par Server Simulation"
    menu['[9]'] = "Arreter la programme"
    #sets the default encryption mode as ecb
    mode = 'ecb'
    #sets the default signature mode as rsa
    mode_signature = 'rsa'
    elgamal = signature_elgamal.Sign_elgamal(512)
    rsa = signature_RSA.Sign_hash('1')
    while True:
        print("\n--- GS15 Main Menu")
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])
        selection = input("/> ")
        #Do action according to input
        if selection == '1':
            print("Encryption KASUMI: Selection de mode: ecb, cbc, pcbc")
            mode = input('/>')
            print("Enter file directory to read from")
            inputfile = input('/>')
            print("Enter file directory to write to")
            outputfile = input('/>')
            chiffreKasumi(inputfile,outputfile,mode)
        elif selection == '2':
            print("Dechiffrement KASUMI:\n")
            print("Enter file directory to read from")
            inputfile = input('/>')
            print("Enter file directory to write to")
            outputfile = input('/>')
            dechifKasumi(inputfile,outputfile,mode)
        elif selection == '3':
            print("Generation de nombre primaire cle pair\n")
            print("Enter a name of key pair you want to create:")
            name = input('/>')
            print("Enter number of bits:")
            nbits = int(input('/>'))
            print("Enter number Confidence:")
            confidence = int(input('/>'))
            key_generate.create_keypair(nbits,confidence,name)
            print('Generation de cle fini. Trouve ces valeurs dans le fichier key/elgamal/name_key')
        elif selection == '4':
            print("Generation de hashage sans signature avec Modified MD5\n")
            print("Enter file directory to read from")
            inputfile = input('/>')
            print("Enter file directory to write to")
            outputfile = input('/>')
            inputfile = fileio.readfile(inputfile)
            hashsponge = eponge_md5.hash_sponge(inputfile)
            print('Hashage generation finished')
            fileio.writefile(outputfile,hashsponge.to_bytes(16,byteorder='big'))
        elif selection == '5':
            print("Signature avec cle pair en mode RSA ou Elgamal: First select your mode")
            mode_signature = input('/>')
            print("Enter file directory to read from")
            inputfile = input('/>')
           
            print("Enter the name of key pair to use")
            name_key = input('/>')          
            if mode_signature == 'elgamal':
                elgamal = signature(inputfile, mode_signature,name_key)
            else:
                rsa = signature(inputfile, mode_signature,name_key)
        elif selection == '6':
            print("Verification de signature avec cle pair en mode RSA ou Elgamal: First select your mode")
            print("Signature avec cle pair en mode RSA ou Elgamal: First select your mode")
            mode_signature = input('/>')
            print("Enter file directory to read from")
            inputfile = input('/>')
            print("Enter the name of key pair to use")
            name_key = input('/>')
            #signed = int.from_bytes(fileio.readfile(inputfile),byteorder='big')
            inputfile = fileio.readfile(inputfile)
            verif = False
            if mode_signature == 'elgamal':    
                elgamal = signature_elgamal.Sign_elgamal(512, name_key)    
                rr = int.from_bytes(fileio.readfile('rr_signed'),byteorder='big')
                ss = int.from_bytes(fileio.readfile('ss_signed'),byteorder='big')
                verif = elgamal.verify(inputfile,rr,ss)
            else:
                signed = int.from_bytes(fileio.readfile('rsa_signed'),byteorder='big')
                rsa = signature_RSA.Sign_hash(name_key)
                verif = rsa.verify(inputfile,signed)
            if verif == True:
                print("\nLa signature est juste")
            else:
                print("\nLa signature n'est pas correcte")
        elif selection == '7':
            print("Commence de programme Blockchain en CLI")
            blockchain_Cli()
        elif selection == '8':
            print('Commence de server Flusk pour Blockchain')
            bl.run_server()
        elif selection == '9':
            break
        else:
            print("Unknown Option Selected!")

