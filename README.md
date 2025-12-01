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

### Common Errors and Solutions

#### ❌ Error: `ModuleNotFoundError: No module named 'tensorflow.python'`

**What it means**: This error appears when running production mode (`app.py`) but TensorFlow is not properly installed.

**Solution**:
```bash
# Option 1: Use Demo Mode (No TensorFlow required)
python3 demo_mode.py

# Option 2: Install TensorFlow for Production Mode
source .venv/bin/activate
pip install tensorflow>=2.10.0 pandas scikit-learn joblib numpy
```

**Note**: If you see this error but TensorFlow IS installed, it's likely because the real issue is the missing Suricata log file (see below).

---

#### ❌ Error: `FileNotFoundError: [Errno 2] No such file or directory: '/var/log/suricata/eve.json'`

**What it means**: The system is trying to read Suricata network logs, but Suricata is not installed or not running.

**Solution**:

**Option 1: Use Demo Mode (Recommended for Testing)**
```bash
python3 demo_mode.py
```
Demo mode simulates all network traffic and doesn't require Suricata.

**Option 2: Install Suricata (For Production)**
```bash
# Install Suricata
sudo apt update
sudo apt install suricata

# Start Suricata
sudo systemctl start suricata
sudo systemctl enable suricata

# Verify log file exists
ls -la /var/log/suricata/eve.json

# Then run production mode
sudo python3 app.py
```

---

### 🎭 Demo Mode vs 🏭 Production Mode

| Feature | Demo Mode | Production Mode |
|---------|-----------|-----------------|
| **Command** | `python3 demo_mode.py` | `sudo python3 app.py` |
| **Requires Suricata** | ❌ No | ✅ Yes |
| **Requires ML Models** | ❌ No | ✅ Yes |
| **Network Traffic** | 🎭 Simulated | 🌐 Real |
| **Detection** | 🤖 Mock heuristics | 🧠 Real ML models |
| **Use Case** | Testing, demos, development | Production monitoring |
| **Setup Time** | ⚡ Instant | 🕐 30+ minutes |

**When to use Demo Mode**:
- ✅ Testing the dashboard UI
- ✅ Demonstrating the system
- ✅ Development and debugging
- ✅ No Suricata available
- ✅ Quick evaluation

**When to use Production Mode**:
- ✅ Real network monitoring
- ✅ Actual threat detection
- ✅ Security operations
- ✅ Suricata is installed and configured

---

### Other Common Issues

-   **Port 7000 in use?**
    ```bash
    lsof -ti:7000 | xargs kill -9
    ```

-   **Permission denied errors?**
    Production mode requires sudo for network monitoring:
    ```bash
    sudo python3 app.py
    ```

-   **Missing models directory?**
    Create it and add your trained models:
    ```bash
    mkdir -p models/
    # Add: backdoor_ann_model.h5, scaler.pkl, encoders.pkl, etc.
    ```

-   **Demo mode not generating traffic?**
    Ensure `demo_data_generator.py` exists and is executable:
    ```bash
    chmod +x demo_data_generator.py
    ```

---

## 📜 License
[MIT License](LICENSE)
