import os
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '0'

print("Starting Whisper Small download...")

from huggingface_hub import snapshot_download

path = snapshot_download(
    repo_id="Systran/faster-whisper-small",
    local_dir="D:/JARVIS/whisper_model/small",
    local_dir_use_symlinks=False
)

print(f"Downloaded to: {path}")
print("DONE!")