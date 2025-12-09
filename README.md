# 🛡️ Backdoor Detection System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10+-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)](https://www.linux.org/)

A **real-time Network + Host Threat Detection System** designed to detect backdoors and malicious activity using a hybrid AI-powered approach. Combines network-level anomaly detection (Suricata IDS + Deep Learning) with host-level behavioral analysis.

![Dashboard Preview](https://via.placeholder.com/800x400/1a1a2e/16213e?text=Cyber+Defense+Dashboard)

---

## ✨ Features

### 🔍 **Multi-Layer Detection**
- **Network IDS**: Suricata-based signature detection
- **AI/ML Detection**: Deep Neural Network for anomaly detection
- **Host Monitoring**: Isolation Forest for process behavior analysis
- **Hybrid Fusion**: Weighted correlation of all detection layers

### 🎯 **Attack Detection Capabilities**
- ✅ Port Scanning
- ✅ Reverse Shells & Backdoors
- ✅ SSH Brute Force
- ✅ DNS Tunneling
- ✅ DDoS/Flood Attacks
- ✅ Command & Control (C2) Communication
- ✅ Suspicious Process Behavior
- ✅ Network Relay Attacks

### 📊 **Real-Time Monitoring**
- Live web dashboard with threat visualization
- Multi-channel alerting (Email, Slack, SMS, Webhook)
- Comprehensive logging and audit trails
- Performance metrics and accuracy tracking

### 🧪 **Testing & Validation**
- Automated attack simulation suite
- Manual attack testing framework
- Accuracy measurement tools
- Confusion matrix generation

---

## 🚀 Quick Start

### **Option 1: Demo Mode** (No Setup Required)

Try the system immediately with simulated data:

```bash
# Install minimal dependencies
sudo apt install python3-flask python3-psutil

# Run demo
python3 demo_mode.py
```

Access dashboard at **http://localhost:7000**

### **Option 2: Production Mode** (Full Detection)

For real network monitoring with trained ML models:

```bash
# 1. Install dependencies
pip install -r requirements.txt
sudo apt install suricata

# 2. Configure environment
cp .env.example .env
nano .env  # Edit settings

# 3. Train models (or use pre-trained)
python3 backend_scripts/train_network_model.py --dataset data/network_traffic.csv

# 4. Start system
sudo python3 app.py
```

📖 **Detailed Guide**: See [QUICKSTART.md](QUICKSTART.md) for step-by-step instructions

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Documentation](#-documentation)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Attack Testing](#-attack-testing)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📚 Documentation

### **Getting Started**
- 📖 [**START_HERE.md**](START_HERE.md) - Overview and introduction
- ⚡ [**QUICKSTART.md**](QUICKSTART.md) - 3-5 hour setup guide
- 🏭 [**PRODUCTION_DEPLOYMENT.md**](PRODUCTION_DEPLOYMENT.md) - Complete production guide
- ✅ [**PRODUCTION_READINESS.md**](PRODUCTION_READINESS.md) - Deployment checklist

### **Understanding the System**
- 🎭 [**DISPLAY_AND_MODES.md**](DISPLAY_AND_MODES.md) - Demo vs Production modes
- 🏗️ [**backend_scripts/README.md**](backend_scripts/README.md) - Backend architecture

### **Testing & Attacks**
- ⚔️ [**MANUAL_ATTACK_TESTING.md**](MANUAL_ATTACK_TESTING.md) - Manual attack guide
- 📋 [**ATTACK_CHEATSHEET.md**](ATTACK_CHEATSHEET.md) - Quick reference

### **Development**
- 🤝 [**CONTRIBUTING.md**](CONTRIBUTING.md) - Contribution guidelines

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask Dashboard (Web UI)                  │
│                     http://localhost:7000                    │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Suricata   │  │ ANN Engine  │  │ Host Monitor│
│     IDS     │  │  (Neural    │  │ (Isolation  │
│             │  │   Network)  │  │   Forest)   │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │ Hybrid Fusion   │
              │     Engine      │
              │                 │
              │ Final Score =   │
              │ ANN×0.5 +       │
              │ Host×0.3 +      │
              │ Network×0.2     │
              └─────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Alert System   │
              │ Email│Slack│SMS │
              └─────────────────┘
```

### **Detection Layers**

1. **Suricata IDS**: Signature-based detection of known attacks
2. **ANN Engine**: Deep learning model for zero-day detection
3. **Host Monitor**: Behavioral analysis of system processes
4. **Stepping Stone Detector**: Network relay pattern detection
5. **Hybrid Fusion**: Weighted combination of all signals

---

## 💻 Installation

### **Prerequisites**

- **OS**: Linux (Ubuntu 20.04+ / Debian 11+ recommended)
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 50GB+ for logs and models

### **System Dependencies**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Suricata IDS
sudo apt install -y suricata

# Install Python dependencies
pip install -r requirements.txt

# Optional: Attack testing tools
sudo apt install -y nmap hping3 netcat hydra
```

### **Python Dependencies**

```bash
# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

**Key Dependencies:**
- TensorFlow 2.10+
- Flask
- Scikit-learn
- Pandas, NumPy
- psutil

---

## 🎮 Usage

### **Demo Mode** (Testing & Development)

```bash
# Start demo with simulated traffic
python3 demo_mode.py

# Or use the convenience script
./run_demo.sh
```

**Features:**
- No Suricata required
- No ML models needed
- Simulated attack patterns
- Full UI functionality

### **Production Mode** (Real Monitoring)

```bash
# 1. Configure Suricata
sudo nano /etc/suricata/suricata.yaml
# Set interface and enable eve.json logging

# 2. Start Suricata
sudo systemctl start suricata

# 3. Configure application
cp .env.example .env
nano .env  # Set NETWORK_INTERFACE, etc.

# 4. Start application
sudo python3 app.py
```

**Access Dashboard:**
- URL: `http://localhost:7000`
- Click **Start Monitoring** to begin detection
- View live threat logs in real-time

---

## ⚔️ Attack Testing

### **Automated Testing**

```bash
# Run comprehensive attack suite
sudo python3 scripts/attack_simulator.py --mode test

# Measure detection accuracy
python3 scripts/measure_accuracy.py \
    --attack-log attacks_performed.json \
    --detection-log /var/log/backdoor-detection/hybrid_live.log
```

### **Manual Testing**

```bash
# Interactive attack testing
./scripts/quick_attack_test.sh

# Or specific attacks
./scripts/quick_attack_test.sh portscan 127.0.0.1
./scripts/quick_attack_test.sh reverseshell 127.0.0.1
```

**Available Attacks:**
- Port Scanning
- SYN Flood
- Reverse Shell
- SSH Brute Force
- DNS Tunneling
- HTTP Flood

📖 **Full Guide**: See [MANUAL_ATTACK_TESTING.md](MANUAL_ATTACK_TESTING.md)

---

## ⚙️ Configuration

### **Environment Variables** (`.env`)

```bash
# Network Configuration
NETWORK_INTERFACE=eth0
SURICATA_EVE_LOG=/var/log/suricata/eve.json

# Model Paths
MODEL_DIR=./models

# Logging
LOG_DIR=/var/log/backdoor-detection

# Alert Configuration
ALERT_THRESHOLD=0.75
ALERT_COOLDOWN_SECONDS=300

# Email Alerts
ENABLE_EMAIL_ALERTS=true
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
ALERT_EMAIL=security@company.com

# Slack Alerts
ENABLE_SLACK_ALERTS=true
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK

# SMS Alerts (Twilio)
ENABLE_SMS_ALERTS=false
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
```

📖 **Full Configuration**: See `.env.example` for all options

---

## 📁 Project Structure

```
Backdoor-Detection/
├── app.py                          # Main Flask application (Production)
├── demo_mode.py                    # Demo application (Simulated)
├── config.py                       # Centralized configuration
├── requirements.txt                # Python dependencies
│
├── backend_scripts/                # Core detection logic
│   ├── stream_connection.py        # ANN detection engine
│   ├── fusion_engine.py            # Hybrid fusion logic
│   ├── stepping_stone.py           # Network relay detector
│   ├── train_network_model.py      # Model training script
│   ├── train_host_model.py         # Host model training
│   └── hybrid_monitor.py           # Hybrid monitoring
│
├── scripts/                        # Utility scripts
│   ├── collect_network_data.py     # Data collection
│   ├── attack_simulator.py         # Automated attacks
│   ├── measure_accuracy.py         # Accuracy measurement
│   ├── alert_system.py             # Real-time alerting
│   └── quick_attack_test.sh        # Interactive testing
│
├── models/                         # ML model files
│   ├── backdoor_ann_model.h5       # Trained neural network
│   ├── scaler.pkl                  # Feature scaler
│   └── encoders.pkl                # Label encoders
│
├── templates/                      # HTML templates
│   └── index.html                  # Dashboard UI
│
├── static/                         # CSS & JavaScript
│   ├── style.css                   # Dashboard styling
│   └── dashboard.js                # Dashboard logic
│
└── docs/                           # Documentation
    ├── START_HERE.md               # Getting started guide
    ├── QUICKSTART.md               # Quick setup guide
    ├── PRODUCTION_DEPLOYMENT.md    # Production guide
    ├── MANUAL_ATTACK_TESTING.md    # Attack testing guide
    └── ATTACK_CHEATSHEET.md        # Quick reference
```

---

## 🎯 Performance Metrics

### **Expected Detection Rates**

| Attack Type | Detection Rate | Primary Engine |
|-------------|---------------|----------------|
| Port Scanning | 95%+ | Suricata + ANN |
| Reverse Shell | 98%+ | Host + Hybrid |
| SSH Brute Force | 99%+ | Suricata |
| DNS Tunneling | 85%+ | ANN |
| SYN Flood | 90%+ | Suricata + ANN |
| HTTP Flood | 92%+ | Suricata + ANN |

### **System Requirements**

- **Detection Latency**: <3 seconds
- **False Positive Rate**: <5%
- **Accuracy**: >90%
- **Precision**: >85%
- **Recall**: >80%

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### **Quick Contribution Guide**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Suricata**: Open-source IDS/IPS engine
- **TensorFlow**: Machine learning framework
- **CICIDS Dataset**: Training data for ML models
- **MITRE ATT&CK**: Attack technique framework

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/backdoor-detection/issues)
- **Documentation**: See `docs/` directory
- **Security**: Report vulnerabilities via email (not public issues)

---

## ⚠️ Disclaimer

This tool is for **educational and authorized security testing purposes only**. 

- ✅ Use on systems you own or have written permission to test
- ❌ Never use on unauthorized systems
- ❌ Attacking systems without permission is illegal

The authors are not responsible for misuse of this software.

---

## 🗺️ Roadmap

### **Current Version** (v1.0)
- ✅ Multi-layer detection system
- ✅ Real-time dashboard
- ✅ Automated attack testing
- ✅ Multi-channel alerting

### **Planned Features** (v2.0)
- [ ] Distributed deployment support
- [ ] Advanced ML models (Transformer-based)
- [ ] SIEM integration (Splunk, ELK)
- [ ] Automated response actions
- [ ] Custom rule engine
- [ ] Mobile app for alerts
- [ ] Cloud deployment (AWS, Azure, GCP)

---

## 📊 Screenshots

### Dashboard Overview
![Dashboard](https://via.placeholder.com/800x400/1a1a2e/16213e?text=Live+Threat+Dashboard)

### Detection Logs
![Logs](https://via.placeholder.com/800x400/1a1a2e/16213e?text=Real-Time+Detection+Logs)

### Alert System
![Alerts](https://via.placeholder.com/800x400/1a1a2e/16213e?text=Multi-Channel+Alerts)

---

<div align="center">

**Made with ❤️ for Cybersecurity**

[⭐ Star this repo](https://github.com/yourusername/backdoor-detection) | [🐛 Report Bug](https://github.com/yourusername/backdoor-detection/issues) | [💡 Request Feature](https://github.com/yourusername/backdoor-detection/issues)

</div>
