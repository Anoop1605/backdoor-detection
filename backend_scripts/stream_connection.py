#!/usr/bin/env python3
import json
import time
import os
import sys
import numpy as np
import joblib
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# -----------------------------------------
# PATHS (from config.py)
# -----------------------------------------
EVE_FILE = config.SURICATA_EVE_LOG
MODEL_PATH = config.MODEL_PATH
SCALER_PKL = config.SCALER_PKL
SCALER_MEAN = config.SCALER_MEAN
SCALER_SCALE = config.SCALER_SCALE
ENCODERS_PKL = config.ENCODERS_PKL
TRAIN_CSV = config.TRAIN_CSV

LOG_FILE = config.ANN_LOG

print("Streaming Suricata logs into Hybrid Engine...")

# -------------------------
# Load ANN Model
# -------------------------
model = load_model(MODEL_PATH)

# -------------------------
# Load Scaler
# -------------------------
scaler = None
if os.path.exists(SCALER_PKL):
    try:
        scaler = joblib.load(SCALER_PKL)
        print("Loaded scaler from scaler.pkl")
    except:
        pass

if scaler is None and os.path.exists(SCALER_MEAN) and os.path.exists(SCALER_SCALE):
    s = StandardScaler()
    s.mean_ = np.load(SCALER_MEAN)
    s.scale_ = np.load(SCALER_SCALE)
    scaler = s
    print("Loaded scaler from mean/scale npy")

if scaler is None:
    raise SystemExit("ERROR: No scaler found")

# -------------------------
# Load Encoders
# -------------------------
encoders = {}
if os.path.exists(ENCODERS_PKL):
    encoders = joblib.load(ENCODERS_PKL)
    print("Loaded encoders")

# -------------------------
# Determine Expected Column Order
# -------------------------
df0 = pd.read_csv(TRAIN_CSV, nrows=0)
X_columns = list(df0.columns)
if "alert" in X_columns:
    X_columns.remove("alert")

print("Training column order:", X_columns)

# -------------------------
# Build features from event
# -------------------------
def build_row_from_event(event, X_columns, encoders):
    flow = event.get("flow", {})

    row = {
        "timestamp": event.get("timestamp", ""),
        "src_ip": event.get("src_ip", ""),
        "src_port": event.get("src_port", 0),
        "dest_ip": event.get("dest_ip", ""),
        "dest_port": event.get("dest_port", 0),
        "proto": event.get("proto", flow.get("proto", "")),
        "pkts_toserver": flow.get("pkts_toserver", 0),
        "pkts_toclient": flow.get("pkts_toclient", 0),
        "bytes_toserver": flow.get("bytes_toserver", 0),
        "bytes_toclient": flow.get("bytes_toclient", 0),
        "flow_age": flow.get("age", flow.get("flow_age", 0))
    }

    # Fill missing columns with 0
    for c in X_columns:
        if c not in row:
            row[c] = 0

    df_row = pd.DataFrame([row], columns=X_columns)

    # Apply label encoders
    for col, enc in encoders.items():
        if col in df_row.columns:
            try:
                df_row[col] = enc.transform(df_row[col].astype(str))
            except:
                df_row[col] = -1  # fallback for unseen labels

    # Convert numeric
    for c in df_row.columns:
        if c != "timestamp":
            df_row[c] = pd.to_numeric(df_row[c], errors="coerce").fillna(0)

    return df_row

# -------------------------
# Align features to scaler
# -------------------------
def align_and_scale(df_row, scaler):
    expected = scaler.mean_.shape[0]
    cols = [c for c in df_row.columns if c != "timestamp"]

    if len(cols) > expected:
        cols = cols[:expected]

    arr = df_row[cols].to_numpy(dtype=float).reshape(1, -1)

    if arr.shape[1] < expected:
        padded = np.zeros((1, expected))
        padded[0, :arr.shape[1]] = arr
        arr = padded

    return scaler.transform(arr)

# -------------------------
# Live Loop
# -------------------------
with open(EVE_FILE, "r") as f:
    f.seek(0, 2)  # jump to end, only new events
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue

        try:
            event = json.loads(line)
        except:
            continue

        # Only process useful Suricata events
        if event.get("event_type") not in ("flow", "alert", "dns", "tls", "quic"):
            continue

                # -----------------------
        # ANN PREDICTION ENGINE
        # -----------------------
        try:
            # Build row & scale features
            df_row = build_row_from_event(event, X_columns, encoders)
            Xs = align_and_scale(df_row, scaler)

            # ANN model prediction
            score = float(model.predict(Xs, verbose=0)[0][0])
            label = "MALICIOUS" if score > 0.5 else "BENIGN"

            # Form log line
            log_line = f"[+] Prediction: {label}  Score={score:.4f}\n"

            # Print to console
            print(log_line, end="")

            # Write log for dashboard
            with open("/tmp/ann_live.log", "a") as lf:
                lf.write(log_line)

        except Exception as e:
            print(f"Stream Error: {e}")
            continue


