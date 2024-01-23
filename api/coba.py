import search_engine

try:
    # kueri = input('Masukan Teks: ')
    kueri = 'Media Pembelajaran Digital'
    hasil_pencarian = search_engine.search(kueri, "FKIP" ,1)
    print(hasil_pencarian)
except:
    hasil_pencarian = 'Anda tidak memberikan kueri atau hasil pencarian tidak ditemukan!'
    print(hasil_pencarian)

    

