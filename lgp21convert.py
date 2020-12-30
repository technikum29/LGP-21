# Convert raw 8-bit papertape images
# to LGP-21 Flexowriter and to ASCII code
# jm 29.11.2019
#
# Input: File name for ".raw" file
# Output: Writes two files,
#   .flx2    6-bit Flexowriter code, incl $00 bytes 
#   .asc2    converted to ASCII, incl $00 bytes
#
# Raw bit order on the tape is 76543/210, where 0 denotes the LSB.
# Flexowriter bit order on the paper tape is ..612/345,
# where '.' denotes unused holes, '/' the transport holes, 6 the LSB.
# The .flx2 file has bits in the order 123456.



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

print ("Convert LGP21 and LGP30 paper tape images")
print ("from raw 8-bit to Flexowriter 6-bit and ASCII 8-bit code.")
print ("jm 29.11.2019")
print ()
print ("Enter empty file name to end.")

    
# ------------------
# Loop through multiple tapes & files
# ------------------

while True:

    # get output file name and open files
    while True:
        print ()
        name = input ("File name (without suffix): ")
        if name == "": break
        try:
            fraw = open (name+".raw",  "rb")
            fflx = open (name+".flx2", "wb")
            fasc = open (name+".asc2", "wb")
            break
        except IOError:
            print ("Cannot find or create file.")

    # stop entirely if empty name enterd
    if name == "": break

    print ("reading", name+".raw")
    print ("writing", name+".flx2")
    print ("writing", name+".asc2")

    # ------------------
    # keep reading and storing data until read timeout is encountered
    # ------------------

    while True:

        # read from raw file and store into output files
        b = fraw.read(1)
        if len(b) == 0: break                           # end of tape
        c = b[0]

        # unscramble bit order in Flexowriter code
        c = c << 1
        if c & 0b01000000 != 0: c = c | 0b00000001      # set bit 6
        c = c & 0b00111111                              # clear unused bits
        fflx.write (bytes([c]))

        # encode as ASCII,
        # keep track of upper/lowercase
        if c == 0: fasc.write (bytes([c]))              # preserve zeros from tape -- desirable?
        elif   c == Flex_cap: is_cap = True
        elif c == Flex_low: is_cap = False
        else:
            if is_cap: c = ASCII_cap [c]
            else: c = ASCII_low [c]
            if c != 0: fasc.write (bytes([c]))


    # tape completed (or cancelled), close files
    print ("done.")
    fraw.close ()
    fflx.close ()
    fasc.close ()

# no more tapes (user has entered empty file name)

