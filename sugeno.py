#Nama   : Windi Risma Wati
#NIM    : 191011401795
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : produksi baju

#Kecepatan Putaran Mesin : min 500 rpm dan max 1200 rpm.
#Banyaknya Baju  : sedikit 40 dan banyak 80.
#Tingkat Penjualan  : rendah 40, sedang 50, dan 60 tinggi.

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Baju():
    minimum = 40
    maximum = 80

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)

class Kwitansi():
    minimum = 40
    medium = 50
    maximum = 60

    def rendah(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def tinggi(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)

class Putaran():
    minimum = 500
    maximum = 1200
    
    def lambat(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def cepat(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    # 2 permintaan 3 persediaan
    def inferensi(self, jumlah_baju, jumlah_kwitansi):
        pak = Baju()
        ktr = Kwitansi()
        result = []
        
        # [R1] Jika Baju SEDIKIT, dan Kwitansi RENDAH, 
        #     MAKA Putaran = 500
        α1 = min(pak.sedikit(jumlah_baju), ktr.rendah(jumlah_kwitansi))
        z1 = self.minimum
        result.append((α1, z1))

        # [R2] Jika Baju SEDIKIT, dan Kwitansi SEDANG, 
        #     MAKA Putaran = 10 * jumlah_kwitansi + 100
        α2 = min(pak.sedikit(jumlah_baju), ktr.sedang(jumlah_kwitansi))
        z2 = 10 * jumlah_kwitansi + 100
        result.append((α2, z2))

        # [R3] Jika Baju SEDIKIT, dan Kwitansi TINGGI, 
        #     MAKA Putaran = 10 * jumlah_kwitansi + 200
        α3 = min(pak.sedikit(jumlah_baju), ktr.tinggi(jumlah_kwitansi))
        z3 = 10 * jumlah_kwitansi + 200
        result.append((α3, z3))

        # [R4] Jika Baju BANYAK, dan Kwitansi RENDAH,
        #     MAKA Putaran = 5 * jumlah_baju + 2 * jumlah_kwitansi
        α4 = min(pak.banyak(jumlah_baju), ktr.rendah(jumlah_kwitansi))
        z4 = 5 * jumlah_baju + 2 * jumlah_kwitansi
        result.append((α4, z4))

        # [R5] Jika Baju BANYAK, dan Kwitansi SEDANG,
        #     MAKA Putaran = 5 * jumlah_baju + 4 * jumlah_kwitansi + 100
        α5 = min(pak.banyak(jumlah_baju), ktr.sedang(jumlah_kwitansi))
        z5 = 5 * jumlah_baju+ 4 * jumlah_kwitansi + 100
        result.append((α5, z5))

        # [R6] Jika Baju BANYAK, dan Kwitansi TINGGI,
        #     MAKA Putaran = 5 * jumlah_baju + 5 * jumlah_kwitansi + 300
        α6 = min(pak.banyak(jumlah_baju), ktr.tinggi(jumlah_kwitansi))
        z6 = 5 * jumlah_baju + 5 * jumlah_kwitansi + 300
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_baju, jumlah_kwitansi):
        inferensi_values = self.inferensi(jumlah_baju, jumlah_kwitansi)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])