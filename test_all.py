import sys
sys.path.insert(0, 'D:/JARVIS')
import json

print("=" * 40)
print("TEST 1 - Edge TTS")
print("=" * 40)
try:
    import asyncio
    import edge_tts
    import os

    async def tts_test():
        c = edge_tts.Communicate(
            'Hello Sir JARVIS online',
            voice='en-GB-RyanNeural'
        )
        await c.save('tts_test.mp3')
        size = os.path.getsize('tts_test.mp3')
        print(f"TTS OK — {size} bytes")

    asyncio.run(tts_test())
except Exception as e:
    print(f"TTS FAIL: {e}")

print()
print("=" * 40)
print("TEST 2 - Groq API")
print("=" * 40)
try:
    from groq import Groq
    with open('D:/JARVIS/config.json') as f:
        cfg = json.load(f)
    key = cfg.get('groq_api_key', '')
    print(f"Key: {key[:20]}...")
    client = Groq(api_key=key)
    r = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{
            'role': 'user',
            'content': 'say hi in 3 words'
        }],
        max_tokens=10
    )
    print(f"Groq OK: {r.choices[0].message.content}")
except Exception as e:
    print(f"Groq FAIL: {e}")

print()
print("=" * 40)
print("TEST 3 - Voice Module")
print("=" * 40)
try:
    import threading
    import time
    from modules.voice import speak
    t = threading.Thread(
        target=speak,
        args=("Testing voice Sir.",)
    )
    t.start()
    t.join(timeout=15)
    print("Voice module OK")
except Exception as e:
    print(f"Voice FAIL: {e}")

print()
print("DONE")