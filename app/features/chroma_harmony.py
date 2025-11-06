import librosa
import numpy as np

def compute_chroma(audio_path: str, sr: int = 22050):
    y, sr = librosa.load(audio_path, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1).tolist()
    chroma_var = np.var(chroma, axis=1).tolist()
    return {"chroma_mean": chroma_mean, "chroma_var": chroma_var}