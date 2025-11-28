#!/usr/bin/env python3
"""
Demo Mode Application - Simplified version for demonstration
Works without Suricata or ML models
"""
from flask import Flask, render_template, jsonify
import subprocess
import threading
import os
import time
import random

app = Flask(__name__)

# Demo configuration
DEMO_EVE_LOG = "/tmp/demo_eve.json"
DEMO_ANN_LOG = "/tmp/demo_ann.log"
DEMO_HYBRID_LOG = "/tmp/demo_hybrid.log"
DEMO_SURICATA_LOG = "/tmp/demo_suricata.log"

processes = {
    "generator": None,
    "ann": None,
    "hybrid": None
}

# -----------------------------------------
# MOCK ANN ENGINE
# -----------------------------------------
def mock_ann_engine():
    """Simulates ANN predictions based on simple heuristics"""
    import json
    
    print("[DEMO ANN] Starting mock ANN engine...")
    
    # Wait for file to be created
    while not os.path.exists(DEMO_EVE_LOG):
        time.sleep(0.1)
    
    with open(DEMO_EVE_LOG, "r") as f:
        f.seek(0, 2)  # Go to end
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            try:
                event = json.loads(line)
                
                # Simple heuristic: suspicious if non-standard port or has alert
                score = 0.0
                if event.get("event_type") == "alert":
                    score = random.uniform(0.7, 0.95)
                elif event.get("dest_port", 0) in [4444, 8080, 9050]:
                    score = random.uniform(0.6, 0.8)
                else:
                    score = random.uniform(0.1, 0.4)
                
                label = "MALICIOUS" if score > 0.5 else "BENIGN"
                log_line = f"[+] Prediction: {label}  Score={score:.4f}\n"
                
                print(log_line, end="")
                with open(DEMO_ANN_LOG, "a") as lf:
                    lf.write(log_line)
                    lf.flush()
                    
            except Exception as e:
                print(f"[DEMO ANN ERROR] {e}")
                continue

# -----------------------------------------
# MOCK HYBRID ENGINE
# -----------------------------------------
def mock_hybrid_engine():
    """Simulates hybrid detection with host monitoring"""
    import json
    
    print("[DEMO HYBRID] Starting mock hybrid engine...")
    
    # Wait for file to be created
    while not os.path.exists(DEMO_EVE_LOG):
        time.sleep(0.1)
    
    with open(DEMO_EVE_LOG, "r") as f:
        f.seek(0, 2)  # Go to end
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            try:
                event = json.loads(line)
                
                # Mock ANN score
                if event.get("event_type") == "alert":
                    ann_score = random.uniform(0.7, 0.95)
                else:
                    ann_score = random.uniform(0.1, 0.4)
                
                # Mock host score
                host_score = random.uniform(0.0, 0.3)
                
                # Fusion
                final_score = (ann_score * 0.6) + (host_score * 0.4)
                label = "MALICIOUS" if final_score >= 0.5 else "BENIGN"
                
                log_line = f"[HYBRID] {label}  Score={final_score:.4f}  (ANN={ann_score:.4f}, Host={host_score:.4f})\n"
                
                print(log_line, end="")
                with open(DEMO_HYBRID_LOG, "a") as lf:
                    lf.write(log_line)
                    lf.flush()
                    
            except Exception as e:
                print(f"[DEMO HYBRID ERROR] {e}")
                continue

# -----------------------------------------
# MOCK SURICATA LOGGER
# -----------------------------------------
def mock_suricata_logger():
    """Simulates Suricata logging"""
    import json
    
    print("[DEMO SURICATA] Starting mock Suricata logger...")
    
    with open(DEMO_EVE_LOG, "r") as f:
        f.seek(0, 2)  # Go to end
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            try:
                event = json.loads(line)
                
                if event.get("event_type") == "alert":
                    log_line = f"[ALERT] {event.get('alert', {}).get('signature', 'Unknown')} - {event['src_ip']}:{event['src_port']} -> {event['dest_ip']}:{event['dest_port']}\n"
                else:
                    log_line = f"[{event['event_type'].upper()}] {event['src_ip']} -> {event['dest_ip']}:{event['dest_port']} ({event['proto']})\n"
                
                with open(DEMO_SURICATA_LOG, "a") as lf:
                    lf.write(log_line)
                    
            except Exception as e:
                continue

# -----------------------------------------
# START DEMO MONITORING
# -----------------------------------------
@app.route("/start")
def start_monitor():
    try:
        # Clear old logs
        for log in [DEMO_ANN_LOG, DEMO_HYBRID_LOG, DEMO_SURICATA_LOG]:
            open(log, "w").close()
        
        # Start data generator
        if processes["generator"] is None or processes["generator"].poll() is not None:
            processes["generator"] = subprocess.Popen(
                ["python3", "demo_data_generator.py", DEMO_EVE_LOG],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
        
        # Always start new threads (daemon threads will automatically stop)
        processes["ann"] = threading.Thread(target=mock_ann_engine, daemon=True)
        processes["ann"].start()
        
        processes["hybrid"] = threading.Thread(target=mock_hybrid_engine, daemon=True)
        processes["hybrid"].start()
        
        # Start mock Suricata logger
        threading.Thread(target=mock_suricata_logger, daemon=True).start()
        
        return jsonify({"status": "running", "demo": True})
        
    except Exception as e:
        return jsonify({"error": str(e)})

# -----------------------------------------
# STOP DEMO MONITORING
# -----------------------------------------
@app.route("/stop")
def stop_monitor():
    if processes["generator"] and processes["generator"].poll() is None:
        processes["generator"].terminate()
    
    # Threads will stop when app stops
    return jsonify({"status": "stopped", "demo": True})

# -----------------------------------------
# API ENDPOINTS
# -----------------------------------------
@app.route("/stream_ann")
def stream_ann():
    if not os.path.exists(DEMO_ANN_LOG):
        return jsonify([])
    return jsonify(open(DEMO_ANN_LOG).read().splitlines()[-30:])

@app.route("/stream_hybrid")
def stream_hybrid():
    if not os.path.exists(DEMO_HYBRID_LOG):
        return jsonify([])
    return jsonify(open(DEMO_HYBRID_LOG).read().splitlines()[-30:])

@app.route("/stream_suricata")
def stream_suricata():
    if not os.path.exists(DEMO_SURICATA_LOG):
        return jsonify([])
    return jsonify(open(DEMO_SURICATA_LOG).read().splitlines()[-30:])

# -----------------------------------------
# DASHBOARD
# -----------------------------------------
@app.route("/")
def index():
    return render_template("demo_index.html")

if __name__ == "__main__":
    print("=" * 60)
    print("  CYBER DEFENSE MONITORING DASHBOARD - DEMO MODE")
    print("=" * 60)
    print("\n✨ Running in DEMO mode - no Suricata or ML models required!")
    print("📊 Dashboard: http://localhost:7000")
    print("🎯 Click 'Start Monitoring' to begin the demonstration\n")
    
    app.run(host="0.0.0.0", port=7000, debug=False)
