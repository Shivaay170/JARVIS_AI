print("Downloading Whisper Small model...")
print("Size: ~244MB — please wait...")

from faster_whisper import WhisperModel

model = WhisperModel(
    'small',
    device='cpu',
    compute_type='int8',
    download_root='D:/JARVIS/whisper_model'
)

print("Testing model...")
import numpy as np
dummy = np.zeros(16000, dtype=np.float32)
segments, info = model.transcribe(
    dummy,
    language='en'
)
list(segments)

print("Whisper Small ready!")
print("Now update config.json:")
print('  "whisper_model_size": "small"')