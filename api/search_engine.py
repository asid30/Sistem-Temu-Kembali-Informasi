import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import RegexpTokenizer
from tqdm import tqdm

def search(teks):
  df = pd.read_excel(r'D:\TEST Codingan\Sistem-Temu-Kembali-Informasi\Riset Jupiter Notebook\Data\df_final.xlsx').head(1000)
  df = df.drop(columns='Unnamed: 0')

  teks = stem(teks)

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
      similaritas.append(cosine_similarities)

  df_temu = pd.DataFrame(df_temu)
  df_temu['similaritas'] = similaritas

  return latent_semantic_analysis(df_temu)

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

def latent_semantic_analysis(dataset):
  tokenizer = RegexpTokenizer(r'\w+')
  topik = []

  for index in range(len(dataset)):
    # Ambil dataset
    teks = dataset['fulltext_stopword'].iloc[index]
    data = tokenizer.tokenize(teks)

    # Proses vektorisasi teks dengan TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(data)

    # Terapkan LSA dengan TruncatedSVD
    num_topics = 4  # Jumlah topik yang ingin diidentifikasi
    lsa_model = TruncatedSVD(n_components=num_topics, random_state=42)
    lsa_topic_matrix = lsa_model.fit_transform(tfidf_matrix)

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

  # return dataset.to_dict()
  return dataset.iloc[0].to_dict()
    
dicari = 'intro kembang KRISAN POTONG DI DESA pesawaran'
# dicari = input('Masukan Pencarian: ')

# dataset = search(dicari)
dataset = search(dicari)
judul = dataset['title']
print(judul)