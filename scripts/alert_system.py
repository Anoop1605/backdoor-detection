#!/usr/bin/env python3
"""
Real-Time Alert System
Sends alerts via multiple channels when threats are detected
"""
import os
import sys
import json
import time
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class AlertManager:
    def __init__(self):
        self.alert_threshold = float(os.getenv('ALERT_THRESHOLD', '0.75'))
        self.cooldown_seconds = int(os.getenv('ALERT_COOLDOWN_SECONDS', '300'))
        self.last_alert_time = defaultdict(float)
        
        # Alert channel configuration
        self.email_enabled = os.getenv('ENABLE_EMAIL_ALERTS', 'false').lower() == 'true'
        self.slack_enabled = os.getenv('ENABLE_SLACK_ALERTS', 'false').lower() == 'true'
        self.sms_enabled = os.getenv('ENABLE_SMS_ALERTS', 'false').lower() == 'true'
        self.webhook_enabled = os.getenv('ENABLE_WEBHOOK_ALERTS', 'false').lower() == 'true'
        
        print("[+] Alert Manager initialized")
        print(f"    Threshold: {self.alert_threshold}")
        print(f"    Cooldown: {self.cooldown_seconds}s")
        print(f"    Email: {'✓' if self.email_enabled else '✗'}")
        print(f"    Slack: {'✓' if self.slack_enabled else '✗'}")
        print(f"    SMS: {'✓' if self.sms_enabled else '✗'}")
        print(f"    Webhook: {'✓' if self.webhook_enabled else '✗'}")
    
    def should_alert(self, alert_key):
        """Check if enough time has passed since last alert of this type"""
        current_time = time.time()
        last_time = self.last_alert_time.get(alert_key, 0)
        
        if current_time - last_time >= self.cooldown_seconds:
            self.last_alert_time[alert_key] = current_time
            return True
        
        return False
    
    def get_severity(self, score):
        """Determine alert severity based on score"""
        if score >= 0.9:
            return 'CRITICAL'
        elif score >= 0.75:
            return 'HIGH'
        elif score >= 0.6:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def send_email_alert(self, subject, body):
        """Send email alert via SMTP"""
        if not self.email_enabled:
            return False
        
        try:
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_username = os.getenv('SMTP_USERNAME', '')
            smtp_password = os.getenv('SMTP_PASSWORD', '')
            alert_email = os.getenv('ALERT_EMAIL', '')
            
            if not all([smtp_username, smtp_password, alert_email]):
                print("[!] Email configuration incomplete")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = alert_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
            
            print(f"[✓] Email alert sent to {alert_email}")
            return True
            
        except Exception as e:
            print(f"[!] Email alert failed: {e}")
            return False
    
    def send_slack_alert(self, message):
        """Send alert to Slack via webhook"""
        if not self.slack_enabled:
            return False
        
        try:
            webhook_url = os.getenv('SLACK_WEBHOOK_URL', '')
            
            if not webhook_url:
                print("[!] Slack webhook URL not configured")
                return False
            
            payload = {
                'text': message,
                'username': 'Backdoor Detection System',
                'icon_emoji': ':shield:'
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("[✓] Slack alert sent")
                return True
            else:
                print(f"[!] Slack alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[!] Slack alert failed: {e}")
            return False
    
    def send_sms_alert(self, message):
        """Send SMS alert via Twilio"""
        if not self.sms_enabled:
            return False
        
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
            from_number = os.getenv('TWILIO_FROM_NUMBER', '')
            to_number = os.getenv('TWILIO_TO_NUMBER', '')
            
            if not all([account_sid, auth_token, from_number, to_number]):
                print("[!] Twilio configuration incomplete")
                return False
            
            client = Client(account_sid, auth_token)
            
            message = client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            
            print(f"[✓] SMS alert sent (SID: {message.sid})")
            return True
            
        except ImportError:
            print("[!] Twilio library not installed: pip install twilio")
            return False
        except Exception as e:
            print(f"[!] SMS alert failed: {e}")
            return False
    
    def send_webhook_alert(self, data):
        """Send alert to custom webhook"""
        if not self.webhook_enabled:
            return False
        
        try:
            webhook_url = os.getenv('WEBHOOK_URL', '')
            auth_token = os.getenv('WEBHOOK_AUTH_TOKEN', '')
            
            if not webhook_url:
                print("[!] Webhook URL not configured")
                return False
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            if auth_token:
                headers['Authorization'] = f'Bearer {auth_token}'
            
            response = requests.post(
                webhook_url,
                json=data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201, 202]:
                print(f"[✓] Webhook alert sent")
                return True
            else:
                print(f"[!] Webhook alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[!] Webhook alert failed: {e}")
            return False
    
    def send_alert(self, detection_data):
        """
        Send alert through all enabled channels
        
        Args:
            detection_data: Dictionary with detection information
        """
        score = detection_data.get('score', 0)
        attack_type = detection_data.get('attack_type', 'Unknown')
        source_ip = detection_data.get('source_ip', 'Unknown')
        timestamp = detection_data.get('timestamp', datetime.now().isoformat())
        
        # Check if score meets threshold
        if score < self.alert_threshold:
            return
        
        # Check cooldown
        alert_key = f"{attack_type}_{source_ip}"
        if not self.should_alert(alert_key):
            print(f"[!] Alert suppressed (cooldown): {alert_key}")
            return
        
        # Determine severity
        severity = self.get_severity(score)
        
        # Format alert message
        subject = f"[{severity}] Backdoor Detection Alert"
        
        message = f"""
🚨 SECURITY ALERT 🚨

Severity: {severity}
Confidence Score: {score:.2%}
Attack Type: {attack_type}
Source IP: {source_ip}
Timestamp: {timestamp}

A potential security threat has been detected by the Backdoor Detection System.
Please investigate immediately.

---
Backdoor Detection System
        """.strip()
        
        # Webhook data
        webhook_data = {
            'severity': severity,
            'score': score,
            'attack_type': attack_type,
            'source_ip': source_ip,
            'timestamp': timestamp,
            'system': 'Backdoor Detection System'
        }
        
        # Send through all enabled channels
        print(f"\n[!] ALERT: {severity} - Score: {score:.2%} - {attack_type}")
        
        if self.email_enabled:
            self.send_email_alert(subject, message)
        
        if self.slack_enabled:
            self.send_slack_alert(message)
        
        if self.sms_enabled:
            # Shorter message for SMS
            sms_message = f"[{severity}] Backdoor Detection: {attack_type} from {source_ip} (Score: {score:.0%})"
            self.send_sms_alert(sms_message)
        
        if self.webhook_enabled:
            self.send_webhook_alert(webhook_data)

def monitor_log_file(log_file, alert_manager):
    """Monitor log file for malicious detections and send alerts"""
    print(f"[+] Monitoring log file: {log_file}")
    
    # Wait for log file to exist
    while not os.path.exists(log_file):
        print(f"[!] Waiting for log file to be created...")
        time.sleep(5)
    
    with open(log_file, 'r') as f:
        # Start from end of file
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            
            if not line:
                time.sleep(0.5)
                continue
            
            # Parse detection
            if 'MALICIOUS' in line:
                try:
                    # Extract score
                    import re
                    score_match = re.search(r'Score[=:]?\s*([\d.]+)', line)
                    score = float(score_match.group(1)) if score_match else 0.0
                    
                    # Extract source IP if available
                    ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
                    source_ip = ip_match.group(0) if ip_match else 'Unknown'
                    
                    # Determine attack type from context
                    attack_type = 'Network Anomaly'
                    if 'HYBRID' in line:
                        attack_type = 'Hybrid Detection'
                    elif 'ANN' in line:
                        attack_type = 'ANN Detection'
                    
                    # Send alert
                    detection_data = {
                        'score': score,
                        'attack_type': attack_type,
                        'source_ip': source_ip,
                        'timestamp': datetime.now().isoformat(),
                        'raw_log': line.strip()
                    }
                    
                    alert_manager.send_alert(detection_data)
                    
                except Exception as e:
                    print(f"[!] Error processing detection: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Real-time alert system')
    parser.add_argument('--log-file', default='/var/log/backdoor-detection/hybrid_live.log',
                       help='Log file to monitor')
    parser.add_argument('--test', action='store_true',
                       help='Send test alert and exit')
    
    args = parser.parse_args()
    
    # Initialize alert manager
    alert_manager = AlertManager()
    
    if args.test:
        print("\n[+] Sending test alert...")
        test_data = {
            'score': 0.95,
            'attack_type': 'Test Alert',
            'source_ip': '192.168.1.100',
            'timestamp': datetime.now().isoformat()
        }
        alert_manager.send_alert(test_data)
        print("[✓] Test complete")
        return
    
    # Monitor log file
    print("=" * 60)
    print("REAL-TIME ALERT SYSTEM")
    print("=" * 60)
    
    try:
        monitor_log_file(args.log_file, alert_manager)
    except KeyboardInterrupt:
        print("\n[!] Alert system stopped")

if __name__ == '__main__':
    main()
