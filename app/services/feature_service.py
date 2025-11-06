from sqlalchemy.orm import Session
from app.db.models import Song, SongFeatures

def list_songs(db: Session, limit: int = 50):
    q = db.query(Song).order_by(Song.created_at.desc()).limit(limit)
    return q.all()

def get_song(db: Session, song_id: int):
    return db.query(Song).filter(Song.song_id == song_id).first()

def get_recommendations(db: Session, filters: dict):
    q = db.query(SongFeatures).join(Song)

    lang = filters.get("language")
    genre = filters.get("genre")
    bpm_min = filters.get("bpm_min")
    bpm_max = filters.get("bpm_max")

    if lang:
        q = q.filter(SongFeatures.language_label == lang)
    if genre:
        q = q.filter(SongFeatures.genre_label == genre)
    if bpm_min is not None and bpm_max is not None:
        q = q.filter(SongFeatures.bpm >= bpm_min, SongFeatures.bpm <= bpm_max)

    rows = q.limit(50).all()
    return [
        {"song_id": r.song_id, "genre": r.genre_label, "language": r.language_label, "bpm": r.bpm}
        for r in rows
    ]