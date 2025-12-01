# Cyber Defense Monitoring Dashboard

A real-time Network + Host Threat Detection System designed to detect backdoors and malicious activity using a hybrid approach. It combines network-level anomaly detection (using Suricata and an Artificial Neural Network) with host-level risk assessment.

---

## 🚀 Quick Demo

Want to see it in action without complex setup? Run the **Demo Mode**:

```bash
# 1. Install minimal dependencies
sudo apt install python3-flask python3-psutil

# 2. Run the demo
python3 demo_mode.py
```

Access the dashboard at **http://localhost:7000**.

**Demo Features**:
- 🎭 Simulated network traffic (benign & malicious)
- 🤖 Mock ANN & Hybrid engines
- 🛡️ No Suricata or ML models required
- 📊 Full dashboard UI

---

## 🏗️ System Architecture

The system consists of four main detection layers managed by a central Flask dashboard:

1.  **Suricata IDS (Network Layer)**
    -   Captures and logs network traffic events to `eve.json`.
    -   Detects known signatures (alerts).

2.  **ANN Detection Engine (Analysis Layer)**
    -   Analyzes network flows using a pre-trained Deep Learning model (TensorFlow/Keras).
    -   Predicts "MALICIOUS" or "BENIGN" based on flow features.

3.  **Host-Based ML Detection (Anomaly Layer)**
    -   Uses Isolation Forest to detect anomalous process behavior.
    -   Monitors CPU, memory, threads, and file descriptors.
    -   Detects suspicious processes and reverse shells.

4.  **Stepping Stone Detector (Network Relay Layer)**
    -   Correlates inbound and outbound flows to detect relay attacks.
    -   Identifies potential command-and-control relay patterns.

5.  **Hybrid Fusion Engine (Correlation Layer)**
    -   Combines all detection layers with weighted scoring.
    -   Formula: `Final = (ANN * 0.5) + (Host * 0.3) + (Network * 0.2)`
    -   Provides comprehensive threat assessment.

---

## 🛠️ Installation (Production)

To run the full system with real detection capabilities:

### 1. Prerequisites
-   **System**: Linux (Ubuntu/Debian recommended)
-   **Python**: 3.8+
-   **Suricata**: Installed and running

### 2. Install Dependencies
```bash
# System packages (recommended)
sudo apt install suricata python3-flask python3-pandas python3-tensorflow python3-scikit-learn python3-psutil

# OR via pip
pip install -r requirements.txt
```

### 3. Setup Model Files
Place your trained ML model files in the `models/` directory:
-   `backdoor_ann_model.h5`
-   `scaler.pkl`, `scaler_mean.npy`, `scaler_scale.npy`
-   `encoders.pkl`
-   `network_dataset.csv`

### 4. Configuration
Copy `.env.example` to `.env` to customize settings:
```bash
cp .env.example .env
nano .env
```
Key settings:
-   `NETWORK_INTERFACE`: Interface to monitor (default: `eth0`)
-   `SURICATA_EVE_LOG`: Path to Suricata logs (default: `/var/log/suricata/eve.json`)

---

## 🚦 Usage

### Running the Dashboard
```bash
sudo python3 app.py
```

### Operation
1.  Open **http://localhost:7000**
2.  Click **Start Monitoring** to launch detection engines.
3.  Monitor the **Live Threat Logs** for alerts.
4.  Click **Stop Monitoring** to terminate processes.

---

## 📂 Project Structure

```
├── app.py                      # Main Flask application (Production)
├── demo_mode.py                # Demo application (Simulated)
├── demo_data_generator.py      # Traffic simulator for demo
├── config.py                   # Centralized configuration
├── backend_scripts/            # Core detection logic
│   ├── stream_connection.py      # ANN Engine
│   ├── fusion_engine.py          # Multi-layer fusion engine
│   ├── stepping_stone.py         # Network relay detector
│   ├── train_host_model.py       # ML model training
│   ├── test_integration.py       # Integration tests
│   ├── SETUP_GUIDE.md            # Detailed setup guide
│   └── README.md                 # Backend documentation
├── models/                     # ML model files directory
├── static/                     # CSS & JS assets
├── templates/                  # HTML templates
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git ignore rules
```

---

## 🔧 Troubleshooting

-   **Port 7000 in use?**
    `lsof -ti:7000 | xargs kill -9`
-   **Suricata not found?**
    Ensure Suricata is installed: `sudo apt install suricata`
-   **Missing models?**
    Check that all required files are in the `models/` directory.

---

## 📜 License
[MIT License](LICENSE)
