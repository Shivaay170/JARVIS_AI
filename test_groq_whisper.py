import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import json
from groq import Groq

with open('D:/JARVIS/config.json') as f:
    cfg = json.load(f)

client = Groq(api_key=cfg['groq_api_key'])

print("Recording 3 seconds — say something...")
time.sleep(1)

audio = sd.rec(
    int(3 * 16000),
    samplerate=16000,
    channels=1,
    dtype='int16',
    device=15  # glasses mic
)
sd.wait()
print("Processing...")

wav.write('test_groq.wav', 16000, audio)

start = time.time()

with open('test_groq.wav', 'rb') as f:
    result = client.audio.transcriptions.create(
        file=('audio.wav', f),
        model="whisper-large-v3",
        language="hi",
        response_format="text"
    )

elapsed = time.time() - start

print(f"Groq Whisper Large V3: {elapsed:.2f} sec")
print(f"Detected: '{result}'")
print()
if elapsed < 1.0:
    print("FAST! Use Groq Whisper in JARVIS")
else:
    print("Slow internet — keep local Whisper")

import os
os.remove('test_groq.wav')