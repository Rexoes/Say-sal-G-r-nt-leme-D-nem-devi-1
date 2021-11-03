# Ahmet Utku ELIK
# 5518123001
# Sayısal Görüntü Işleme Dersi Dönem Odevi-1
# Ders Hocası : Dr.Öğr.Uyesi KALI GURKAHRAMAN

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

#Görüntünün Çözünürlük Değeri M x N
M = 512
N = 512

#Görüntü sayısallaştırılırken kullanılan bit sayısı 8 ise
maxTone = 255 #np.power(2,8) - 1

#Lütfen transfer fonksiyonu tanımlamak için (r,s) değerlerini giriniz!
r1 = 150.0
s1 = 100.0
r2 = 230.0
s2 = 200.0

# 2 adet nokta girildiği için max 3 min 2 (Kare Dalga) fonksiyon oluşacaktır!

def function1(r):   # F1(x) = mx + c
    m = s1 / r1
    c = s1 - m * r1 # (r1,s1) sağlayan c değeri
    return int(m * r + c)

def function2(r):   # F2(x) = mx + c
    m = (s2 - s1) / (r2 - r1)
    c = s2 - m * r2 # (r2,s2) sağlayan c değeri
    return int(m * r + c)

def function3(r):   # F3(x) = mx + c
    m = (maxTone - s2) / (maxTone - r2)
    c = maxTone - m * maxTone # (255,255) sağlayan c değeri
    return int(m * r + c)

def transverFunctionCalculate(array): #Gri tonlar indis'e karşılık gelmekte
    for i in range(256):
        if(i < r1): # Birinci Fonksiyon
            value = function1(i)
            array[i] = value
        elif(i < r2):
            value = function2(i)
            array[i] = value
        else:
            value = function3(i)
            array[i] = value
    return array

def outputImageCalculate(Iin, Iout, transverFunction):
    for r in range(M):
        for c in range(N):
            valueOfGrayTone = Iin[r,c]
            valueOfTransverFunction = transverFunction[valueOfGrayTone]
            Iout[r,c] = valueOfTransverFunction
    return Iout

Irgb = Image.open('lenna.png') #İşlenecek resim okunuyor
Igray = Irgb.convert('L')   #Gri formata çevriliyor

Irgb_array = np.array(Irgb) #Matematiksel işlem yapabilmek için
Igray_array = np.array(Igray) #Array formatına dönüştürülüyor

transverFunction = [0 for x in range(maxTone + 1)] #Tüm değerleri 0 olan 256 elemanlı dizi oluşturuluyor
transverFunction = transverFunctionCalculate(transverFunction) # (r,s) değerlerine göre transfer fonksiyonu oluşturuluyor.

Iout = [[0 for x in range(M)] for y in range(N)] #Çıkış görüntüsü için dizi oluşturuluyor
Iout = np.array(Iout)
Iout = outputImageCalculate(Igray_array, Iout, transverFunction) # Transfer fonksiyonuna göre yeni değer atanıyor

Irgb.show() #Resmin orjinal hali
Igray.show() #Resmin gri hali
Iout_imageFormat = Image.fromarray(Iout) #Array -> Image formatına dönüştürülüyor
Iout_imageFormat.show() # Ve resmin transfer fonksiyonuna göre işlenmiş hali bastırılıyor

#Input ve Output Görüntünün Histogram Eğrileri Çizdiriliyor Plots sekmesinden görüntülenebilmektedir.

histogram, bin_edges = np.histogram(Igray, bins=256, range=(0,255))
plt.figure()
plt.title("Input Grayscale Histogram")
plt.xlabel("grayscale value")
plt.ylabel("pixels")
plt.xlim([0,255])
plt.plot(bin_edges[0:-1], histogram)
plt.show()

histogram, bin_edges = np.histogram(Iout_imageFormat, bins=256, range=(0,255))
plt.figure()
plt.title("Output Grayscale Histogram")
plt.xlabel("grayscale value")
plt.ylabel("pixels")
plt.xlim([0,255])
plt.plot(bin_edges[0:-1], histogram)
plt.show()
