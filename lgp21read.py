# Read LGP-21 paper tapes from Gielmetti FER 201 with USB CDC interface
# jm 29.11.2019
#
# Input: COM port and target file name for tape data.
# Output: Writes three files,
#   .raw    raw 8-bit binary data, including leading/trailing $00 bytes
#   .flx    6-bit Flexowriter code, $00 bytes removed
#   .asc    converted to ASCII, $00 bytes removed
#
# Raw bit order on the tape is 76543/210, where 0 denotes the LSB.
# Flexowriter bit order on the paper tape is ..612/345,
# where '.' denotes unused holes, '/' the transport holes, 6 the LSB.
# The .flx file has bits in the order 123456.
# 
# to do:
# online help
# support command line parameters?


import serial
import time
import msvcrt
import os

# ------------------
# Flexowriter to ASCII conversion 
# ------------------

# Encodings different from Stuttgart utility:
#
# Delta         ($12 upper)     $5E, caret ^
# Pi            ($1E upper)     $23, hash #
# Sigma         ($22 upper)     $26, ampersand &
# Color shift   ($0C)           $0F, shift in
# Delete        ($3F)           $7F, delete

# capital letters
ASCII_cap = [  0,  90,  41,  32,   0,  66,  76,  95,
              60,  89,  42,  61,  15,  82,  34,  58,
              13,  73,  94,  63,   8,  68,  37,  93,
               9,  78,  36,  91,   0,  77,  35,  86,
              39,  80,  38,  79,   0,  69,  40,  88,
               0,  85,  70,   0,   0,  84,  71,   0,
               0,  72,  74,   0,   0,  67,  75,   0,
               0,  65,  81,   0,   0,  83,  87, 127 ]

# lowercase letters
ASCII_low = [  0, 122,  48,  32,   0,  98, 108,  45,
              62, 121,  50,  43,  15, 114,  51,  59,
              13, 105,  52,  47,   8, 100,  53,  46,
               9, 110,  54,  44,   0, 109,  55, 118,
              39, 112,  56, 111,   0, 101,  57, 120,
               0, 117, 102,   0,   0, 116, 103,   0,
               0, 104, 106,   0,   0,  99, 107,   0,
               0,  97, 113,   0,   0, 115, 119, 127 ]


# Flexowriter codes which toggle capital/lowercase
Flex_cap = 8
Flex_low = 4

# remember current state
is_cap = False
      
# ------------------
# Startup message
# ------------------

print ("Read LGP21 and LGP30 paper tapes")
print ("from Ghielmetti reader connected via USB interface.")
print ("jm 29.11.2019")
print ()
print ("Press any key during tape reading to cancel.")
print ("Enter empty port or file name to end.")
print ()

# ------------------
# open COM port
# ------------------

while True:
    port = input ("COM port (number only): ")
    if port == "": break
    try:
        ser = serial.Serial ("COM"+port, timeout=1)
        break
    except serial.SerialException:
        print ("Cannot open port COM"+port)

if port != "":
    
# ------------------
# Loop through multiple tapes & files
# ------------------

    while True:

        # clear DTR to indicate we are not ready
        ser.dtr = False

        # get output file name and open files
        while True:
            print ()
            name = input ("Output file name (without suffix): ")
            if name == "": break
            try:
                fraw = open (name+".raw", "wb")
                fflx = open (name+".flx", "wb")
                fasc = open (name+".asc", "wb")
                break
            except IOError:
                print ("Cannot create file.")

        # stop entirely if empty name enterd
        if name == "": break

        # set DTR, we are ready now
        ser.dtr = True
        cancel = False

        # wait for transmission to start.
        # no timeout desired here, as the user may still be inserting the tape.
        print ("insert tape in reader, or press any key to cancel...")
        while ser.in_waiting == 0:
            if msvcrt.kbhit():
                msvcrt.getch ()
                cancel = True
                break

        if not cancel:
            print ("reading...")
            starttime = time.time()
            bytecount = 0

            # ------------------
            # keep reading and storing data until read timeout is encountered
            # ------------------

            while True:

                # check for "emergency stop" from keyboard
                if msvcrt.kbhit():
                    msvcrt.getch ()
                    cancel = True
                    break

                # read from tape and store into output files
                b = ser.read(1)
                if len(b) == 0: break                           # end of tape
                bytecount = bytecount+1                         # count raw bytes, just for speed measurement 
                fraw.write(b)
                c = b[0]

                # unscramble bit order in Flexowriter code
                c = c << 1
                if c & 0b01000000 != 0: c = c | 0b00000001      # set bit 6
                c = c & 0b00111111                              # clear unused bits
                fflx.write (bytes([c]))

                # encode as ASCII,
                # keep track of upper/lowercase
                if c == 0: fasc.write (bytes([c]))              # preserve zeros from tape -- desirable?
                elif c == Flex_cap: is_cap = True
                elif c == Flex_low: is_cap = False
                else:
                    if is_cap: c = ASCII_cap [c]
                    else: c = ASCII_low [c]
                    if c != 0: fasc.write (bytes([c]))

            endtime = time.time()

        # tape completed (or cancelled), close files
        fraw.close ()
        fflx.close ()
        fasc.close ()
        if not cancel:
            print ("read", bytecount, "bytes,", round (bytecount/(endtime-starttime)), "byte/s.")
        else:
            print ("cancelled, removing files.")
            os.remove (fraw.name)
            os.remove (fflx.name)
            os.remove (fasc.name)

    # no more tapes (user has entered empty file name)
    ser.close ()
