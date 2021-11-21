from .utils import Utils

import random

class ElGamal:
    def __init__(self):
        pass

    def create_key(self, p, g, x):
        y = pow(g, x, p)
        public_key = { 'y': y, 'g': g, 'p': p }
        private_key = { 'x': x, 'p': p }
        return public_key, private_key

    def encrypt(self, message, key, public_key):
        a = pow(public_key['g'], key, public_key['p'])
        b = (pow(public_key['y'], key, public_key['p']) * (message % public_key['p'])) % public_key['p']
        return { 'a': a, 'b': b }

    def decrypt(self, message, private_key):
        return ((message['b'] % private_key['p']) * pow(message['a'], (private_key['p'] - 1 - private_key['x']), private_key['p'])) % private_key['p']

class ElGamalMachine:
    def __init__(self):
        self.elgamal = ElGamal()
    
    def is_prime(self, num, test_count=1000):
        if(num == 1):
            return False
        if(test_count >= num):
            test_count = num - 1
        for _ in range(test_count):
            val = random.randint(1, num - 1)
            if(pow(val, num-1, num) != 1):
                return False
        return True
    def create_random_prime(self, bit):
        found = False
        while not found:
            p = random.randint(2**(bit-1)+1, 2**bit-1)
            if self.is_prime(p):
                return p
    
    def create_key(self, bit):
        p = self.create_random_prime(bit)
        g = random.randint(1, p - 1)
        x = random.randint(1, p -2)

        public_key, private_key = self.elgamal.create_key(p, g, x)

        public_key['y'] = Utils.dec_to_b64(public_key['y'])
        public_key['g'] = Utils.dec_to_b64(public_key['g'])
        public_key['p'] = Utils.dec_to_b64(public_key['p'])

        private_key['x'] = Utils.dec_to_b64(private_key['x'])
        private_key['p'] = Utils.dec_to_b64(private_key['p'])

        pub_key = public_key['y'] + public_key['g'] + public_key['p']
        pri_key = private_key['x'] + private_key['p']

        return pub_key, pri_key

    def create_key_file(self, bit):
        public_key, private_key = self.create_key(bit)

        pub = open("key.pub", "w")
        pub.write(public_key)

        pri = open("key.pri", "w")
        pri.write(private_key)
        

    def encrypt(self, message, public_key):
        y = Utils.b64_to_dec(public_key['y'])
        g = Utils.b64_to_dec(public_key['g'])
        p = Utils.b64_to_dec(public_key['p'])

        p_key = { 'y': y, 'g': g, 'p': p }

        encrypted = ''
        for m in message:
            k = random.randint(1, p-2)
            res = self.elgamal.encrypt(ord(m), k, p_key)
            a = Utils.dec_to_b64(res['a'])
            b = Utils.dec_to_b64(res['b'])
            encrypted += a + b
        return encrypted

    def encrypt_full(self, message, pub_key):
        public_key = pub_key.split("=\n")[:-1]
        public_key = { 'y': public_key[0] + "=\n", 'g': public_key[1] + "=\n", 'p': public_key[2] + "=\n" }

        encrypted = self.encrypt(message, public_key)
        return Utils.encrypted

    def decrypt_full(self, encrypted, pri_key):
        private_key = pri_key.split("=\n")[:-1]
        private_key = { 'x': private_key[0] + "=\n", 'p': private_key[1] + "=\n" }
        
        decrypted = self.decrypt(encrypted, private_key)
        return decrypted


    def decrypt(self, encrypted, private_key):
        x = Utils.b64_to_dec(private_key['x'])
        p = Utils.b64_to_dec(private_key['p'])

        p_key = { 'x': x, 'p': p }
        
        encrypted = encrypted.split('=\n')[:-1]
        encrypted_paired = []
        for i in range(0, len(encrypted), 2):
            a = Utils.b64_to_dec(encrypted[i] + '=\n')
            b = Utils.b64_to_dec(encrypted[i+1] + '=\n')
            encrypted_paired.append({ 'a': a, 'b': b })

        message = ''
        for m in encrypted_paired:
            message += chr(self.elgamal.decrypt(m, p_key))
        return message