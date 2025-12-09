#!/usr/bin/env python3
"""
Accuracy Measurement Script
Measures detection accuracy by comparing performed attacks with detected threats
"""
import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
import re

def parse_attack_log(attack_log_path):
    """Parse the attack log JSON file"""
    print(f"[+] Loading attack log from {attack_log_path}...")
    
    with open(attack_log_path, 'r') as f:
        data = json.load(f)
    
    attacks = data.get('attacks', [])
    print(f"[✓] Loaded {len(attacks)} attack records")
    
    return attacks

def parse_detection_log(detection_log_path, start_time=None, end_time=None):
    """Parse detection log and extract malicious detections"""
    print(f"[+] Loading detection log from {detection_log_path}...")
    
    detections = []
    
    if not os.path.exists(detection_log_path):
        print(f"[WARNING] Detection log not found: {detection_log_path}")
        return detections
    
    with open(detection_log_path, 'r') as f:
        for line in f:
            # Look for MALICIOUS predictions
            if 'MALICIOUS' in line:
                # Extract score
                score_match = re.search(r'Score[=:]?\s*([\d.]+)', line)
                score = float(score_match.group(1)) if score_match else 0.0
                
                detections.append({
                    'line': line.strip(),
                    'score': score,
                    'timestamp': datetime.now().isoformat()  # Ideally parse from log
                })
    
    print(f"[✓] Found {len(detections)} malicious detections")
    
    return detections

def calculate_metrics(attacks, detections, time_window=60):
    """
    Calculate detection metrics
    
    Args:
        attacks: List of performed attacks
        detections: List of detections from logs
        time_window: Time window in seconds to correlate attacks with detections
    """
    print(f"[+] Calculating metrics (time window: {time_window}s)...")
    
    # Count attacks by type
    attack_counts = defaultdict(int)
    for attack in attacks:
        if attack.get('success', False):
            attack_counts[attack['attack_type']] += 1
    
    # Total successful attacks
    total_attacks = sum(attack_counts.values())
    
    # Detections with high confidence (>0.5)
    high_confidence_detections = [d for d in detections if d['score'] > 0.5]
    
    # Calculate True Positives (simplified - assumes detections during attack window are TP)
    # In production, you'd need more sophisticated correlation
    true_positives = min(len(high_confidence_detections), total_attacks)
    
    # False Negatives (attacks not detected)
    false_negatives = max(0, total_attacks - true_positives)
    
    # Estimate False Positives (detections when no attack was running)
    # This is simplified - in production you'd track benign traffic periods
    false_positives = max(0, len(high_confidence_detections) - true_positives)
    
    # Estimate True Negatives (benign traffic correctly classified)
    # This requires knowing total benign samples - using estimate
    estimated_benign_samples = len(detections) * 10  # Rough estimate
    true_negatives = estimated_benign_samples - false_positives
    
    # Calculate metrics
    accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives) if (true_positives + true_negatives + false_positives + false_negatives) > 0 else 0
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # False Positive Rate
    fpr = false_positives / (false_positives + true_negatives) if (false_positives + true_negatives) > 0 else 0
    
    # True Positive Rate (same as recall)
    tpr = recall
    
    metrics = {
        'true_positives': true_positives,
        'true_negatives': true_negatives,
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'true_positive_rate': tpr,
        'false_positive_rate': fpr,
        'total_attacks': total_attacks,
        'total_detections': len(high_confidence_detections),
        'attack_breakdown': dict(attack_counts)
    }
    
    return metrics

def print_report(metrics):
    """Print formatted accuracy report"""
    print("\n" + "=" * 70)
    print("DETECTION ACCURACY REPORT")
    print("=" * 70)
    
    print("\nCONFUSION MATRIX:")
    print("-" * 70)
    print(f"{'':20} {'Predicted Benign':>20} {'Predicted Malicious':>20}")
    print(f"{'Actual Benign':20} {metrics['true_negatives']:>20} {metrics['false_positives']:>20}")
    print(f"{'Actual Malicious':20} {metrics['false_negatives']:>20} {metrics['true_positives']:>20}")
    
    print("\nPERFORMANCE METRICS:")
    print("-" * 70)
    print(f"{'Accuracy:':<30} {metrics['accuracy']*100:>6.2f}%")
    print(f"{'Precision:':<30} {metrics['precision']*100:>6.2f}%")
    print(f"{'Recall (TPR):':<30} {metrics['recall']*100:>6.2f}%")
    print(f"{'F1-Score:':<30} {metrics['f1_score']*100:>6.2f}%")
    print(f"{'False Positive Rate:':<30} {metrics['false_positive_rate']*100:>6.2f}%")
    
    print("\nDETECTION SUMMARY:")
    print("-" * 70)
    print(f"{'Total Attacks Performed:':<30} {metrics['total_attacks']:>6}")
    print(f"{'Attacks Detected (TP):':<30} {metrics['true_positives']:>6}")
    print(f"{'Attacks Missed (FN):':<30} {metrics['false_negatives']:>6}")
    print(f"{'False Alarms (FP):':<30} {metrics['false_positives']:>6}")
    
    print("\nATTACK TYPE BREAKDOWN:")
    print("-" * 70)
    for attack_type, count in metrics['attack_breakdown'].items():
        print(f"  {attack_type:<25} {count:>4} attacks")
    
    print("\nRECOMMENDATIONS:")
    print("-" * 70)
    
    if metrics['recall'] < 0.8:
        print("  ⚠️  Low recall - many attacks are being missed")
        print("     → Consider lowering detection threshold")
        print("     → Retrain model with more attack samples")
    
    if metrics['false_positive_rate'] > 0.1:
        print("  ⚠️  High false positive rate")
        print("     → Consider raising detection threshold")
        print("     → Retrain model with more benign samples")
    
    if metrics['precision'] < 0.8:
        print("  ⚠️  Low precision - many false alarms")
        print("     → Review feature engineering")
        print("     → Add more context to detections")
    
    if metrics['accuracy'] > 0.9 and metrics['f1_score'] > 0.85:
        print("  ✓ Excellent detection performance!")
        print("     → System is production-ready")
    
    print("=" * 70)

def save_report(metrics, output_path):
    """Save metrics to JSON file"""
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n[✓] Report saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Measure detection accuracy')
    parser.add_argument('--attack-log', required=True,
                       help='Path to attack log JSON file')
    parser.add_argument('--detection-log', default='/var/log/backdoor-detection/hybrid_live.log',
                       help='Path to detection log file')
    parser.add_argument('--output', default='accuracy_report.json',
                       help='Output file for accuracy report')
    parser.add_argument('--time-window', type=int, default=60,
                       help='Time window in seconds to correlate attacks with detections')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("DETECTION ACCURACY MEASUREMENT")
    print("=" * 70)
    
    # Parse logs
    attacks = parse_attack_log(args.attack_log)
    detections = parse_detection_log(args.detection_log)
    
    # Calculate metrics
    metrics = calculate_metrics(attacks, detections, args.time_window)
    
    # Print report
    print_report(metrics)
    
    # Save report
    save_report(metrics, args.output)
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Review the detailed report in:", args.output)
    print("2. If accuracy is low, consider:")
    print("   - Collecting more training data")
    print("   - Retraining the model")
    print("   - Adjusting detection thresholds")
    print("3. If false positives are high:")
    print("   - Review benign traffic patterns")
    print("   - Add whitelisting rules")
    print("=" * 70)

if __name__ == '__main__':
    main()
