import os, sqlite3, uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()
BASE=Path(__file__).parent
DB=BASE/"data"/"words.db"
UPLOADS=BASE/"uploads"
UPLOADS.mkdir(exist_ok=True)
DB.parent.mkdir(exist_ok=True)

def db():
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS words(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id TEXT NOT NULL,
      word TEXT NOT NULL,
      translation TEXT NOT NULL,
      examples TEXT DEFAULT '',
      image TEXT DEFAULT '',
      correct INTEGER DEFAULT 0,
      wrong INTEGER DEFAULT 0
    )""")
    c.commit()
    return c

app=FastAPI(title="Deutsch Lernen Mini App")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

@app.get("/api/words")
def get_words(user_id:str):
    c=db()
    rows=c.execute("SELECT * FROM words WHERE user_id=? ORDER BY id DESC",(user_id,)).fetchall()
    return [dict(r) for r in rows]

@app.post("/api/words")
def add_word(user_id:str=Form(...),word:str=Form(...),translation:str=Form(...),examples:str=Form(""),image:UploadFile|None=File(None)):
    image_url=""
    if image and image.filename:
        ext=Path(image.filename).suffix.lower()
        if ext not in [".jpg",".jpeg",".png",".webp",".gif"]:
            ext=".jpg"
        name=uuid.uuid4().hex+ext
        (UPLOADS/name).write_bytes(image.file.read())
        image_url="/uploads/"+name
    c=db()
    c.execute("INSERT INTO words(user_id,word,translation,examples,image) VALUES(?,?,?,?,?)",
              (user_id,word,translation,examples,image_url))
    c.commit()
    return {"ok":True}

@app.post("/api/result")
def result(user_id:str=Form(...),word_id:int=Form(...),correct:bool=Form(...)):
    c=db()
    field="correct" if correct else "wrong"
    c.execute(f"UPDATE words SET {field}={field}+1 WHERE id=? AND user_id=?",(word_id,user_id))
    c.commit()
    return {"ok":True}

app.mount("/uploads",StaticFiles(directory=UPLOADS),name="uploads")
app.mount("/",StaticFiles(directory=BASE/"web",html=True),name="web")
