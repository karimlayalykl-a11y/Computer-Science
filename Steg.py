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


    width = (data[18] | (data[19]<<8) | (data[20]<<16) | (data[21]<<24))
    height = (data[22] | (data[23]<<8) | (data[24]<<16) | (data[25]<<24))
    # W & H (bytes 28-25)

    if width & (1 << 31):
        width -=(1 << 32)
    if height & (1 << 31):
        height -=(1 << 32)


    planes = data[26] | (data[27]<<8) #planes = bytes 26-27
    if planes != 1:
        raise ValueError("Number of planes are unexpected")
    
    Bits_per_pixel = data[28] | (data[29]<<8)  #bbp = bytes 28-29
    if Bits_per_pixel !=24:
        raise ValueError("only 24 bit BMP are supported")
    
    compressionn = data[30] | (data[31]<<8) | (data[32]<<16) | (data[33]<<24)
    if compressionn != 0:
        raise ValueError("Any compressed BMP are not supported")

    return offset, width, abs(height), Bits_per_pixel

    



        #capacity checker (capacity calculation)
    

def capacity__bits_BMP(data: bytearray, p_offset:int): #calculating available bits for the LSB embed
    sum_bytes = len(data) - p_offset
    if sum_bytes <= 0:
        return 0
    return sum_bytes  #1 bit for every byte
    



        #start of    EMBDDING /////// EXTRACTION


def bit_embeded(imagee: bytearray, offset: int, bits: list):
    Maximum_bits = capacity__bits_BMP(imagee, offset)
    if len(bits) > Maximum_bits
        raise ValueError("Not enough space in image")
    for i, bit in enumerate(bits):
        id = offset + i
        imagee[id] = (imagee(id) & 0xFE) | bit 
    return imagee
# loop walks through image bytes and hides one bit inside the LSB of each byte
#enumerate helps with when needing both imgae and its index in a loop

def extraction_bits(imagee: bytearray, offset: int, number_bits: int):
    maximum_bits = capacity__bits_BMP(imagee, offset)
    if number_bits > maximum_bits:
        raise ValueError("Not enough data in image")
    bitss = []
    for i in range(number_bits):
        bitss.append(imagee[offset+i] & 1)
    return bitss

#extracting bits from the LSB of the image 





            #ENCODING //// DECODING 
def ENCODE(image_path: str, out_path: str, message_bytes: bytes):
    data = file_read(image_path)
    offset, width, height, bit_per_pixel = photo_validation(data)
    capacity = capacity__bits_BMP(data, offset)

    bytes_length = integer_bytes(len(message_bytes), Len_bytes)
    PL = GAM + Len_bytes + message_bytes
    PL_bits = bytes_bits(PL)
    if len(PL_bits) > capacity:
        raise ValueError("Message to large to embed")
    bit_embeded(data, offset, PL_bits)
    file_write(out_path, data)
    print ("Message has been encoded into image successfully.")

#offset is to start embedding at pixel data, skipping the header atm
#payload which is manditory for recognigtion 
#Start embedding the LSB one bit per byte 
#adding the signature
#Capacity checker
#Conversion 


def DECODE(image_path: str):
    data = file_read(image_path)
    offset, width, height, bit_per_pixel = photo_validation(data)

    bits_header = extraction_bits(data, offset, BITS_header)
    bytes_header = bits_bytes(bits_header)
    if bytes_header[0:4] != GAM:
        raise ValueError("GAM not found; No Message to decode.")
    Len_bytes = bytes_header[4:12]
    Message_length = bytes_integer(Len_bytes)

    Message_bits = extraction_bits(data, offset, BITS_header, Message_length*8)
    Message_bytes = bits_bytes(Message_bits)
    return Message_bytes


#Header extraction = getting message length 
#Making sure that there is an actual message to decode
#checking signature 
#LSB extraction one bit oer byte from the pixel data
#conversion 





            #USER input for steg application (MESSAGE)(TYPED OR FILE)
def bytes_message():
    mode = input("\n Please Choose your message input; (Type message / Provide file): ").strip().lower()
    if mode == " " or mode == 'type':
        print("Please Enter Message (Leave an empty line when done)")
        msg = []
        while True:
            msg = input()
            if msg == '':
                break 
            msg.append(msg)
        return '\n'.join(msg).encode('utf-8')
    elif mode == 'file':
        msg_path = input("Enter the path to the text file you want to encode").strip()
        f = open(msg_path, 'rb')
        data = f.read()
        f.close()
        return data
    else:
        print("Invalid Choice, please choose betweent the given option")
        return bytes_message
    
    