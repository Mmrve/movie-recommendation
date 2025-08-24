import psycopg2
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")  # varsayılan localhost
DB_PORT = os.getenv("DB_PORT", "5432")       # varsayılan 5432

# Postgres bağlantısı
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASS,
    host=DB_HOST, port=DB_PORT
)
cur = conn.cursor()

# CSV verisini yükle
df = pd.read_csv("movies.csv")
df = df.dropna(subset=["soup"])

# Yeni model (768 boyut)
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

for _, row in tqdm(df.iterrows(), total=len(df)):
    title = row["original_title"]
    soup = row["soup"]
    
    # embedding hesapla
    emb = model.encode(soup)
    emb_str = "[" + ",".join(map(str, emb)) + "]"  # pgvector format
    
    cur.execute(
        "INSERT INTO movies (original_title, soup, embedding) VALUES (%s, %s, %s)",
        (title, soup, emb_str)
    )

conn.commit()
cur.close()
conn.close()

print("✅ Yükleme tamamlandı!")

