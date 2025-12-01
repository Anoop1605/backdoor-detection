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

The system consists of three main components managed by a central Flask dashboard:

1.  **Suricata IDS (Network Layer)**
    -   Captures and logs network traffic events to `eve.json`.
    -   Detects known signatures (alerts).

2.  **ANN Detection Engine (Analysis Layer)**
    -   Analyzes network flows using a pre-trained Deep Learning model (TensorFlow/Keras).
    -   Predicts "MALICIOUS" or "BENIGN" based on flow features.

3.  **Hybrid Fusion Engine (Correlation Layer)**
    -   Combines ANN predictions with host-based indicators (suspicious processes, reverse shells).
    -   Calculates a weighted risk score: `Final = (ANN * 0.6) + (Host * 0.4)`.

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
├── app.py                  # Main Flask application (Production)
├── demo_mode.py            # Demo application (Simulated)
├── demo_data_generator.py  # Traffic simulator for demo
├── config.py               # Centralized configuration
├── backend_scripts/        # Core detection logic
│   ├── stream_connection.py  # ANN Engine
│   ├── hybrid_monitor.py     # Hybrid Engine
│   └── fusion_engine.py      # Risk scoring logic
├── models/                 # ML model files directory
├── static/                 # CSS & JS assets
├── templates/              # HTML templates
└── requirements.txt        # Python dependencies
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
