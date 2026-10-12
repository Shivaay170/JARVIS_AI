"""
JARVIS AR Vision — Step-by-step Diagnostic Script
Run this INSTEAD of test_ar_vision.py to find exactly what's failing.
Each step is isolated. If one fails, the rest still run.

Usage: python diagnose_ar.py
"""

import os
import sys
import time

# Silence TensorFlow/oneDNN noise immediately
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["GRPC_VERBOSITY"] = "ERROR"

PASS = "  [PASS]"
FAIL = "  [FAIL]"
INFO = "  [INFO]"

results = []

def test(name, fn):
    print(f"\n--- {name} ---")
    try:
        msg = fn()
        print(f"{PASS} {msg}")
        results.append((name, True, msg))
    except Exception as e:
        print(f"{FAIL} {e}")
        results.append((name, False, str(e)))

# ─────────────────────────────────────────────
# TEST 1: Basic Python environment
# ─────────────────────────────────────────────
def check_python():
    v = sys.version
    assert sys.version_info >= (3, 8), "Need Python 3.8+"
    return f"Python {v.split()[0]}"

test("Python version", check_python)

# ─────────────────────────────────────────────
# TEST 2: Core packages
# ─────────────────────────────────────────────
def check_numpy():
    import numpy as np
    return f"numpy {np.__version__}"

def check_cv2():
    import cv2
    return f"opencv {cv2.__version__}"

def check_ultralytics():
    import ultralytics
    return f"ultralytics {ultralytics.__version__}"

def check_requests():
    import requests
    return f"requests {requests.__version__}"

def check_bs4():
    import bs4
    return f"beautifulsoup4 {bs4.__version__}"

def check_feedparser():
    import feedparser
    return f"feedparser {feedparser.__version__}"

test("numpy", check_numpy)
test("opencv", check_cv2)
test("ultralytics / YOLOv8", check_ultralytics)
test("requests", check_requests)
test("beautifulsoup4", check_bs4)
test("feedparser", check_feedparser)

# ─────────────────────────────────────────────
# TEST 3: JARVIS module imports
# ─────────────────────────────────────────────
def check_object_database():
    sys.path.insert(0, ".")
    from modules.object_database import get_object_info
    info = get_object_info("laptop")
    assert info is not None, "get_object_info('laptop') returned None"
    return f"object_database OK — laptop has {len(info.get('components', []))} components"

def check_ar_vision_import():
    from modules.ar_vision import ARVisionEngine
    return "ARVisionEngine class imported OK"

def check_ar_controller_import():
    from modules.ar_controller import ARController
    return "ARController class imported OK"

test("modules/object_database.py", check_object_database)
test("modules/ar_vision.py import", check_ar_vision_import)
test("modules/ar_controller.py import", check_ar_controller_import)

# ─────────────────────────────────────────────
# TEST 4: YOLO model
# ─────────────────────────────────────────────
def check_yolo_model():
    import os
    # Check common locations
    locations = [
        "yolov8n.pt",
        "models/yolov8n.pt",
        os.path.join(os.path.expanduser("~"), ".config", "Ultralytics", "yolov8n.pt"),
    ]
    found = None
    for loc in locations:
        if os.path.exists(loc):
            found = loc
            break
    if found:
        size_mb = os.path.getsize(found) / (1024 * 1024)
        return f"Found at '{found}' ({size_mb:.1f} MB)"
    else:
        # Try to download/load via ultralytics (will auto-download)
        from ultralytics import YOLO
        print(f"{INFO} yolov8n.pt not found locally — ultralytics will auto-download on first use (~6MB)")
        return "Not cached locally — will auto-download on first YOLO() call (OK)"

test("YOLOv8n model file", check_yolo_model)

# ─────────────────────────────────────────────
# TEST 5: Camera
# ─────────────────────────────────────────────
def check_camera():
    import cv2
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        # Try index 1
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            raise RuntimeError("No camera found at index 0 or 1. Check if camera is connected and not used by another app.")
    ret, frame = cap.read()
    cap.release()
    if not ret or frame is None:
        raise RuntimeError("Camera opened but could not read a frame.")
    h, w = frame.shape[:2]
    return f"Camera OK — resolution {w}x{h}"

test("Camera (OpenCV)", check_camera)

# ─────────────────────────────────────────────
# TEST 6: Quick YOLO inference (no camera — test image)
# ─────────────────────────────────────────────
def check_yolo_inference():
    import numpy as np
    from ultralytics import YOLO
    print(f"{INFO} Loading YOLOv8n (may download ~6MB if first run)...")
    model = YOLO("yolov8n.pt")
    # Create a blank test image (640x480 gray)
    dummy = np.zeros((480, 640, 3), dtype="uint8")
    # Add a white rectangle so YOLO has something to look at
    dummy[100:300, 150:450] = 200
    t0 = time.time()
    results_yolo = model(dummy, verbose=False)
    elapsed = time.time() - t0
    return f"YOLO inference OK in {elapsed:.2f}s (blank frame — real objects will detect fine)"

test("YOLOv8n inference speed", check_yolo_inference)

# ─────────────────────────────────────────────
# TEST 7: WebSocket bridge reachability
# ─────────────────────────────────────────────
def check_websocket_port():
    import socket
    # Just check if port 8765 is in use (JARVIS running) or available
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(("127.0.0.1", 8765))
    sock.close()
    if result == 0:
        return "Port 8765 is OPEN — JARVIS WebSocket bridge is running"
    else:
        return "Port 8765 is free (JARVIS not running yet — that's OK for this test)"

test("WebSocket bridge port 8765", check_websocket_port)

# ─────────────────────────────────────────────
# TEST 8: News intelligence module
# ─────────────────────────────────────────────
def check_news_intel_import():
    try:
        from modules.news_intel import NewsIntelligence
        return "news_intel.py imported OK"
    except ModuleNotFoundError:
        return "news_intel.py not yet created — that's OK, create it next"
    except Exception as e:
        raise RuntimeError(f"news_intel.py exists but has errors: {e}")

test("modules/news_intel.py (optional)", check_news_intel_import)

# ─────────────────────────────────────────────
# TEST 9: Internet + Groq connectivity
# ─────────────────────────────────────────────
def check_internet():
    import requests
    r = requests.get("https://httpbin.org/get", timeout=5)
    assert r.status_code == 200, f"Got status {r.status_code}"
    return "Internet connection OK"

def check_groq_key():
    import os
    # Check common places for Groq API key
    key = (
        os.environ.get("GROQ_API_KEY") or
        os.environ.get("GROQ_KEY")
    )
    if key:
        return f"GROQ_API_KEY found in environment (starts with: {key[:8]}...)"
    # Try to find it in config files
    for cfg in ["config.py", "config.json", ".env", "modules/config.py"]:
        if os.path.exists(cfg):
            with open(cfg) as f:
                content = f.read()
            if "groq" in content.lower() and ("gsk_" in content or "key" in content.lower()):
                return f"Groq key likely found in {cfg}"
    raise RuntimeError(
        "GROQ_API_KEY not found in environment variables. "
        "Set it with: set GROQ_API_KEY=your_key_here  (Windows CMD) "
        "or check your config file."
    )

test("Internet connectivity", check_internet)
test("Groq API key", check_groq_key)

# ─────────────────────────────────────────────
# TEST 10: Google News RSS (news intel fallback)
# ─────────────────────────────────────────────
def check_google_news_rss():
    import feedparser
    feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
    assert len(feed.entries) > 0, "No entries returned from Google News RSS"
    top = feed.entries[0].title
    return f"RSS OK — top headline: '{top[:60]}...'"

test("Google News RSS feed", check_google_news_rss)

# ─────────────────────────────────────────────
# FINAL REPORT
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("DIAGNOSTIC REPORT")
print("="*60)

passed = [r for r in results if r[1]]
failed = [r for r in results if not r[1]]

for name, ok, msg in results:
    icon = "OK  " if ok else "FAIL"
    print(f"  [{icon}] {name}")
    if not ok:
        print(f"          └─ {msg}")

print(f"\n  {len(passed)}/{len(results)} tests passed")

if failed:
    print("\nFIX THESE FIRST:")
    for i, (name, _, msg) in enumerate(failed, 1):
        print(f"\n  {i}. {name}")
        print(f"     Problem: {msg}")

        # Specific fix suggestions
        if "numpy" in name.lower():
            print("     Fix: pip install numpy")
        elif "opencv" in name.lower():
            print("     Fix: pip install opencv-contrib-python")
        elif "ultralytics" in name.lower():
            print("     Fix: pip install ultralytics")
        elif "requests" in name.lower():
            print("     Fix: pip install requests")
        elif "beautifulsoup" in name.lower():
            print("     Fix: pip install beautifulsoup4")
        elif "feedparser" in name.lower():
            print("     Fix: pip install feedparser")
        elif "camera" in name.lower():
            print("     Fix: Close any app using the camera (Teams, Zoom, OBS)")
            print("           Then retry. Or check Device Manager for camera driver.")
        elif "groq" in name.lower():
            print("     Fix: Run:  set GROQ_API_KEY=gsk_your_key_here")
            print("           Or add it to your .env or config.py file")
        elif "object_database" in name.lower():
            print("     Fix: Check modules/object_database.py exists and has no syntax errors")
            print("           Run: python -c \"from modules.object_database import get_object_info\"")
        elif "ar_vision" in name.lower():
            print("     Fix: Check modules/ar_vision.py for syntax errors")
            print("           Run: python -c \"from modules.ar_vision import ARVisionEngine\"")
        elif "ar_controller" in name.lower():
            print("     Fix: Check modules/ar_controller.py for syntax errors")
            print("           Run: python -c \"from modules.ar_controller import ARController\"")

    print("\nAfter fixing, run:  python diagnose_ar.py  again")
else:
    print("\n  All systems GO. Run:  python main.py")
    print("  Then say: 'Jarvis, scan this'")

print("="*60)