import numpy as np
import librosa

def compute_tempo(audio_path: str, sr: int = 22050):
    y, sr = librosa.load(audio_path, sr=sr)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    bpm = float(tempo)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    intervals = np.diff(beat_times)
    tempo_var = float(np.std(intervals) / np.mean(intervals)) if intervals.size > 1 else 0.0
    return {"bpm": bpm, "tempo_variation": tempo_var, "beat_times": beat_times.tolist()}