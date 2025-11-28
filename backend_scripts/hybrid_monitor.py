#!/usr/bin/env python3
import json
import time
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from fusion_engine import fusion_analyze

# -----------------------------------------
# PATHS (from config.py)
# -----------------------------------------
EVE_FILE = config.SURICATA_EVE_LOG
LOG_FILE = config.HYBRID_LOG

print("Hybrid Monitoring Activated...")

with open(EVE_FILE, "r") as f:
    f.seek(0, 2)

    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue

        try:
            event = json.loads(line)
        except:
            continue

        # Accept all major Suricata event types
        if event.get("event_type") not in ("flow", "alert", "dns", "tls", "http", "quic"):
            continue

        result = fusion_analyze(event)

        # Print to terminal
        # Only log fusion results (ignore TensorFlow startup messages)
if "Prediction" in result:
    print("[HYBRID]", result)
    with open(LOG_FILE, "a") as lf:
        lf.write("[HYBRID] " + result + "\n")

