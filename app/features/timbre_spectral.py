import librosa
import numpy as np

def compute_timbre(audio_path: str, sr: int = 22050, n_mfcc: int = 13):
    y, sr = librosa.load(audio_path, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    mfcc_mean = np.mean(mfcc, axis=1).tolist()
    mfcc_var = np.var(mfcc, axis=1).tolist()
    spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    spectral_rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))
    return {
        "mfcc_mean": mfcc_mean,
        "mfcc_var": mfcc_var,
        "spectral_centroid": spectral_centroid,
        "spectral_rolloff": spectral_rolloff
    }