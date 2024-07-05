import requests #Library dibutuhkan untuk API
import json     #Library dibutuhkan untuk API
import datetime #Library dibutuhkan untuk waktu
import pandas   #Library dibutuhkan untuk database
import locale   #Library dibutuhkan untuk waktu

#setting waktu lokal
locale.setlocale(locale.LC_TIME, 'id_ID.utf8')
#Fungsi untuk membaca data base agar dapat digunakan secara offline

def Fungsi_Membaca_Database()->tuple[str,str]:
    """
    Pastikan data base disimpan pada folder yang sama dengan kode utama.
    Fungsi ini akan mengembalikan type data tuple. Tuple[0] adalah waktu
    dan Tuple[1] adalah nilai dari Rupiah
    """
    #Fungsi untuk membaca databaes
    dataframe:pandas.core.frame.DataFrame = pandas.read_csv("data_base.txt",sep=",")
    baris_terakhir:int = dataframe.tail(1).index.item() # agar mendapat indeks paling baru
    #mengambil indeks paling baru, pada kolom rupiah
    data_base_paling_baru:numpy.int64 = dataframe.at[baris_terakhir,"rupiah"]
    #mengambil indeks paling baru, pada kolom time
    waktu_paling_baru:str = dataframe.at[baris_terakhir,"time"]
    return waktu_paling_baru , data_base_paling_baru #kembalian

def Fungsi_MengambildataInternet()-> [requests.models.Response, str]:
    """
    Fungsi akan mengembalikan requests.models.Response jika terkoneksi internet
    dan akan mengemalikan string jika tidak terkoneksi internet
    """
    try :
        url:str = f"https://api.frankfurter.app/latest?from=USD&to=IDR" #alamat dari API
        response:requests.models.Response = requests.get(url) #mendapatkan data dari url
        return response
    except requests.exceptions.ConnectionError: #ketika terjadi error
        response:str = "Not Connected"
        return response

def Fungsi_ParsingdataInternet() -> [str, dict]:
    """
    Fungsi untuk parsing data dari internet dengan memanggil library json
    yang akan mengembalikan fungsi berupa dict. status_code yang digunakan adalah 200
    yang berarti mendapatkan respond dari url yang dipanggil. Menggunakan fungsi try/except
    karena sewaktu-waktu koneksi dapat terputus.
    """
    response:requests.models.Response = Fungsi_MengambildataInternet()
    try :
        if response.status_code != 200:
            return "Error"
        else:
            #fungsi untuk menampilkan hasil
            USD_IDR:dict = response.json().get("rates") #parsing data
            return USD_IDR
    except :
        return "Response ConnectionError"

def Fungsi_Update_database(DataBaru:dict)-> None:
    """
    Fungsi untuk menulis ke data_base.txt, menerima parameter input
    berupa dictionary dari fungsi sebelumnya.
    """
    now:datetime.datetime = datetime.datetime.now() #fungsi untuk mendapatkan waktu dari komputer
    
    if isinstance(DataBaru,dict):
        with open("data_base.txt", "a") as file:
            file.write(f"{now},1,{DataBaru["IDR"]}\n")  #fungsi untuk menulis pada database
            file.close()    #menutup database
    else :
        print(DataBaru) #print Error ketika DataBaru bukan berupa dict

def Fungsi_Konversi(Nilai_konversi:[dict,str], uang:float) -> tuple[int,int]:
    """
    Fungsi untuk konversi nilai mata uang 1 dollar = 100 sen.
    '//' digunakan agar pembagiannya bernilai bulat
    '%' digunakan agar mengetahui sisa uang

    kembalian berupa tuple yang berisi interger, tuple[0] uang dollar
    tuple[1] uang sen
    """
    try:
        if isinstance(Nilai_konversi,dict):
            sisa_uang = uang%float(Nilai_konversi["IDR"]) # jumlah uang yang akan dikonversi menjadi sen
            uang_dolar = uang//float(Nilai_konversi["IDR"]) # jumlah uang konversi ke dollar
            uang_sen = (sisa_uang/float(Nilai_konversi["IDR"])*100) # jumlah uang konversi ke sen
            return uang_dolar, uang_sen
        else:
            sisa_uang = uang%float(Nilai_konversi) # jumlah uang yang akan dikonversi The data refreshes around 16:00 CET menjadi sen
            uang_dolar = uang//float(Nilai_konversi) # jumlah uang konversi ke dollar
            uang_sen = (sisa_uang/float(Nilai_konversi)*100) # jumlah uang konversi ke sen
            return uang_dolar, uang_sen
    except:
        pass

def sambutan() -> None:
    print("""
         =============== APLIKASI KONVERSI MATA UANG ===========
         = Author : Febri C                                    =
         = Lisensi : GPL                                       =
         = version : 1.2                                       =
         = Cara Penggunaan                                     =
         = Tinggal tulis uang yang mau dikonversi              =
         = Baru ada konversi dari rupiah (IDR) ke dollar (USD) =
         = referensi mata uang : https://www.ecb.europa.eu/    =
         = referensi github : https://github.com/hakanensari   =
         =======================================================
    """)
def menampilkan_data(Data:[tuple,dict], waktu:str,uang_konversi:tuple[int,int]) -> None :
    if isinstance(Data,dict):
        print(f"Data diambil pada {waktu}.Nilai mata uang saat ini : $1 USD = Rp {Data["IDR"]:,.2f}")
        print(f"Data nilai mata uang di perbaharui setiap pukul 16.00 CET pada hari kerja.")
        print(f"Nilai uang anda setelah konversi adalah ${uang_konversi[0]:,.0f} dollar, {uang_konversi[1]:.0f} sen")
    else :
        print(f"Data diambil pada {waktu}.Nilai mata uang waktu itu : $1 USD = Rp {Data[1]:,.2f}")
        print(f"Data nilai mata uang di perbaharui setiap pukul 16.00 CET pada hari kerja.")
        print(f"Nilai uang anda setelah konversi adalah ${uang_konversi[0]:,.0f} dollar, {uang_konversi[1]:.0f} sen")

def main() -> None :
    '''
    Fungsi utama yang menjalankan seluruh program
    '''
    sambutan() #panggil fungsi sambutan
    uang:float = float(input("Jumlah Uang (Rp) : "))    # jumlah id_IDuang yang dimasukkan
    now:datetime.datetime = datetime.datetime.now()     # mencetak waktu

    if isinstance(Fungsi_MengambildataInternet(),requests.models.Response):
        waktu:str = now.strftime("%A,%d %B %Y %H:%M:%S")                #format waktu
        DataBaru:dict = Fungsi_ParsingdataInternet()
        uang_konversi:tuple[int,int] = Fungsi_Konversi(DataBaru,uang)
        menampilkan_data(DataBaru, waktu,uang_konversi)
        Fungsi_Update_database(DataBaru)

    else :
        DataLama:tuple = Fungsi_Membaca_Database()      # mengambil data dari database
        formate_date:str = '%Y-%m-%d %H:%M:%S.%f'       #format waktu
        waktu:str = datetime.datetime.strptime(DataLama[0], formate_date).strftime("%A,%d %B %Y %H:%M:%S")
        uang_konversi:tuple[int,int] = Fungsi_Konversi(DataLama[1],uang)
        menampilkan_data(DataLama, waktu,uang_konversi)


if __name__ == "__main__" :
    main()
