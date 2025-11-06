import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.config import settings
from app.db.models import Song, SongFeatures
from app.features.beat_tempo import compute_tempo
from app.features.timbre_spectral import compute_timbre
from app.features.chroma_harmony import compute_chroma
from app.features.instrumentation_vocals import compute_instruments_and_language
from app.features.genre_classification import classify_genre

UPLOAD_DIR = settings.UPLOAD_DIR

def ensure_dirs():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload(file: UploadFile) -> str:
    ensure_dirs()
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, unique_name)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path

def ingest_audio_file(db: Session, file: UploadFile, title: str, artist: str) -> int:
    # 1) Save file + create Song row
    file_path = save_upload(file)
    song = Song(title=title or file.filename, artist=artist, file_path=file_path)
    db.add(song)
    db.commit()
    db.refresh(song)

    # 2) Extract features (sync for now)
    tempo = compute_tempo(file_path)
    timbre = compute_timbre(file_path)
    chroma = compute_chroma(file_path)
    instr_lang = compute_instruments_and_language(file_path)
    genre = classify_genre({**tempo, **timbre, **chroma, **instr_lang})

    # 3) Insert SongFeatures
    feats = SongFeatures(
        song_id=song.song_id,
        bpm=tempo["bpm"],
        tempo_variation=tempo["tempo_variation"],
        mfcc_vector={"mean": timbre["mfcc_mean"], "var": timbre["mfcc_var"]},
        chroma_vector={"mean": chroma["chroma_mean"], "var": chroma["chroma_var"]},
        instrumentation_vector=instr_lang["instrumentation"],
        language_label=instr_lang["language_label"],
        genre_label=genre["genre_label"]
    )
    db.add(feats)
    db.commit()

    return song.song_id