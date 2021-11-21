from re import M
from .utils import Utils
from random import randrange

import math


class Paillier:
    def _lcm(self, a, b):
        return abs(a * b) // math.gcd(a, b)

    def _L(self, x, n):
        return (x - 1) // n

    def generate_keys(self, keys):
        p, q = map(int, keys.split())
        print(p,q)

        # TODO check gcd(pq, (p-1)(q-1)) = 1
        n = p * q
        lamb = self._lcm(p - 1, q - 1)
        g = randrange(n * n)
        mu = pow(self._L(pow(g, lamb, n * n), n), -1, n)

        # private key = (lamb, mu)
        # public key = (g, n)
        return g, n, lamb, mu

    def _encrypt(self, m, keys, r=0):
        g, n = map(int, keys.split())
        while math.gcd(r, n) != 1:
            r = randrange(n)

        return (pow(g, int(m)) * pow(r, n)) % (n * n)

    def _decrypt(self, c, keys):
        n, lamb, mu = map(int, keys.split())
        return int((self._L(pow(int(c), lamb, n * n), n) * mu) % n)

    def execute(self, command, text, keys, r):
        if (command == "encrypt"):
            return self._encrypt(text, keys, r)
        else:
            return self._decrypt(text, keys)
