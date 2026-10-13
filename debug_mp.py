import traceback
try:
    print("[TEST] Importing mediapipe...")
    import mediapipe as mp
    print(f"[TEST] Mediapipe version: {getattr(mp, '__version__', 'unknown')}")
    print(f"[TEST] Has solutions: {hasattr(mp, 'solutions')}")
    if not hasattr(mp, 'solutions'):
        print("[TEST] Attempting alternative import: import mediapipe.python.solutions")
        try:
             import mediapipe.python.solutions as solutions
             print("[TEST] Alternative import success")
        except:
             traceback.print_exc()
except Exception as e:
    traceback.print_exc()
