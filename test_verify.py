import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os

MIC_INDEX = 15
SAMPLE_RATE = 16000

print("Testing voice verification...")
print("Say something in 2 seconds...")

import time
time.sleep(2)

audio = sd.rec(
    int(3 * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype='int16',
    device=MIC_INDEX
)
sd.wait()

audio_flat = audio.flatten()

# Save temp
wav.write('test_verify.wav', SAMPLE_RATE, audio_flat)

# Load profile
from resemblyzer import VoiceEncoder, preprocess_wav

encoder = VoiceEncoder()
owner = np.load(
    'D:/JARVIS/voice_profile/owner_profile.npy'
)

test_wav = preprocess_wav('test_verify.wav')
test_emb = encoder.embed_utterance(test_wav)

similarity = np.dot(test_emb, owner) / (
    np.linalg.norm(test_emb) * 
    np.linalg.norm(owner)
)

print(f"\nSimilarity: {similarity:.3f}")
print(f"Threshold:  0.75")

if similarity >= 0.75:
    print("✅ OWNER VERIFIED!")
elif similarity >= 0.60:
    print("⚠️ Close — lower threshold to 0.60")
else:
    print("❌ Not matching — re-enroll karo")

os.remove('test_verify.wav')