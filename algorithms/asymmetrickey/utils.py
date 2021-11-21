import math
import codecs
import base64 

class Utils:
    def __init__(self):
        '''if not used then delete'''
    
    def hex_to_dec(hex):
        deci = int(hex, 16)
        return deci

    def dec_to_hex(dec):
        hexa = hex(dec)
        return hexa

    def hex_to_b64(hex):
        hex = hex[2:] if(len(hex[2:]) % 2 == 0) else '0' + hex[2:]
        b64 = codecs.encode(codecs.decode(hex, 'hex'), 'base64').decode()
        return b64
       
    def b64_to_hex(b64):
        hexa = base64.b64decode(b64).hex()
        return hexa
    
    def dec_to_b64(dec):
        b64 = Utils.hex_to_b64(Utils.dec_to_hex(dec))
        return b64

    def b64_to_dec(b64):
        deci = Utils.hex_to_dec(Utils.b64_to_hex(b64))
        return deci

    def string_to_b64(string):
        b64= base64.b64encode(string.encode("ascii")).decode("ascii")
        return b64

    def b64_to_string(b64):
        string = base64.b64decode(b64.encode("ascii")).decode("ascii")
        return string

    def is_square(i):
        return i == math.isqrt(i) ** 2

    def mod_sqrt(n, p):

        points = []
        n = n % p
        for x in range (1, p):
            if (pow(x, 2, p) == n):
                points.append(x)
        return points
