file = "/dev/hidraw0"

# def readTemperature():
while(1):
    fp = open(file,'rb')

    buffer = fp.read(4)
    buffer = buffer[2:]
    # print(buffer)
    buffer = int.from_bytes(buffer, byteorder="big") #311
    buffer /= 10 
    print(buffer)
    # return(buffer)
