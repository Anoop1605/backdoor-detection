#!/usr/bin/env python3
"""
Centralized configuration for Backdoor Detection System.
All paths and settings can be customized via environment variables.
"""
import os
import sys

# -------------------------
# Project Directories
# -------------------------
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_SCRIPTS_DIR = os.path.join(PROJECT_DIR, "backend_scripts")

# -------------------------
# Model Files
# -------------------------
# Default to 'models' directory in project, but allow override via env var
MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(PROJECT_DIR, "models"))

# Individual model file paths
MODEL_PATH = os.path.join(MODEL_DIR, "backdoor_ann_model.h5")
SCALER_PKL = os.path.join(MODEL_DIR, "scaler.pkl")
SCALER_MEAN = os.path.join(MODEL_DIR, "scaler_mean.npy")
SCALER_SCALE = os.path.join(MODEL_DIR, "scaler_scale.npy")
ENCODERS_PKL = os.path.join(MODEL_DIR, "encoders.pkl")
TRAIN_CSV = os.path.join(MODEL_DIR, "network_dataset.csv")

# -------------------------
# Python Executable
# -------------------------
# Use current Python interpreter by default, allow override
PYTHON_EXECUTABLE = os.getenv("PYTHON_EXECUTABLE", sys.executable)

# -------------------------
# Log Files
# -------------------------
LOG_DIR = os.getenv("LOG_DIR", "/tmp")
ANN_LOG = os.path.join(LOG_DIR, "ann_live.log")
HYBRID_LOG = os.path.join(LOG_DIR, "hybrid_live.log")
SURICATA_LOG = os.path.join(LOG_DIR, "suricata_live.log")

# -------------------------
# Suricata Configuration
# -------------------------
SURICATA_EVE_LOG = os.getenv("SURICATA_EVE_LOG", "/var/log/suricata/eve.json")
NETWORK_INTERFACE = os.getenv("NETWORK_INTERFACE", "eth0")

# -------------------------
# Script Paths
# -------------------------
STREAM_SCRIPT = os.path.join(BACKEND_SCRIPTS_DIR, "stream_connection.py")
HYBRID_SCRIPT = os.path.join(BACKEND_SCRIPTS_DIR, "hybrid_monitor.py")
