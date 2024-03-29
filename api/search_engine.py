import pandas as pd
import numpy as np
import re
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm

def search(teks: str, fakultas: str = "ALL", pilihan: int = 0):
  df_utama = pd.read_excel(r'D:\Project KP\Sistem-Temu-Kembali-Informasi\Riset Jupiter Notebook\Data\df_final.xlsx').head(2000)
  df_utama = df_utama.drop(columns = ['Unnamed: 0'])
  if fakultas.upper() == 'FKIP' or fakultas == 'FMIPA' or fakultas == 'FEB' or fakultas == 'FH' or fakultas == 'FT' or fakultas == 'FISIP' or fakultas == 'FK':
    df = filter_by_divisions(df_utama, fakultas)
  else:
    df = df_utama

  teks = stem(remove_stopwords(teks))

  df_temu = []
  similaritas = []

  # Inisialisasi TF-IDF Vectorizer
  tfidf_vectorizer = TfidfVectorizer()

  for i in tqdm(range(len(df['text_stemmed']))):
    temp = df['text_stemmed'].iloc[i]

    # Transformasi teks menjadi vektor TF-IDF
    tfidf_matrix = tfidf_vectorizer.fit_transform([teks, temp])

    # Hitung similaritas kosinus antara kedua teks
    cosine_similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    if cosine_similarities[0][0] > 0.1:
      df_temu.append(df.iloc[i])
      similaritas.append(float(cosine_similarities))

  df_temu = pd.DataFrame(df_temu)
  df_temu['similaritas'] = similaritas
  return tentukan_topik(df_temu.sort_values(by=['similaritas'], ascending=False), pilihan)

def remove_stopwords(text):
  factory = StopWordRemoverFactory()
  stopwords = factory.get_stop_words()

  result = []
  for x in  text.split():
      if x not in stopwords:
          result.append(x)

  hasil_stopword = " ".join(result)

  return hasil_stopword

def stem(text):
  factory2 = StemmerFactory()
  stemmer = factory2.create_stemmer()
  return stemmer.stem(text)

def hapus_nan(dataset):
  dataset.fillna("", inplace=True) 
  return dataset

def filter_by_divisions(dataset, fakultas):
  new_divisions = []
  for i in range(len(dataset['divisions'])):
    try:
      new_divisions.append(ast.literal_eval(dataset['divisions'].iloc[i]))
    except:
      new_divisions.append(ast.literal_eval('[]'))
  dataset['new_divisions'] = new_divisions
  
  new_fakultas = []
  for i in range(len(dataset)):
    temp = dataset['new_divisions'].iloc[i]
    temp2 = []
    for j in range(len(temp)):
      temp2.append(pisahkan_kata(temp[j]))
    new_fakultas.append(temp2)
  dataset['fakultas'] = new_fakultas
  
  df_hasil = []
  for i in range(len(dataset)):  
    if fakultas in dataset['fakultas'].iloc[i]:
      df_hasil.append(dataset.iloc[i])
  df_hasil = pd.DataFrame(df_hasil)
  
  return df_hasil

def pisahkan_kata(kata):
    hasil = re.sub(r'\d', '', kata)
    return hasil

def tentukan_topik(dataset, pilihan:int = 0):
  tokenizer = RegexpTokenizer(r'\w+')
  topik = []

  for index in range(len(dataset)):
    # Ambil dataset
    teks = dataset['fulltext_stopword'].iloc[index]
    data = tokenizer.tokenize(teks)

    # Proses vektorisasi teks dengan TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(data)
    jumlah_feature = tfidf_matrix.shape

    # Terapkan LSA dengan TruncatedSVD
    if jumlah_feature[1] < 5:
      num_topics = jumlah_feature[1] # Jumlah topik yang ingin diidentifikasi
    else:
      num_topics = 5 # Jumlah topik yang ingin diidentifikasi
    lsa_model = TruncatedSVD(n_components=num_topics, random_state=42)
    lsa_model.fit_transform(tfidf_matrix)

    # Ambil kata-kata kunci untuk setiap topik
    terms = tfidf_vectorizer.get_feature_names_out()
    top_keywords = 1  # Jumlah kata kunci untuk setiap topik (HANYA BISA DIAMBIL 1)

    kata_kunci = []

    for i, topic in enumerate(lsa_model.components_):
        top_keywords_idx = topic.argsort()[-top_keywords:][::-1]
        keywords = [terms[key_idx] for key_idx in top_keywords_idx]
        kata_kunci.append(keywords[0])

    topik.append(kata_kunci)
  dataset['topik'] = topik
  dataset = dataset.drop(columns=[
     'text_stemmed',
     'fulltext_stopword', 
     'fulltext', 
     'language_accuracy', 
     'language', 
     'text_raw',
     'abstract', 
    #  'date',
    #  'keywords',
    #  'similaritas',
    #  'new_abstract',
    #  'publisher',
    #  'publication',
    #  'divisions'
    ])
  
  dataset = hapus_nan(dataset) #hapus nilai nan
  if pilihan == 0:
    return convert_dataframe_to_list(dataset)
  elif pilihan == 1:
    return dataset
  elif pilihan == 2:
    return convert_dataframe_to_dict(dataset)

def convert_dataframe_to_list(dataset):
  dataset = dataset.T
  hasil_pencarian = []
  for i in dataset.columns.values.tolist():
    hasil_pencarian.append(dataset[i].to_list())
  return hasil_pencarian

def convert_dataframe_to_dict(dataset):
  dataset = dataset.T
  hasil_pencarian = dataset.to_dict()
  return hasil_pencarian