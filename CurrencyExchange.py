import requests
import json
import locale
#Aplikasi Konversi mata uang
print("""
     =============== APLIKASI KONVERSI MATA UANG ===========
     = Author : Febri C                                    =
     = Lisensi : GPL                                       =
     = version : 1.1                                       =
     = Cara Penggunaan                                     =
     = Tinggal tulis uang yang mau dikonversi              =
     = Baru ada konversi dari rupiah (IDR) ke dollar (USD) =
     = referensi mata uang : https://www.ecb.europa.eu/    =
     = referensi github : https://github.com/hakanensari   =
     =======================================================
""")

url = f"https://api.frankfurter.app/latest?from=USD&to=IDR" #alamat dari API

response = requests.get(url) #mendapatkan data dari url

if response.status_code != 200:
    print("server sedang error")
    pass

else:
    USD_IDR = response.json().get("rates") #parsing data
    uang = float(input("Jumlah Uang (Rp) : ")) # jumlah uang yang dimasukkan
    sisa_uang = uang%float(USD_IDR["IDR"]) # jumlah uang yang akan dikonversi The data refreshes around 16:00 CET menjadi sen
    uang_dolar = uang//float(USD_IDR["IDR"]) # jumlah uang konversi ke dollar
    uang_sen = (sisa_uang/float(USD_IDR["IDR"])*100) # jumlah uang konversi ke sen
    #fungsi untuk menampilkan hasil
    print(f"Nilai mata uang saat ini : $1 USD = Rp {USD_IDR["IDR"]:,.2f}")
    print(f"Data nilai mata uang di perbaharui setiap pukul 16.00 CET pada hari kerja.")
    print(f"Nilai uang anda setelah konversi adalah ${uang_dolar:,.0f} dollar, {uang_sen:.0f} sen")

# DEBUG: print(response.status_code)
