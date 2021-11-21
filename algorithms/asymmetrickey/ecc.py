from .utils import Utils

import random
import math

class EllipticPoint:
    def __init__(self, x=0, y=0, inf=False):
        self.x = x if not inf else math.inf
        self.y = y if not inf else math.inf
        self.inf = inf

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def is_infinity(self):
        return self.inf
    
    def mirror(self):
        return EllipticPoint(self.x, -self.y, self.inf)

    def __eq__(self, point):
        if(isinstance(point, EllipticPoint)):
            if(self.inf):
                return self.inf == point.inf
            else:
                return self.x == point.x and self.y == point.y
            
        return False

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)


class EllipticCurve:
    def __init__(self, a, b, p):
        ''' y^2 = x^3 + ax + b '''
        self.a = a
        self.b = b
        self.p = p
        self.points = []
        if(self.is_singular()):
            print("Error: Curve is Singular!.")
    
    def is_singular(self):
        return((((4 * (self.a ** 3)) + (27 * (self.b ** 2))) % self.p) == 0)

    def get_points(self):
        points = [EllipticPoint(inf=True)]
        
        for x in range(self.p):
            y_square = x ** 3 + self.a * x + self.b

            for point in Utils.mod_sqrt(y_square % self.p, self.p):
                points.append(EllipticPoint(x, point))
        self.points = points 
    
    def get_y_square(self, x):
        y_square = x ** 3 + self.a * x + self.b

        for point in Utils.mod_sqrt(y_square % self.p, self.p):
            return(EllipticPoint(x, point))

    def point_addition(self, P, Q):
        if(P == Q):
            return self.point_multiplication(P)
        else:
            xp = P.get_x(); yp = P.get_y();
            xq = Q.get_x(); yq = Q.get_y();

            if(xp == xq):
                return EllipticPoint(inf=True)
            else:
                m = ((yp-yq) * pow((xp-xq), -1, self.p)) % self.p

                xr = (m ** 2 - xp - xq) % self.p
                yr = (m * (xp - xr) - yp) % self.p
                return EllipticPoint(xr, yr)

    def point_substraction(self, P, Q):
        return self.point_addition(P, EllipticPoint(Q.get_x(), -Q.get_y() % self.p))

    def point_multiplication(self, P):
        
        xp = P.get_x(); yp = P.get_y();

        if(yp == 0):
            return EllipticPoint(inf=True)
        else:
            m = ((3 * (xp ** 2) + self.a) * pow((2 * yp), -1, self.p)) % self.p
            xr = (m ** 2 - 2 * xp) % self.p
            yr = (m * (xp - xr) - yp) % self.p
            return EllipticPoint(xr, yr)

    def point_scalar_multiplication(self, P, k):
        if(k == 1):
            return P
        elif(k == 2):
            return self.point_multiplication(P)
        else:
            prev = P
            res = self.point_multiplication(P)
            for i in range(k-2):
                if(res.is_infinity()):
                    res = self.point_addition(prev, self.point_multiplication(P))
                else:
                    prev = res
                    res = self.point_addition(res, P)
    
            return res


class ECCElGamalMachine:
    def __init__(self):
        pass

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
    
    def create_agreement(self, bit):
        p = self.create_random_prime(bit)

        curve_a = random.randint(-10, 10)
        curve_b = random.randint(-200, 200)

        curve = EllipticCurve(curve_a, curve_b, p)
        curve.get_points()

        found = False

        B = None

        while(not found):
            B = curve.points[random.randint(1, len(curve.points) - 2)]
            if(not B.is_infinity()):
                found = True
        k = 2

        return p, curve_a, curve_b, B, k

    def create_key(self, p, curve_a, curve_b, B):

        pri = random.randint(1, p-2)

        curve = EllipticCurve(curve_a, curve_b, p)
        curve.get_points()
       
        public_key = curve.point_scalar_multiplication(B, pri)
        private_key = pri

        return public_key, private_key

    def create_key_full(self, bit):
        p, curve_a, curve_b, B, k = self.create_agreement(bit)
        public_key, private_key = self.create_key(p, curve_a, curve_b, B)

        public_key = str(public_key.x) + "," + str(public_key.y)
        B = str(B.x) + "," + str(B.y)

        pub_key = public_key + " " + str(p) + " " + str(curve_a) + " " + str(curve_b) + " " + B + " " + str(k)
        pri_key = str(private_key) + " " + str(p) + " " + str(curve_a) + " " + str(curve_b) + " " + str(k)
        
        pub_key = Utils.string_to_b64(pub_key)
        pri_key = Utils.string_to_b64(pri_key)
        
        return pub_key, pri_key

    def encrypt_full(self, message, pub_key):
        pub_key = Utils.b64_to_string(pub_key)
        pub_key = pub_key.split(" ")

        public_key  = pub_key[0].split(",")
        public_key  = EllipticPoint(int(public_key[0]), int(public_key[1]))
        p           = int(pub_key[1])
        curve_a     = int(pub_key[2])
        curve_b     = int(pub_key[3])
        B           = pub_key[4].split(",")
        B           = EllipticPoint(int(B[0]), int(B[1]))
        k           = int(pub_key[5])

        encrypted = self.encrypt(message, public_key, p, curve_a, curve_b, B, k)

        encrypted_text = ""

        for i in range(len(encrypted)):
            e = encrypted[i]
            encrypted_text += str(e['kB'].x) + "," + str(e['kB'].y) + "," + str(e['PmkPb'].x) + "," + str(e['PmkPb'].y)
            if(i != len(encrypted)-1):
                encrypted_text += "\n"

        return encrypted_text

    def decrypt_full(self, encrypted_text, pri_key):
        
        encrypted = []
        encrypted_text = encrypted_text.split("\n")
        for i in range(len(encrypted_text)):
            e = encrypted_text[i].split(",")
            kB = EllipticPoint(int(e[0]), int(e[1]))
            PmkPb = EllipticPoint(int(e[2]), int(e[3]))
            encrypted.append({'kB': kB, 'PmkPb': PmkPb})


        pri_key = Utils.b64_to_string(pri_key)
        pri_key = pri_key.split(" ")

        private_key = int(pri_key[0])
        p           = int(pri_key[1])
        curve_a     = int(pri_key[2])
        curve_b     = int(pri_key[3])
        k           = int(pri_key[4])

        decrypted = self.decrypt(encrypted, private_key, p, curve_a, curve_b, k)

        return decrypted


    def point_available(self, points, x):
        res = None
        for point in points:
            if(point.get_x() == x):
                res = point
                break
        return res

    def encode(self, message, p, curve_a, curve_b, k):

        curve = EllipticCurve(curve_a, curve_b, p)
        curve.get_points()

        encoded = []

        for m in message:
            m = ord(m)
            
            point = curve.points[k*m + 1]

            encoded.append(point)  
        return encoded

    def decode(self, encrypted, p, curve_a, curve_b, k):
        curve = EllipticCurve(curve_a, curve_b, p)
        curve.get_points()
        points = curve.points
        decoded = ""

        for e in encrypted:
            for i in range(len(points)):
                if(points[i].get_x() == e.get_x()):
                    break
            decoded += chr(math.floor((i - 1) / k))
        return decoded

    def encrypt(self, message, public_key, p, curve_a, curve_b, B, k):
        curve = EllipticCurve(curve_a, curve_b, p)
        curve.get_points()

        encoded = self.encode(message, p, curve_a, curve_b, k)

        print("ENCODED")
        for e in encoded:
            print(e)
        print()

        encrypted = []

        for encode in encoded:
            found = False
            while(not found):
                random_k = random.randint(1, p-1)
                kB = curve.point_scalar_multiplication(B, random_k)
                PmkPb = curve.point_addition(encode, curve.point_scalar_multiplication(public_key, random_k))
                if(not kB.is_infinity() and not PmkPb.is_infinity()):
                    found = True
            
            encrypted.append({ 'kB': kB, 'PmkPb': PmkPb })
            print("kB\t\t:" + str(kB))
            print("PmkPb\t:" + str(PmkPb))

        return encrypted

    def decrypt(self, encrypted, private_key, p, curve_a, curve_b, k):
        curve = EllipticCurve(curve_a, curve_b, p)
        curve.get_points()

        decrypted = []

        for e in encrypted:
            # print("PmkPb\t: " + str(e['PmkPb']))
            # print("Mul\t: " + str(curve.point_scalar_multiplication(e['kB'], private_key)))
            decrypted.append(curve.point_substraction(e['PmkPb'], curve.point_scalar_multiplication(e['kB'], private_key)))

        print("DECRYPTED")
        for e in decrypted:
            print(e)
        decoded = self.decode(decrypted, p, curve_a, curve_b, k)

        print()
        return decoded