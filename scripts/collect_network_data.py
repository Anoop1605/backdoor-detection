#!/usr/bin/env python3
"""
Network Traffic Data Collection Script
Captures real network traffic and labels it for model training
"""
import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
import pandas as pd

def collect_traffic(interface, duration, output_dir):
    """
    Collect network traffic using Suricata
    
    Args:
        interface: Network interface to monitor
        duration: Collection duration in seconds
        output_dir: Directory to save collected data
    """
    print(f"[+] Starting traffic collection on {interface} for {duration} seconds...")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Temporary EVE log file
    eve_log = os.path.join(output_dir, f"eve_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    # Start Suricata
    print(f"[+] Starting Suricata (logging to {eve_log})...")
    suricata_cmd = [
        "sudo", "suricata",
        "-i", interface,
        "--af-packet",
        "-l", output_dir
    ]
    
    proc = subprocess.Popen(
        suricata_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"[+] Collecting traffic for {duration} seconds...")
    print("[!] During this time:")
    print("    - Browse normally for BENIGN traffic")
    print("    - Or run attacks for MALICIOUS traffic")
    
    # Wait for collection period
    time.sleep(duration)
    
    # Stop Suricata
    print("[+] Stopping Suricata...")
    proc.terminate()
    proc.wait(timeout=10)
    
    # Parse collected data
    print("[+] Parsing collected events...")
    events = []
    
    eve_path = os.path.join(output_dir, "eve.json")
    if os.path.exists(eve_path):
        with open(eve_path, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    if event.get('event_type') in ['flow', 'alert']:
                        events.append(event)
                except json.JSONDecodeError:
                    continue
    
    print(f"[+] Collected {len(events)} network events")
    
    # Convert to DataFrame
    rows = []
    for event in events:
        flow = event.get('flow', {})
        
        row = {
            'timestamp': event.get('timestamp', ''),
            'src_ip': event.get('src_ip', ''),
            'src_port': event.get('src_port', 0),
            'dest_ip': event.get('dest_ip', ''),
            'dest_port': event.get('dest_port', 0),
            'proto': event.get('proto', flow.get('proto', '')),
            'pkts_toserver': flow.get('pkts_toserver', 0),
            'pkts_toclient': flow.get('pkts_toclient', 0),
            'bytes_toserver': flow.get('bytes_toserver', 0),
            'bytes_toclient': flow.get('bytes_toclient', 0),
            'flow_age': flow.get('age', 0),
            'alert': 1 if event.get('event_type') == 'alert' else 0
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Save to CSV
    output_csv = os.path.join(output_dir, f"traffic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    df.to_csv(output_csv, index=False)
    
    print(f"[✓] Data saved to {output_csv}")
    print(f"[✓] Total samples: {len(df)}")
    print(f"[✓] Malicious samples: {df['alert'].sum()}")
    print(f"[✓] Benign samples: {len(df) - df['alert'].sum()}")
    
    return output_csv

def main():
    parser = argparse.ArgumentParser(description='Collect network traffic data for model training')
    parser.add_argument('--interface', default='eth0', help='Network interface to monitor')
    parser.add_argument('--duration', type=int, default=300, help='Collection duration in seconds')
    parser.add_argument('--output', default='data/raw', help='Output directory')
    parser.add_argument('--label', choices=['benign', 'malicious', 'mixed'], default='mixed',
                       help='Label for this collection session')
    
    args = parser.parse_args()
    
    # Check if running as root
    if os.geteuid() != 0:
        print("[ERROR] This script requires root privileges (sudo)")
        sys.exit(1)
    
    print("=" * 60)
    print("Network Traffic Data Collection")
    print("=" * 60)
    print(f"Interface: {args.interface}")
    print(f"Duration: {args.duration} seconds")
    print(f"Label: {args.label}")
    print("=" * 60)
    
    # Collect traffic
    output_file = collect_traffic(args.interface, args.duration, args.output)
    
    print("\n[✓] Collection complete!")
    print(f"\nNext steps:")
    print(f"1. Review the data: {output_file}")
    print(f"2. Combine multiple collection sessions")
    print(f"3. Train the model: python3 backend_scripts/train_network_model.py")

if __name__ == '__main__':
    main()
