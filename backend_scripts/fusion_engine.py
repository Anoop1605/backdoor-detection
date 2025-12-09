import psutil
import os
import joblib
import numpy as np
from stepping_stone import SteppingStoneDetector

# -------------------------
# Load Host ML Model & Scaler
# -------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "host_iso_forest.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "host_scaler.pkl")

host_model = None
scaler = None

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    host_model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("[+] Host ML model and scaler loaded successfully")
else:
    print(f"[WARNING] Host ML model or scaler not found. Run train_host_model.py first!")

# -------------------------
# Initialize Stepping Stone Detector
# -------------------------
stepping_stone = SteppingStoneDetector(local_network="192.168.0.0/16", time_threshold=2.0, byte_threshold_pct=0.1)

# -------------------------
# Host-level detectors
# -------------------------

def detect_ml_anomalies():
    """
    Uses Isolation Forest to find processes behaving strangely 
    (High CPU, weird thread counts, etc.)
    """
    if not host_model or not scaler:
        return 0.0
        
    risk_score = 0
    anomaly_count = 0
    
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent', 'num_threads', 'num_fds']):
        try:
            # Handle platform differences for num_fds
            try:
                n_fds = proc.info['num_fds'] if proc.info['num_fds'] is not None else 0
            except (AttributeError, KeyError):
                # Windows doesn't have num_fds
                n_fds = 0
            
            cpu = proc.info['cpu_percent'] or 0
            mem = proc.info['memory_percent'] or 0
            
            features = [[
                cpu,
                mem,
                proc.info['num_threads'],
                n_fds
            ]]
            
            # Apply same scaling as training
            features_scaled = scaler.transform(features)
            
            # Prediction: 1 = Normal, -1 = Anomaly
            pred = host_model.predict(features_scaled)[0]
            
            if pred == -1:
                # Calculate anomaly score (lower is more abnormal)
                score = host_model.score_samples(features_scaled)[0]
                severity = abs(score)
                
                print(f"[ML HOST ALERT] Anomaly: {proc.info['name']} (Severity: {severity:.2f})")
                
                # Accumulate risk instead of max - cap per-process contribution
                risk_score += min(severity * 0.2, 0.3)
                anomaly_count += 1
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            continue
            
    return min(risk_score, 1.0)  # Cap total risk

def detect_suspicious_processes():
    """
    String-based detection for known malicious process patterns
    """
    risky = ["nc", "ncat", "bash -i", "reverse", "python -m http.server", "/bin/sh", "cmd.exe"]
    score = 0
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmd = " ".join(p.info["cmdline"]) if p.info["cmdline"] else ""
            if any(x in cmd.lower() for x in risky):
                print(f"[SUSPICIOUS PROCESS] {p.info['name']}: {cmd[:100]}")
                score += 0.4
        except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
            pass
    return min(score, 1.0)

def detect_reverse_shell():
    """
    Detects suspicious network connections (non-standard ports)
    """
    score = 0
    suspicious_count = 0
    try:
        for c in psutil.net_connections(kind='inet'):
            if c.raddr and c.status == "ESTABLISHED":
                # Whitelist common ports
                if c.raddr.port not in (80, 443, 22, 53, 8080, 8443):
                    suspicious_count += 1
                    score += 0.2
    except (psutil.AccessDenied, AttributeError):
        pass
    
    if suspicious_count > 0:
        print(f"[NETWORK ALERT] {suspicious_count} suspicious connections detected")
    
    return min(score, 1.0)

def host_risk_score():
    """
    Combines all host-based detection methods
    """
    total_score = (
        detect_suspicious_processes() + 
        detect_reverse_shell() + 
        detect_ml_anomalies()
    )
    return min(total_score, 1.0)

# -------------------------
# Fusion logic
# -------------------------
def fusion_analyze(event):
    """
    Main fusion engine combining ANN, Host-based, and Network-based detection
    """
    # Get ANN score from event
    ann = float(event.get("ann_score", 0.0))
    
    # Get host-based risk score
    host = host_risk_score()
    
    # Check for stepping stone attack
    stepping_stone_alert = stepping_stone.check_relay(event)
    stepping_stone_score = 0.8 if stepping_stone_alert else 0.0
    
    # Weighted hybrid formula (ANN + Host + Network)
    final = (ann * 0.5) + (host * 0.3) + (stepping_stone_score * 0.2)
    
    label = "MALICIOUS" if final >= 0.5 else "BENIGN"
    
    # Build result string
    result = f"{label}  Score={final:.4f}  (ANN={ann:.4f}, Host={host:.4f}, Network={stepping_stone_score:.4f})"
    
    # Add stepping stone alert if detected
    if stepping_stone_alert:
        result += f"\n{stepping_stone_alert}"
    
    return result