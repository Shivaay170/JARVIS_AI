import time
import numpy as np
from faster_whisper import WhisperModel
import os

print("Loading Whisper Small...")
start = time.time()

model = WhisperModel(
    "D:/JARVIS/whisper_model/small",
    device="cpu",
    compute_type="int8"
)

load_time = time.time() - start
print(f"Loaded in {load_time:.1f} seconds")

print("\nTesting transcription speed...")
dummy = np.zeros(16000 * 3, dtype=np.float32)

start = time.time()
segments, info = model.transcribe(
    dummy,
    language=None,
    beam_size=5,
    initial_prompt="Jarvis"
)
list(segments)
trans_time = time.time() - start

print(f"Transcription: {trans_time:.2f} sec")
print(f"Language detected: {info.language}")
print(f"Model: small ✅")
print("\nWhisper Small ready for JARVIS!")