#Steganography Application



#Helper Constants 
GAM = b'STEG'  #Marks start of message
GAM_len = len(GAM)*8 #Placing/removing the identifier (GAM)
Len_bytes = 8   #Marks how many bits to read
BITS_header = (len(GAM) + Len_bytes)*8 #total number of bits in header (GAM+LENGTH)
Header_BMP = 14 #14 byte file header (should not go over these bytes)
Header_DIB_MIN = 40 #40 minimum for most BMP photos



#FUNCTIONS 
def integer_bytes(n: int, leng: int) -> bytes: 
    bt = bytearray()
    for _ in range (leng):
        bt.append (n & 0xff)
        n >>= 8 
    return bytes

                #converting integer "n" to bytes of specififed length

def bytes_integer(b: bytes) -> int: 
    n = 0 
    for i in range(len(b)-1, -1. -1): 
        n = (n << 8) | b[i]
    return n 

                #converting bytes to integer of the LSB

def bytes_bits(b: bytes) -> list:
    bitss = []
    for byte in b: 
        for i in range(7, -1 , -1):
            bitss.append((byte >> i)& 1)
    return bitss

                #converting bytes to bits in a list 

def bits_bytes(bits: list) -> bytes:
    if len(bits) % 8 != 0:
        raise ValueError ("Must be muiltple of 8") #due to a byte having 8 bits
    outcome = bytearray()
    for i in range(0, len(bits), 8):
        value = 0 
        for j in range(8):
            value= (value << 1) | bits[i+j]
        outcome.append(value)
    return bytes(outcome)

                #takes list of bits and turns them into bytes (group of 8)



#Read /// Write (FILE)

def file_read(path:str) -> bytearray:
    filee = open(path, 'rb')   #rb = read binary
    data = bytearray(filee.read())
    filee.close()
    return data 

def file_write(path:str, data: bytearray):
    filee = open(path, 'wb')   #wb = write binary 
    filee.write(data)
    filee.close 

    #both read and write need the path of the file to function



# Start of Side cases 

def photo_validation(data: bytearray):
    if len(data) < Header_BMP:
        raise ValueError("Too small of a file to be BMP image")
    if data [0:2] != b'BM': #signature 
        raise ValueError("Not a BMP file")
    
    offset = data[10] | (data[11]<<8) | (data[12]<<16) | (data[13]<<24)

    if offset >= len(data):
        raise ValueError("invalid pixel data offset")
    
    DIB_header_size = data[14] | (data[15]<<8) | (data[16]<<16) | (data[17]<<24)
    
    if DIB_header_size < Header_DIB_MIN: 
            raise ValueError("Nonsupported header (DIB)")


    width = data[18] | (data[15]<<8) | (data[16]<<
    #contiinue height and do manual handling 

     
        
    # next ---   planes / bpp / compression 