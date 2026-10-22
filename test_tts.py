import asyncio
import edge_tts
import os

async def test():
    print("Testing Edge TTS...")
    c = edge_tts.Communicate(
        'Hello Sir, JARVIS systems online.',
        voice='en-GB-RyanNeural'
    )
    await c.save('test_tts.mp3')
    size = os.path.getsize('test_tts.mp3')
    print(f"File size: {size} bytes")
    if size > 1000:
        print("TTS OK!")
    else:
        print("TTS FAIL - file too small")

asyncio.run(test())