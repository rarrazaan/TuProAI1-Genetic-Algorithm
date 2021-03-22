import random
import math

def h(x, y):                   #rumus nilai heuristic
    return (math.cos(x*x) * math.sin(y*y)) + (x + y)

rb_x = -1       # batas bawah x
ra_x = 2        # batas atas x
rb_y = -1       # batas bawah y
ra_y = 1        # batas atas y

class Kromosom:                     #Class untuk menampung kromosom
    def __init__(self, bit = None):
        if bit == None:
            self.bit = random.choices([0, 1], k=8)
        else:
            self.bit = bit
        self.x1 = self.rekombinasi(ra_x, rb_x, self.bit[:4])
        self.x2 = self.rekombinasi(ra_y, rb_y, self.bit[4:])

    def __repr__(self):
        return '{} ({}, {}) - {}'.format(self.bit, self.x1, self.x2, h(self.x1, self.x2))

    def rekombinasi(self, ra, rb, g):
        tp = [2**-i for i in range(1, len(g) + 1)]
        return rb + ((ra - rb) / sum(tp) * sum([g[i] * tp[i] for i in range(len(g))]))

def f(x1, x2):          #fungsi fitness: maksimum f = h
    hasil = h(x1, x2)
    return hasil

def exist(l, c):        #check jika kromosom ada di populasi dan digunakan juga
    found = False       #untuk seleksi orang tua
    for i in l:
        if i.bit == c.bit:
            found = True
            break
    return found

def seleksi_orangtua(k):    # fungsi seleksi orangtua mereturn orangtua dari
    orangtua = []           # populasi
    arr_fitness = list(map(lambda c: f(c.x1, c.x2), populasi))
    arr_weight = [arr_fitness[i] / sum(arr_fitness) for i in range(len(populasi))]
    while len(orangtua) != k:
        kandidat = random.choices(populasi, weights=arr_weight)[0]
        if not exist(orangtua, kandidat):
            orangtua.append(kandidat)
    return orangtua


def Crossover(ortu1, ortu2):        # fungsi untuk crossover menghasilkan anak
    posisi = random.randint(1, len(ortu1.bit) - 2)

    bit_anak1 = ortu1.bit[:posisi] + ortu2.bit[posisi:]
    bit_anak2 = ortu2.bit[:posisi] + ortu1.bit[posisi:]


    rng_mutasi = random.uniform(0, 100)
    if rng_mutasi > (100 - 0.5): #0.5% mutasi
        posisi_mutasi = random.randint(0, len(bit_anak1) - 1)
        if bit_anak1[posisi_mutasi] == 1:
            bit_anak1[posisi_mutasi] = 0
        else:
            bit_anak1[posisi_mutasi] = 1

    rng_mutasi = random.uniform(0, 100)
    if rng_mutasi > (100 - 0.5): #0.5% mutasi
        posisi_mutasi = random.randint(0, len(bit_anak2) - 1)
        if bit_anak2[posisi_mutasi] == 1:
            bit_anak2[posisi_mutasi] = 0
        else:
            bit_anak2[posisi_mutasi] = 1


    populasi.append(Kromosom(bit_anak1))    # memasukan hasil crossover dan mutasi
    populasi.append(Kromosom(bit_anak2))    # ke populasi


def seleksi_survivor():     #fungsi seleksi survivo agar populasi terus sama
    populasi.sort(key=lambda c: h(c.x1, c.x2), reverse=True)

    while len(populasi) != 50:
        populasi.pop()

# fungsi main
populasi = []
generasi = 1
while len(populasi) != 50:
    c = Kromosom()

    if not exist(populasi, c):
        populasi.append(c)

seleksi_survivor()
print('Generasi', generasi)
print('fittest', populasi[0])

arr_fit = []
while generasi < 48:
    orangtua = seleksi_orangtua(2)
    Crossover(orangtua[0], orangtua[1])
    seleksi_survivor()

    generasi += 1
    print('Generasi', generasi)
    print('fittest', populasi[0])