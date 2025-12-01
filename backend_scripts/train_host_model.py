#!/usr/bin/env python3
import psutil
import time
import joblib
import numpy as np
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Config
MODEL_PATH = "host_iso_forest.pkl"
SCALER_PATH = "host_scaler.pkl"
RECORD_SECONDS = 60
MIN_CPU_THRESHOLD = 0.1  # Filter out idle processes

print(f"[+] Starting Host Behavior Training ({RECORD_SECONDS}s)...")
print("[!] Please do NOT run any attacks or open new heavy apps during this time.")

data = []
start_time = time.time()

while time.time() - start_time < RECORD_SECONDS:
    for proc in psutil.process_iter(['cpu_percent', 'memory_percent', 'num_threads', 'num_fds']):
        try:
            cpu = proc.info['cpu_percent'] or 0
            mem = proc.info['memory_percent'] or 0
            
            # Filter out completely idle processes
            if cpu < MIN_CPU_THRESHOLD and mem < 0.1:
                continue
            
            # Handle platform differences
            try:
                n_fds = proc.info['num_fds'] if proc.info['num_fds'] is not None else 0
            except AttributeError:  # Windows doesn't have num_fds
                n_fds = len(proc.open_files()) if hasattr(proc, 'open_files') else 0
            
            features = [cpu, mem, proc.info['num_threads'], n_fds]
            data.append(features)
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    time.sleep(1)

print(f"[+] Data collection complete. Samples collected: {len(data)}")

if len(data) < 100:
    print("[ERROR] Insufficient training data. Please run for longer.")
    exit(1)

# Normalize features
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Train the model (lower contamination for clean training data)
print("[+] Training Isolation Forest...")
clf = IsolationForest(n_estimators=100, contamination=0.001, random_state=42)
clf.fit(data_scaled)

# Save both model and scaler
joblib.dump(clf, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)
print(f"[SUCCESS] Model saved to {os.path.abspath(MODEL_PATH)}")
print(f"[SUCCESS] Scaler saved to {os.path.abspath(SCALER_PATH)}")