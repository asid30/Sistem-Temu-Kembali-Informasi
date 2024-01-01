import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

def search():
  df = pd.read_excel(r'D:\TEST Codingan\Sistem-Temu-Kembali-Informasi\Riset Jupiter Notebook\Data\df_final.xlsx').head(1000)
  df = df.drop(columns='Unnamed: 0')

  dicari = 'intro Bunga Krisan sebgai komoditi'
  # dicari = input('Masukan Pencarian: ')

  df_temu = []
  similaritas = []

  # Inisialisasi TF-IDF Vectorizer
  tfidf_vectorizer = TfidfVectorizer()

  for i in tqdm(range(len(df['text_stemmed']))):
    temp = df['text_stemmed'].iloc[i]

    # Transformasi teks menjadi vektor TF-IDF
    tfidf_matrix = tfidf_vectorizer.fit_transform([dicari, temp])

    # Hitung similaritas kosinus antara kedua teks
    cosine_similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    if cosine_similarities[0][0] > 0.1:
      df_temu.append(df.iloc[i])
      similaritas.append(cosine_similarities)

  df_temu = pd.DataFrame(df_temu)
  df_temu['similaritas'] = similaritas

  return df_temu[['title', 'similaritas','abstract']]

print(search())