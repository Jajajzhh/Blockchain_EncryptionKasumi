import sys
import os.path
#Simple file that only serves to simplify input output interaction
def readfile(fname):
    fname = 'io_data/' + fname 
    if not os.path.exists(fname):
        print("File does not exist.")
        return b'error'
    else:
        to_hash = open(fname,"rb")
        data = to_hash.read()
        return data
def writefile_append(fname,data):
    fname = 'io_data/' + fname 
    if os.path.exists(fname):
        print("File already exist. will append to exsisting file")
        to_hash = open(fname,"ab") 
        to_hash.write(data)
        to_hash.close()
        return
    else:    
        to_hash = open(fname,"wb")    
        to_hash.write(data)
        to_hash.close()

def writefile(fname,data):
    fname = 'io_data/' + fname 
    if os.path.exists(fname):
        print("File already exist. will overwrite file")
        to_hash = open(fname,"wb") 
        to_hash.write(data)
        to_hash.close()
        return
    else:    
        to_hash = open(fname,"wb")    
        to_hash.write(data)
        to_hash.close()
#file = readfile('data.txt')
#print(file)
#writefile('data.txt',b'text change')
     