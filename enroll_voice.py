import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import time
import torch

MIC_INDEX = 15  # Fire Boult glasses
SAMPLE_RATE = 16000

SAMPLE_RATE = 16000
ENROLL_DIR  = "D:/JARVIS/voice_profile"
os.makedirs(ENROLL_DIR, exist_ok=True)

PHRASES = [
    "Jarvis open chrome",
    "What is the time Jarvis",
    "Jarvis check my email",
    "Hey Jarvis how are you",
    "Jarvis open youtube"
]

def record_sample(duration=4, index=0):
    print(f"\n--- Sample {index+1}/5 ---")
    print(f"Say: '{PHRASES[index]}'")
    print("Recording in 3 seconds...")
    time.sleep(3)
    print("🔴 RECORDING NOW...")
    
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16',
        device=MIC_INDEX  
    )
    sd.wait()
    print("✅ Done!")
    
    path = f"{ENROLL_DIR}/sample_{index}.wav"
    wav.write(path, SAMPLE_RATE, audio)
    return path

print("=" * 50)
print("JARVIS VOICE ENROLLMENT")
print("=" * 50)
print("Speak naturally and clearly.")
print("Use your GLASSES/HEADPHONE mic!")
print("Keep same distance each time.")
print("=" * 50)

input("\nPress ENTER to start enrollment...")

samples = []
for i in range(5):
    path = record_sample(duration=4, index=i)
    samples.append(path)
    print(f"Saved: {path}")
    time.sleep(1)

print("\nCreating voice profile...")

from resemblyzer import VoiceEncoder, preprocess_wav

encoder = VoiceEncoder()
embeddings = []

for path in samples:
    wav_data = preprocess_wav(path)
    embedding = encoder.embed_utterance(wav_data)
    embeddings.append(embedding)
    print(f"Processed: {path}")

# Average all samples
owner_embedding = np.mean(embeddings, axis=0)

# Save profile
profile_path = f"{ENROLL_DIR}/owner_profile.npy"
np.save(profile_path, owner_embedding)

print("\n" + "=" * 50)
print("✅ Voice profile saved!")
print(f"   Path: {profile_path}")
print("JARVIS will now only respond to YOU!")
print("=" * 50)
