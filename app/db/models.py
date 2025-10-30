from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Song(Base):
    __tablename__ = "songs"

    song_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    features = relationship("SongFeatures", back_populates="song", uselist=False)

class SongFeatures(Base):
    __tablename__ = "song_features"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey("songs.song_id"), nullable=False, unique=True)
    bpm = Column(Float, nullable=False)
    tempo_variation = Column(Float, nullable=False)
    mfcc_vector = Column(JSON, nullable=False)
    chroma_vector = Column(JSON, nullable=False)
    instrumentation_vector = Column(JSON, nullable=False)
    language_label = Column(String(255), nullable=False)
    genre_label = Column(String(255), nullable=False)
    processed_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), nullable=False)

    song = relationship("Song", back_populates="features")