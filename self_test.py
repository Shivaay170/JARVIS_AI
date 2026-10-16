import sys
import os
import json
import requests
import sqlite3
import time

# Ensure JARVIS path is in sys.path
sys.path.insert(0, 'D:/JARVIS')

results = {}

print("=" * 50)
print("JARVIS SELF-TEST")
print("=" * 50)

# Test 1: Email connection
print("\n[TEST 1] Email connection...")
try:
    from modules.email_agent import get_emails
    total, emails = get_emails(1)
    if total is not None:
        results['email'] = f"OK ({total} emails)"
    else:
        results['email'] = "FAIL (Connection failed)"
except Exception as e:
    results['email'] = f"FAIL (Error: {e})"
print(f"  Email: {results['email']}")

# Test 2: Face recognition DB
print("\n[TEST 2] Face recognition DB...")
try:
    from modules.face_recognition_agent import (
        load_all_persons
    )
    persons = load_all_persons()
    results['face_db'] = (
        f"OK ({len(persons)} faces registered)"
    )
    for p in persons:
        print(f"    - {p['name']} ({p['relation']})")
except Exception as e:
    results['face_db'] = f"FAIL (Error: {e})"
print(f"  Face DB: {results['face_db']}")

# Test 3: Camera
print("\n[TEST 3] Camera...")
try:
    import cv2
    import numpy as np
    import time
    wake = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(1)
    wake.release()
    time.sleep(0.3)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    for _ in range(20):
        ret, frame = cap.read()
        if ret and np.mean(frame) > 10:
            results['camera'] = (
                f"OK (Brightness: "
                f"{np.mean(frame):.1f})"
            )
            break
    else:
        results['camera'] = "FAIL (Black frames)"
    cap.release()
except Exception as e:
    results['camera'] = f"FAIL (Error: {e})"
print(f"  Camera: {results['camera']}")

# Test 4: Groq API
print("\n[TEST 4] Groq API...")
try:
    import requests, json
    config_path = "D:/JARVIS/config.json"
    if os.path.exists(config_path):
        with open(config_path) as f:
            cfg = json.load(f)
        key = cfg.get("groq_api_key", "")
        r = requests.post(
            "https://api.groq.com/openai/v1/"
            "chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "user", "content": "hi"}
                ],
                "max_tokens": 5
            },
            timeout=5
        )
        if r.status_code == 200:
            results['groq'] = "OK (Connected)"
        else:
            results['groq'] = f"FAIL (HTTP {r.status_code})"
    else:
        results['groq'] = "FAIL (config.json not found)"
except Exception as e:
    results['groq'] = f"FAIL (Error: {e})"
print(f"  Groq: {results['groq']}")

# Test 5: Ollama
print("\n[TEST 5] Ollama...")
try:
    import requests
    r = requests.get(
        "http://localhost:11434/api/tags",
        timeout=3
    )
    if r.status_code == 200:
        models = r.json().get('models', [])
        names = [m['name'] for m in models]
        results['ollama'] = (
            f"OK ({len(models)} models: "
            f"{', '.join(names[:3])})"
        )
    else:
        results['ollama'] = "FAIL (Not running)"
except:
    results['ollama'] = "FAIL (Not running)"
print(f"  Ollama: {results['ollama']}")

# Test 6: Legion listener
print("\n[TEST 6] Legion port...")
try:
    import socket
    s = socket.socket()
    result = s.connect_ex(
        ('localhost', 4444)
    )
    s.close()
    if result == 0:
        results['legion'] = (
            "OK (Port 4444 listening)"
        )
    else:
        results['legion'] = (
            "WARN (Port 4444 not active - "
            "start JARVIS first)"
        )
except Exception as e:
    results['legion'] = f"FAIL (Error: {e})"
print(f"  Legion: {results['legion']}")

# Test 7: Tesseract OCR
print("\n[TEST 7] Tesseract OCR...")
try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = (
        r'C:\Tesseract-OCR\tesseract.exe'
    )
    from PIL import Image
    img = Image.new('RGB', (100,30), 'white')
    pytesseract.image_to_string(img)
    results['tesseract'] = "OK (Working)"
except Exception as e:
    results['tesseract'] = f"FAIL (Error: {e})"
print(f"  Tesseract: {results['tesseract']}")

print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
passed = sum(
    1 for v in results.values() 
    if v.startswith("OK")
)
total_tests = len(results)
print(f"Passed: {passed}/{total_tests}")
for k, v in results.items():
    print(f"  {k:15} {v}")
print("=" * 50)
