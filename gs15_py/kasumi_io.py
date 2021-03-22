import kasumi_mod as kasumi
import fileio
def xor_bytes(a, b):
    """ Returns a new byte array with the elements xor'ed. """
    return bytes(i^j for i, j in zip(a, b))
class Kasumi_symtrique:
    def __init__(self,masterkey):
        self.key     = masterkey  
        self.my_kasumi = kasumi.Kasumi()
        self.my_kasumi.set_key(self.key)


    def padding(self,plaintext):
    #input of form bytes which would be padded to a number 8N bytes = N * 64 bits padded with n bytes of n (n = lengthText % 8)
        padding_len = 8 - (len(plaintext) % 8)
        padding = bytes([padding_len] * padding_len)
        return plaintext + padding

    def unpad(self,plaintext):
        padding_len = plaintext[-1]
        assert padding_len > 0
        message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
        assert all(p == padding_len for p in padding)
        return message

    def split_blocks(self, message, block_size=16, require_padding=True):
        assert len(message) % block_size == 0 or not require_padding
        return [message[i:i+16] for i in range(0, len(message), block_size)]

    def blockDivide(self, block, chunks):
        result = []
        size = len(block)//8
        print(size)
        for i in range(0, size):
            result.append( int.from_bytes( block[i*8:(i+1)*8],byteorder="little" ))
        return(result)
#Encryption ECB => Simple encryption of each block then the blocks are appended
    def encryption_ecb(self, plaintext):
        #key     = 0x9900aabbccddeeff1122334455667788  
        #my_kasumi = kasumi.Kasumi()
        #my_kasumi.set_key(key)
        plaintext = self.padding(plaintext)
        print(plaintext)
        blocks_enc = []
        blocks = self.blockDivide(plaintext,8)
        for block in blocks:
            blockcryp = self.my_kasumi.enc(block)
            block = blockcryp.to_bytes(8,byteorder="little")
            blocks_enc.append(block)
        return b''.join(blocks_enc)
        
    def decryption_ecb(self, plaintext):
        #key     = 0x9900aabbccddeeff1122334455667788  
        #my_kasumi = kasumi.Kasumi()
        #my_kasumi.set_key(key)
        blocks_dec = []
        blocks = self.blockDivide(plaintext,8)
        for block in blocks:
            print(block)
            blockcryp = self.my_kasumi.dec(block)
            block = blockcryp.to_bytes(8,byteorder="little")
            blocks_dec.append(block)
        return self.unpad(b''.join(blocks_dec))
   
    def encryption_cbc(self, plaintext, iv):
        #iv is initial vector which should be a <= 64 bit int
        #Encryption CBC plaintext ^ previous resultat => cipher KASUMI => result = next vector
        #assert kasumi._bitlen(iv) <= 64
        plaintext = self.padding(plaintext)
        print(plaintext)
        blocks_enc = []
        blocks = self.blockDivide(plaintext,8)
        previous = iv
        for block in blocks:
            # CBC mode encrypt: encrypt(plaintext_block XOR previous)
            assert kasumi._bitlen(previous) <= 64
            block = block ^ previous
            blockcryp = self.my_kasumi.enc(block)
            print("block:",hex(block),"previous:",hex(previous),"encryption:",hex(blockcryp))
            previous = blockcryp           
            #previsou then is given value of previous encryption
            blockbyte = blockcryp.to_bytes(8,byteorder="little")
            blocks_enc.append(blockbyte)
        return b''.join(blocks_enc)

    def decryption_cbc(self, ciphertext, iv):  
        assert kasumi._bitlen(iv) <= 64
        blocks = self.blockDivide(ciphertext,8)
        blocks_dec = []
        previous = iv
        for block in blocks:
            assert kasumi._bitlen(previous) <= 64
            # CBC mode decrypt: previous XOR decrypt(ciphertext)
            #for each block we do: 1.decryption KASUMI 2. Add vector previous   
            blockcryp = previous ^ self.my_kasumi.dec(block) 
            blockbyte = blockcryp.to_bytes(8,byteorder="little") 
            print("block:",hex(block),"previous:",hex(previous),"decryption:",hex(blockcryp))
            previous = block          
            blocks_dec.append(blockbyte)
        return self.unpad(b''.join(blocks_dec))

    def encryption_pcbc(self, plaintext, iv):
        #iv is initial vector which should be a <= 64 bit int
        #Encryption CBC plaintext ^ previous resultat => cipher KASUMI => result = next vector
        assert kasumi._bitlen(iv) <= 64
        plaintext = self.padding(plaintext)
        blocks_enc = []
        blocks = self.blockDivide(plaintext,8)
        previous_cipher = iv
        previous_plain = 0
        for block in blocks:
            # CBC mode encrypt: encrypt(plaintext_block XOR previous)          
            # block = block ^ previous_cipher ^ previous_plain
            blockcryp = self.my_kasumi.enc( (block ^ previous_cipher ^ previous_plain) )
            previous_cipher = blockcryp
            previous_plain = block
            print("block:",hex(block),"previous_cipher:",hex(previous_cipher),"previous_plain",hex(previous_plain),"encryption:",hex(blockcryp))
            #previsou then is given value of previous encryption
            blockbyte = blockcryp.to_bytes(8,byteorder="little")
            blocks_enc.append(blockbyte)
        return b''.join(blocks_enc)
        

    def decryption_pcbc(self, ciphertext, iv):
        assert kasumi._bitlen(iv) <= 64
        blocks = self.blockDivide(ciphertext,8)
        blocks_dec = []
        previous_plain = 0
        previous_cipher = iv
        for block in blocks:
            assert kasumi._bitlen(previous_cipher) <= 64
            blockdecry = self.my_kasumi.dec(block)
            blockdecry = blockdecry ^ previous_cipher ^ previous_plain
            previous_cipher = block
            previous_plain = blockdecry
            print("block:",hex(block),"previous_cipher:",hex(previous_cipher),"previous_plain",hex(previous_plain),"encryption:",hex(blockdecry))
            blockbyte = blockdecry.to_bytes(8,byteorder="little") 
            blocks_dec.append(blockbyte)
            # CBC mode decrypt: previous XOR decrypt(ciphertext)
            #for each block we do: 1.decryption KASUMI 2. Add vector previous               
        return self.unpad(b''.join(blocks_dec))

if __name__ == '__main__':
    key     = 0x9900aabbccddeeff1122334455667788  
    msg = "hillooverby2_fuckgs15"
    arr = bytes(msg, 'utf-8')
    kasumsym = Kasumi_symtrique(key)
    iv = 0x121a12340987198
    #msg_enc = kasumsym.encryption_ecb(arr)
    #msg_dec = kasumsym.decryption_ecb(msg_enc)
    #msg_enc = kasumsym.encryption_cbc(arr,iv)
    #msg_dec = kasumsym.decryption_cbc(msg_enc,iv)
    arr = fileio.readfile('data.txt')
    msg_enc = kasumsym.encryption_pcbc(arr,iv)
    fileio.writefile('enc',msg_enc)
    msg_dec = fileio.readfile('enc')
    msg_dec = kasumsym.decryption_pcbc(msg_enc,iv)
    fileio.writefile('dec',msg_dec)
    print(arr)
    print(msg_enc)
    print(msg_dec)