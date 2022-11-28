from inspect import _void
from io import BufferedReader
import sys

def start(file : BufferedReader):
    """
        Helper function that passes on the file information
        to a printer function.
    """

    raw_data = file.read().hex()
    print_hex(raw_data)
    

def print_hex(data : str):
    """ 
        Workhorse function that breaks the input data into chunks
        of 32 characters. Separates them further into 16 & 16, which
        allows for easy spacing and counting.
        Calls get_ascii() to process perusal format.
    """

    str(data) if type(data) != str else None    #type check

    for num in range(0, len(data), 32):     #step by 32
        l = [data[num:num+16], data[num+16:num+32]]        #segment the data into 2 chunks of 16 chars
        s = [(" ".join(l[0][i:i+2] for i in range(0, len(l[0]), 2))).strip(),
            (" ".join(l[1][i:i+2] for i in range(0, len(l[1]), 2))).strip()]    #adds spaces every 2 chars
        print_str = (f"{format(num//2, '#010x')[2:]}  {s[0]}  {s[1]}").ljust(58)    #adds number on the left & proper spacing for ascii

        print(f"{print_str}  |{get_ascii(data[num:num+32])}|")  #calls get_ascii() with entire row of 32
    print(format(len(data)//2, '#010x')[2:]) if len(data) != 0 else None    #always outputs end length at last row


def get_ascii(data : str) -> str:
    """
        Processes even numbered data bytes in hex into ASCII chars,
        within perusal foramt range (0x20 to 0x7E inclusive)
    """

    if (len(data) % 2 != 0):
        return Exception("input length not even, cannot process bytes properly")

    temp_str = ""
    for num in range(0, len(data), 2):  #step by 2 (even to get both bytes in chunk)
        hx = data[num:num+2]
        if eval("0x"+hx) in range(0x20, 0x7F):  #inclusive range for perusal format
            temp_str += bytes.fromhex(hx).decode("utf-8")   #decode from hex to ASCII
        else:
            temp_str += "."    #if not in range, just turn it into a '.'
    return temp_str


if __name__ == "__main__":
    if len(sys.argv) == 2:    
        with open(sys.argv[1], 'rb') as f:
            start(f)
    else:
        print(Exception("missing 2nd argument (file name)"))
    