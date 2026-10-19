import sounddevice as sd

print("All INPUT devices:")
print("=" * 50)
devices = sd.query_devices()
for i, d in enumerate(devices):
    if d['max_input_channels'] > 0:
        print(f"Index {i}: {d['name']}")
        print(f"  Channels: {d['max_input_channels']}")
        print(f"  Sample rate: {d['default_samplerate']}")
        print()