import random
import math

rb_x = -1       # batas bawah x
ra_x = 2        # batas atas x
rb_y = -1       # batas bawah y
ra_y = 1        # batas atas y

class Kromosom:                     #Class untuk menampung kromosom
    def __init__(self, biner = None):
        if biner == None:
            self.biner = random.choices([0, 1], k=10)
        else:
            self.biner = biner
        self.x = self.Representasi(ra_x, rb_x, self.biner[:5])
        self.y = self.Representasi(ra_y, rb_y, self.biner[5:])

    def __repr__(self):         #printable representation dari class kromosom
        return '{} ({}, {}) - {}'.format(self.biner, self.x, self.y, heuristic(self.x, self.y))

    def Representasi(self, ra, rb, g):          #fungsi representasi biner
        tp = [2**-i for i in range(1, len(g) + 1)]
        return rb + ((ra - rb) / sum(tp) * sum([g[i] * tp[i] for i in range(len(g))]))  #rumus representasi biner

def heuristic(x, y):                   #rumus nilai heuristic
    return (math.cos(x*x) * math.sin(y*y)) + (x + y)

def fitness(x, y):          #fungsi fitness: maksimum f = h
    return heuristic(x, y)

def exist(l, c):        #check jika kromosom ada di populasi dan digunakan juga
    found = False       #untuk seleksi orang tua
    for i in l:
        if i.biner == c.biner:
            found = True
            break
    return found

def seleksi_orangtua(k):    # fungsi seleksi orangtua mereturn orangtua dari Roulette wheel
    orangtua = []           # list atau array orangtua
    list_fitness = list(map(lambda c: fitness(c.x, c.y), populasi))  # memakai fungsi lambda sebagai anonymous function
    list_weight = [list_fitness[i] / sum(list_fitness) for i in range(len(populasi))]  # list atau array untuk menampung weight dari semua kromosom yang ada di populasi
    while len(orangtua) != k:
        kandidat = random.choices(populasi, weights=list_weight)[0]  # parameter weight akan memberi berat kemungkinan pada setiap nilai
        if not exist(orangtua, kandidat):                           # sehingga setiap item untuk dipilih ditentukan oleh bobot relatifnya.
            orangtua.append(kandidat)
    return orangtua

def Crossover(ortu1, ortu2):        # fungsi untuk crossover menghasilkan anak
    posisi = random.randint(1, len(ortu1.biner) - 2)    # mengambil titik potong dari indeks kedua paling awal atau indek kedua paling akhir

    biner_anak1 = ortu1.biner[:posisi] + ortu2.biner[posisi:]
    biner_anak2 = ortu2.biner[:posisi] + ortu1.biner[posisi:]

    #Mutasi anak1
    prob_mutasi = random.uniform(0, 100)    # pick angka random dari 0 sampai 100 prob_mutasi dalam persen
    if prob_mutasi < 0.5:                   #0.5% mutasi
        index_mutasi = random.randint(0, len(biner_anak1) - 1)
        if biner_anak1[index_mutasi] == 1:
            biner_anak1[index_mutasi] = 0
        else:
            biner_anak1[index_mutasi] = 1

    #mutasi anak2
    prob_mutasi = random.uniform(0, 100)    # pick angka random dari 0 sampai 100 prob_mutasi dalam persen
    if prob_mutasi < 0.5:                   #0.5% mutasi
        index_mutasi = random.randint(0, len(biner_anak2) - 1)
        if biner_anak2[index_mutasi] == 1:
            biner_anak2[index_mutasi] = 0
        else:
            biner_anak2[index_mutasi] = 1

    populasi.append(Kromosom(biner_anak1))    # memasukan hasil crossover dan mutasi
    populasi.append(Kromosom(biner_anak2))    # ke populasi

def seleksi_survivor():     #fungsi seleksi survivor agar populasi terus sama
    populasi.sort(key=lambda c: heuristic(c.x, c.y), reverse=True)  # memakai fungsi key dan fungsi lambda sebagai anonymous function di dalam fungsi sort descending

    while len(populasi) != 46:  # kontrol jumlah populasi agar tetap 46
        populasi.pop()          # membuang kromosom yang paling buruk di populasi

# fungsi main
populasi = []
generasi = 1
while len(populasi) != 46:
    c = Kromosom()

    if not exist(populasi, c):
        populasi.append(c)

seleksi_survivor()
print('Generasi', generasi)
print('Best', populasi[0])

arr_fit = [0]*120
arr_fit[generasi-1] = fitness(populasi[0].x, populasi[0].y)

while generasi < 120:
    orangtua = seleksi_orangtua(2)
    Crossover(orangtua[0], orangtua[1])
    seleksi_survivor()

    generasi += 1

    arr_fit[generasi-1] = fitness(populasi[0].x, populasi[0].y)
    print('Generasi', generasi)
    print('Best', populasi[0])  # output kromosom terbaik dari populasi generasi 'generasi'

# untuk menunjukkan grafik pertumbuhan nilai fitness kromosom terbaik setiap generasi
import matplotlib.pyplot as plt

# lihat pertumbuhan nilai fitness kromosom terbaik
plt.plot(range(1, generasi + 1), arr_fit)
plt.title("Pertumbuhan Nilai Fitness")
plt.xlabel("Generasi")
plt.ylabel("Fitness Terbaik")
plt.show()