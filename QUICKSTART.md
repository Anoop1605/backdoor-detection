# Quick Start Guide: Demo to Production

This guide provides a **step-by-step workflow** to transition from demo mode to a production-ready backdoor detection system.

---

## 🎯 Overview

You currently have a **working demo system**. To make it production-ready, you need to:

1. ✅ **Train real ML models** (instead of dummy models)
2. ✅ **Deploy with real network monitoring** (Suricata)
3. ✅ **Test detection accuracy** with simulated attacks
4. ✅ **Enable real-time alerts** (email, Slack, SMS, etc.)

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Ubuntu/Debian Linux system
- [ ] Root/sudo access
- [ ] Python 3.8+ installed
- [ ] At least 8GB RAM
- [ ] 50GB+ free disk space
- [ ] Network interface for monitoring (e.g., `eth0`)

---

## 🚀 Step-by-Step Workflow

### **Step 1: Install System Dependencies** (15 minutes)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Suricata IDS
sudo apt install -y suricata

# Install network tools (for testing)
sudo apt install -y nmap hping3 netcat

# Install Python dependencies
source .venv/bin/activate  # If using virtual environment
pip install -r requirements.txt
```

**Verify Installation:**
```bash
suricata --version
python3 -c "import tensorflow; print(tensorflow.__version__)"
```

---

### **Step 2: Configure Suricata** (10 minutes)

```bash
# Edit Suricata configuration
sudo nano /etc/suricata/suricata.yaml
```

**Key changes:**
- Set `af-packet: - interface: eth0` (replace `eth0` with your interface)
- Ensure `eve-log: enabled: yes`
- Set `filename: /var/log/suricata/eve.json`

**Update rules and start Suricata:**
```bash
# Update Suricata rules
sudo suricata-update

# Start Suricata
sudo systemctl start suricata
sudo systemctl enable suricata

# Verify it's running
sudo systemctl status suricata
sudo tail -f /var/log/suricata/eve.json
```

---

### **Step 3: Collect Training Data** (1-3 hours)

You have **two options** for getting training data:

#### **Option A: Use Public Dataset** (Recommended - Faster)

```bash
# Create data directory
mkdir -p data/raw

# Download CICIDS2017 or similar dataset
# Example: https://www.unb.ca/cic/datasets/ids-2017.html
# Follow dataset-specific instructions

# Once downloaded, convert to required format
python3 scripts/convert_dataset.py \
    --input data/raw/cicids2017.csv \
    --output data/processed/network_traffic.csv
```

#### **Option B: Collect Your Own Data**

**Collect Benign Traffic (30 minutes):**
```bash
# Run during normal network usage
sudo python3 scripts/collect_network_data.py \
    --interface eth0 \
    --duration 1800 \
    --output data/raw \
    --label benign
```

**Collect Malicious Traffic (30 minutes):**
```bash
# Run while performing attacks in a controlled environment
sudo python3 scripts/collect_network_data.py \
    --interface eth0 \
    --duration 1800 \
    --output data/raw \
    --label malicious
```

**Combine datasets:**
```bash
# Merge all collected CSV files
python3 scripts/merge_datasets.py \
    --input data/raw/*.csv \
    --output data/processed/network_traffic.csv
```

---

### **Step 4: Train the Models** (30-60 minutes)

#### **Train Network ANN Model:**

```bash
python3 backend_scripts/train_network_model.py \
    --dataset data/processed/network_traffic.csv \
    --output models/ \
    --epochs 50 \
    --batch-size 128
```

**Expected Output:**
```
✓ Model Accuracy: 95%+
✓ Precision: 90%+
✓ Recall: 88%+
✓ Files created:
  - models/backdoor_ann_model.h5
  - models/scaler.pkl
  - models/encoders.pkl
  - models/training_report.json
```

#### **Train Host-Based Model:**

```bash
# Run during normal system operation (no attacks)
cd backend_scripts
python3 train_host_model.py
```

**Expected Output:**
```
✓ Model saved to host_iso_forest.pkl
✓ Scaler saved to host_scaler.pkl
```

---

### **Step 5: Test the System** (15 minutes)

```bash
# Test model integration
python3 backend_scripts/test_integration.py

# Expected output:
# ✓ Model loaded successfully
# ✓ Scaler loaded successfully
# ✓ Test predictions working
```

---

### **Step 6: Deploy Production System** (10 minutes)

```bash
# Copy environment configuration
cp .env.example .env

# Edit configuration
nano .env
```

**Minimal required settings:**
```bash
NETWORK_INTERFACE=eth0  # Your interface
SURICATA_EVE_LOG=/var/log/suricata/eve.json
LOG_DIR=/var/log/backdoor-detection
```

**Create log directory:**
```bash
sudo mkdir -p /var/log/backdoor-detection
sudo chown $USER:$USER /var/log/backdoor-detection
```

**Start the application:**
```bash
sudo python3 app.py
```

**Access dashboard:**
- Open browser: `http://localhost:7000`
- Click **Start Monitoring**
- Verify all three engines are running

---

### **Step 7: Test Detection Accuracy** (30 minutes)

**⚠️ IMPORTANT:** Only run attacks in a controlled environment or against your own systems!

```bash
# Run attack simulation suite
sudo python3 scripts/attack_simulator.py \
    --target 127.0.0.1 \
    --mode test \
    --duration 10 \
    --delay 5
```

**Measure accuracy:**
```bash
# Wait a few minutes for detections to process
sleep 120

# Measure accuracy
python3 scripts/measure_accuracy.py \
    --attack-log attacks_performed.json \
    --detection-log /var/log/backdoor-detection/hybrid_live.log \
    --output accuracy_report.json
```

**Review results:**
```bash
cat accuracy_report.json
```

**Target Metrics:**
- Accuracy: >90%
- Precision: >85%
- Recall: >80%
- F1-Score: >85%

---

### **Step 8: Configure Alerts** (15 minutes)

Edit `.env` and enable your preferred alert channels:

#### **Email Alerts:**
```bash
ENABLE_EMAIL_ALERTS=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Use app-specific password
ALERT_EMAIL=security@yourcompany.com
```

#### **Slack Alerts:**
```bash
ENABLE_SLACK_ALERTS=true
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**Start alert system:**
```bash
python3 scripts/alert_system.py --log-file /var/log/backdoor-detection/hybrid_live.log &
```

**Test alerts:**
```bash
python3 scripts/alert_system.py --test
```

---

### **Step 9: Production Hardening** (30 minutes)

#### **Create systemd service:**

```bash
sudo nano /etc/systemd/system/backdoor-detection.service
```

**Service file:**
```ini
[Unit]
Description=Backdoor Detection System
After=network.target suricata.service

[Service]
Type=simple
User=root
WorkingDirectory=/home/ubuntu/Desktop/Backdoor-Detection
Environment="PATH=/home/ubuntu/Desktop/Backdoor-Detection/.venv/bin"
ExecStart=/home/ubuntu/Desktop/Backdoor-Detection/.venv/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable backdoor-detection
sudo systemctl start backdoor-detection
sudo systemctl status backdoor-detection
```

#### **Setup log rotation:**

```bash
sudo nano /etc/logrotate.d/backdoor-detection
```

```
/var/log/backdoor-detection/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
}
```

---

## ✅ Verification Checklist

After completing all steps, verify:

- [ ] Suricata is running: `sudo systemctl status suricata`
- [ ] Models are trained and in `models/` directory
- [ ] Dashboard is accessible at `http://localhost:7000`
- [ ] All three detection engines show "Running" status
- [ ] Detection logs are being written to `/var/log/backdoor-detection/`
- [ ] Alerts are configured and tested
- [ ] System service is enabled and running

---

## 📊 Expected Timeline

| Phase | Time Required |
|-------|--------------|
| Install dependencies | 15 minutes |
| Configure Suricata | 10 minutes |
| Collect/download data | 1-3 hours |
| Train models | 30-60 minutes |
| Deploy system | 10 minutes |
| Test accuracy | 30 minutes |
| Configure alerts | 15 minutes |
| Production hardening | 30 minutes |
| **Total** | **3-5 hours** |

---

## 🆘 Troubleshooting

### Issue: "No module named 'tensorflow'"
```bash
pip install tensorflow>=2.10.0
```

### Issue: "Suricata eve.json not found"
```bash
sudo systemctl start suricata
sudo tail -f /var/log/suricata/eve.json
```

### Issue: "Low detection accuracy"
- Collect more training data
- Retrain with balanced dataset (50% benign, 50% malicious)
- Adjust detection threshold in `.env`

### Issue: "Too many false positives"
- Increase `ALERT_THRESHOLD` in `.env`
- Retrain with more benign samples
- Review and whitelist known-good IPs

---

## 📚 Next Steps

Once your system is running:

1. **Monitor daily**: Check logs and dashboard regularly
2. **Review alerts**: Investigate all high-severity alerts
3. **Tune thresholds**: Adjust based on false positive/negative rates
4. **Retrain monthly**: Update models with new data
5. **Update rules**: Keep Suricata rules current

---

## 📖 Additional Resources

- **Full Deployment Guide**: [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)
- **Display & Modes**: [DISPLAY_AND_MODES.md](DISPLAY_AND_MODES.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **README**: [README.md](README.md)

---

## 🎓 Training Resources

- **Suricata**: https://suricata.readthedocs.io/
- **TensorFlow**: https://www.tensorflow.org/tutorials
- **CICIDS Dataset**: https://www.unb.ca/cic/datasets/
- **MITRE ATT&CK**: https://attack.mitre.org/

---

**Need Help?** Check the troubleshooting section in [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) or open an issue on GitHub.
