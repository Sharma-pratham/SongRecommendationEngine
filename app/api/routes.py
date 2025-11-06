from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.ingest_service import ingest_audio_file
from app.services.feature_service import list_songs, get_song, get_recommendations

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/songs")
def api_list_songs(db: Session = Depends(get_db), limit: int = 50):
    return [{"song_id": s.song_id, "title": s.title, "artist": s.artist} for s in list_songs(db, limit)]

@router.get("/songs/{song_id}")
def api_get_song(song_id: int, db: Session = Depends(get_db)):
    s = get_song(db, song_id)
    if not s:
        raise HTTPException(status_code=404, detail="Song not found")
    return {"song_id": s.song_id, "title": s.title, "artist": s.artist, "file_path": s.file_path}

@router.post("/ingest")
def api_ingest(
    file: UploadFile = File(...),
    title: str = Form(""),
    artist: str = Form(""),
    db: Session = Depends(get_db)
):
    try:
        song_id = ingest_audio_file(db, file, title, artist)
        return {"song_id": song_id, "status": "processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend")
def api_recommend(filters: dict, db: Session = Depends(get_db)):
    try:
        recs = get_recommendations(db, filters)
        return {"recommendations": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))