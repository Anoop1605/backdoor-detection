#!/usr/bin/env python3
"""
Demo Data Generator - Simulates network traffic events for demonstration
Generates realistic network flow events without requiring Suricata
"""
import json
import time
import random
from datetime import datetime

# Demo event templates
BENIGN_EVENTS = [
    {"src_ip": "192.168.1.100", "dest_ip": "8.8.8.8", "dest_port": 53, "proto": "UDP", "event_type": "dns"},
    {"src_ip": "192.168.1.100", "dest_ip": "142.250.185.46", "dest_port": 443, "proto": "TCP", "event_type": "tls"},
    {"src_ip": "192.168.1.100", "dest_ip": "151.101.1.140", "dest_port": 443, "proto": "TCP", "event_type": "http"},
    {"src_ip": "192.168.1.50", "dest_ip": "192.168.1.1", "dest_port": 80, "proto": "TCP", "event_type": "flow"},
]

MALICIOUS_EVENTS = [
    {"src_ip": "10.0.0.50", "dest_ip": "192.168.1.100", "dest_port": 4444, "proto": "TCP", "event_type": "alert", "alert": {"signature": "Reverse Shell Detected"}},
    {"src_ip": "192.168.1.100", "dest_ip": "185.220.101.50", "dest_port": 9050, "proto": "TCP", "event_type": "alert", "alert": {"signature": "TOR Connection"}},
    {"src_ip": "10.0.0.99", "dest_ip": "192.168.1.100", "dest_port": 22, "proto": "TCP", "event_type": "alert", "alert": {"signature": "SSH Brute Force"}},
    {"src_ip": "192.168.1.100", "dest_ip": "45.33.32.156", "dest_port": 8080, "proto": "TCP", "event_type": "alert", "alert": {"signature": "Data Exfiltration"}},
]

def generate_event(is_malicious=False):
    """Generate a single network event"""
    template = random.choice(MALICIOUS_EVENTS if is_malicious else BENIGN_EVENTS)
    
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "src_ip": template["src_ip"],
        "src_port": random.randint(1024, 65535),
        "dest_ip": template["dest_ip"],
        "dest_port": template["dest_port"],
        "proto": template["proto"],
        "event_type": template["event_type"],
        "flow": {
            "pkts_toserver": random.randint(5, 100),
            "pkts_toclient": random.randint(5, 100),
            "bytes_toserver": random.randint(500, 50000),
            "bytes_toclient": random.randint(500, 50000),
            "age": random.randint(1, 300)
        }
    }
    
    # Add alert info if malicious
    if is_malicious and "alert" in template:
        event["alert"] = template["alert"]
    
    return event

def run_generator(output_file, events_per_second=2, malicious_ratio=0.2):
    """
    Continuously generate demo events
    
    Args:
        output_file: Path to write events
        events_per_second: Rate of event generation
        malicious_ratio: Probability of generating malicious events (0.0-1.0)
    """
    print(f"[DEMO] Starting data generator...")
    print(f"[DEMO] Writing to: {output_file}")
    print(f"[DEMO] Rate: {events_per_second} events/sec, {malicious_ratio*100}% malicious")
    
    with open(output_file, "w") as f:
        event_count = 0
        while True:
            # Decide if this event should be malicious
            is_malicious = random.random() < malicious_ratio
            
            # Generate and write event
            event = generate_event(is_malicious)
            f.write(json.dumps(event) + "\n")
            f.flush()
            
            event_count += 1
            if event_count % 10 == 0:
                print(f"[DEMO] Generated {event_count} events ({int(event_count * malicious_ratio)} malicious)")
            
            # Sleep to maintain desired rate
            time.sleep(1.0 / events_per_second)

if __name__ == "__main__":
    import sys
    
    output_file = sys.argv[1] if len(sys.argv) > 1 else "/tmp/demo_eve.json"
    
    try:
        run_generator(output_file)
    except KeyboardInterrupt:
        print("\n[DEMO] Generator stopped")
