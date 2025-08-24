
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# ----------------------------
# PostgreSQL Config
# ----------------------------


# ----------------------------
# OMDB Config
# ----------------------------

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
if not OMDB_API_KEY:
    raise RuntimeError("OMDB_API_KEY .env içinde tanımlı değil")


# ----------------------------
# FastAPI Setup
# ----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # geliştirme için
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# DB Bağlantısı
# ----------------------------
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# ----------------------------
# OMDB Fonksiyonu
# ----------------------------
def get_movie_details_omdb(title):
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": OMDB_API_KEY,
        "t": title,
        "plot": "short"
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        return None
    data = res.json()
    if data.get("Response") == "False":
        return None
    return {
        "title": data.get("Title"),
        "poster": data.get("Poster") if data.get("Poster") != "N/A" else None,
        "overview": data.get("Plot") if data.get("Plot") != "N/A" else None,
        "rating": float(data.get("imdbRating")) if data.get("imdbRating") != "N/A" else None
    }

# ----------------------------
# Home Endpoint
# ----------------------------
@app.get("/")
def home():
    return {"message": "Film Öneri API'mize hoş geldin 🎬"}

# ----------------------------
# Search Endpoint
# ----------------------------
@app.get("/search")
def search_movies(query: str = Query(..., min_length=1), limit: int = 5):
    cur.execute("""
        SELECT original_title 
        FROM movies
        WHERE original_title ILIKE %s
        LIMIT %s
    """, (f"%{query}%", limit))
    rows = cur.fetchall()
    titles = [r[0] for r in rows]
    return {"results": titles}

# ----------------------------
# Recommend Endpoint
# ----------------------------
@app.get("/recommend")
def recommend(title: str = Query(...), top_n: int = 5, page: int = 1):
    # 1) Sorgulanan filmin embedding'i
    cur.execute("SELECT embedding FROM movies WHERE original_title ILIKE %s LIMIT 1", (title,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"'{title}' adlı film bulunamadı.")
    target_emb = row[0]

    # 2) PGVector ile benzerlik sorgusu
    cur.execute('''
        SELECT original_title, 1 - (embedding <=> %s) AS similarity
        FROM movies
        WHERE embedding IS NOT NULL
          AND original_title <> %s
        ORDER BY embedding <=> %s
        OFFSET %s LIMIT %s
    ''', (target_emb, title, target_emb, (page-1)*top_n, top_n))
    rows = cur.fetchall()

    # 3) OMDB detaylarını ekle
    results = []
    for r in rows:
        movie_title = r[0]
        score = float(r[1])
        details = get_movie_details_omdb(movie_title)
        if details:
            details["score"] = score
            results.append(details)

    return {"film": title, "oneriler": results}


# kodları çalıştırmak için vscode da terminale uvicorn app:app --reload kodunu çalıştıyoruz.
# test içiçn http://127.0.0.1:8000/recommend?title=Avatar&top_n=5