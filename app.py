#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
import subprocess
import threading
import os
import config

app = Flask(__name__)

# -----------------------------------------
# PATHS (from config.py)
# -----------------------------------------
STREAM_SCRIPT = config.STREAM_SCRIPT
HYBRID_SCRIPT = config.HYBRID_SCRIPT

processes = {
    "suricata": None,
    "stream": None,
    "hybrid": None
}

# Log files (from config.py)
ANN_LOG = config.ANN_LOG
HYBRID_LOG = config.HYBRID_LOG
SURICATA_LOG = config.SURICATA_LOG


# -----------------------------------------
# LOG PIPE FUNCTION (writes stdout → logfile)
# -----------------------------------------
def pipe_output(proc, logfile):
    with open(logfile, "a") as f:
        for line in proc.stdout:
            f.write(line)
            f.flush()


# -----------------------------------------
# START MONITORING
# -----------------------------------------
@app.route("/start")
def start_monitor():
    try:
        # ---- Start Suricata ----
        if processes["suricata"] is None or processes["suricata"].poll() is not None:
            processes["suricata"] = subprocess.Popen(
                ["sudo", "suricata", "-i", config.NETWORK_INTERFACE, "--af-packet"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            threading.Thread(
                target=pipe_output,
                args=(processes["suricata"], SURICATA_LOG),
                daemon=True
            ).start()

        # ---- Start ANN Stream Engine ----
        if processes["stream"] is None or processes["stream"].poll() is not None:
            processes["stream"] = subprocess.Popen(
                ["sudo", config.PYTHON_EXECUTABLE, STREAM_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            threading.Thread(
                target=pipe_output,
                args=(processes["stream"], ANN_LOG),
                daemon=True
            ).start()

        # ---- Start Hybrid Engine ----
        if processes["hybrid"] is None or processes["hybrid"].poll() is not None:
            processes["hybrid"] = subprocess.Popen(
                ["sudo", config.PYTHON_EXECUTABLE, HYBRID_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            threading.Thread(
                target=pipe_output,
                args=(processes["hybrid"], HYBRID_LOG),
                daemon=True
            ).start()

        return jsonify({"status": "running"})

    except Exception as e:
        return jsonify({"error": str(e)})


# -----------------------------------------
# STOP MONITORING
# -----------------------------------------
@app.route("/stop")
def stop_monitor():
    for name, proc in processes.items():
        if proc and proc.poll() is None:
            proc.terminate()
    return jsonify({"status": "stopped"})


# -----------------------------------------
# API ENDPOINTS FOR UI
# -----------------------------------------
@app.route("/stream_ann")
def stream_ann():
    if not os.path.exists(ANN_LOG):
        return jsonify([])
    return jsonify(open(ANN_LOG).read().splitlines()[-30:])  # last 30 lines


@app.route("/stream_hybrid")
def stream_hybrid():
    if not os.path.exists(HYBRID_LOG):
        return jsonify([])
    return jsonify(open(HYBRID_LOG).read().splitlines()[-30:])


@app.route("/stream_suricata")
def stream_suricata():
    if not os.path.exists(SURICATA_LOG):
        return jsonify([])
    return jsonify(open(SURICATA_LOG).read().splitlines()[-30:])


# -----------------------------------------
# DASHBOARD HOME
# -----------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------------------
# RUN APP
# -----------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
