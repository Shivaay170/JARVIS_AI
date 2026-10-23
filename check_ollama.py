import ollama
print(f"[TEST] Ollama attributes: {dir(ollama)}")
try:
    print(f"[TEST] Ollama version: {getattr(ollama, '__version__', 'unknown')}")
except:
    pass
