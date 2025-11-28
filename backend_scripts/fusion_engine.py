import psutil
import os

# -------------------------
# Host-level detectors
# -------------------------
def detect_suspicious_processes():
    risky = ["nc", "ncat", "bash -i", "reverse", "python -m http.server"]
    score = 0
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmd = " ".join(p.info["cmdline"])
            if any(x in cmd.lower() for x in risky):
                score += 0.2
        except:
            pass
    return min(score, 1.0)

def detect_reverse_shell():
    score = 0
    for c in psutil.net_connections():
        if c.raddr and c.status == "ESTABLISHED":
            if c.raddr.port not in (80, 443):
                score += 0.3
    return min(score, 1.0)

def host_risk_score():
    return min(
        detect_suspicious_processes() +
        detect_reverse_shell(),
        1.0
    )

# -------------------------
# Fusion logic
# -------------------------
def fusion_analyze(event):
    ann = float(event.get("ann_score", 0.0))
    host = host_risk_score()

    # Weighted hybrid formula
    final = (ann * 0.6) + (host * 0.4)

    label = "MALICIOUS" if final >= 0.5 else "BENIGN"

    return f"{label}  Score={final:.4f}  (ANN={ann:.4f}, Host={host:.4f})"
