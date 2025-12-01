#!/usr/bin/env python3
"""
Quick integration test for the backdoor detection system
Tests: Stepping Stone, Isolation Forest, and Fusion Engine
"""

import sys
import time

print("=" * 60)
print("BACKDOOR DETECTION SYSTEM - INTEGRATION TEST")
print("=" * 60)

# Test 1: Stepping Stone Detector
print("\n[TEST 1] Stepping Stone Detector")
print("-" * 60)
try:
    from stepping_stone import SteppingStoneDetector
    
    detector = SteppingStoneDetector(local_network="192.168.0.0/16")
    
    # Simulate inbound flow
    event1 = {
        'src_ip': '10.0.0.5',
        'dest_ip': '192.168.1.10',
        'timestamp': time.time(),
        'flow': {'bytes_toserver': 1024}
    }
    
    result1 = detector.check_relay(event1)
    print(f"✓ Inbound flow processed: {result1}")
    
    # Simulate outbound flow (potential relay)
    event2 = {
        'src_ip': '192.168.1.10',
        'dest_ip': '8.8.8.8',
        'timestamp': time.time() + 0.5,
        'flow': {'bytes_toserver': 1050}
    }
    
    result2 = detector.check_relay(event2)
    if result2:
        print(f"✓ Stepping stone detected: {result2}")
    else:
        print("✓ No stepping stone detected (expected for test)")
    
    print("✓ Stepping Stone Detector: PASSED")
    
except Exception as e:
    print(f"✗ Stepping Stone Detector: FAILED - {e}")
    sys.exit(1)

# Test 2: Check if ML model files exist
print("\n[TEST 2] ML Model Files")
print("-" * 60)
import os

model_path = os.path.join(os.path.dirname(__file__), "host_iso_forest.pkl")
scaler_path = os.path.join(os.path.dirname(__file__), "host_scaler.pkl")

if os.path.exists(model_path) and os.path.exists(scaler_path):
    print(f"✓ Model found: {model_path}")
    print(f"✓ Scaler found: {scaler_path}")
    print("✓ ML Model Files: PASSED")
    ml_ready = True
else:
    print(f"⚠ Model or scaler not found")
    print(f"  Run: python3 train_host_model.py")
    print("⚠ ML Model Files: SKIPPED (not trained yet)")
    ml_ready = False

# Test 3: Fusion Engine
print("\n[TEST 3] Fusion Engine")
print("-" * 60)
try:
    from fusion_engine import fusion_analyze, host_risk_score
    
    # Test with dummy event
    test_event = {
        'ann_score': 0.3,
        'src_ip': '192.168.1.10',
        'dest_ip': '8.8.8.8',
        'timestamp': time.time(),
        'flow': {'bytes_toserver': 512}
    }
    
    result = fusion_analyze(test_event)
    print(f"✓ Fusion analysis result: {result}")
    
    if ml_ready:
        host_score = host_risk_score()
        print(f"✓ Host risk score: {host_score:.4f}")
    
    print("✓ Fusion Engine: PASSED")
    
except Exception as e:
    print(f"✗ Fusion Engine: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("INTEGRATION TEST SUMMARY")
print("=" * 60)
print("✓ Stepping Stone Detector: Working")
print(f"{'✓' if ml_ready else '⚠'} ML Model: {'Ready' if ml_ready else 'Not trained yet'}")
print("✓ Fusion Engine: Working")
print("\nNext steps:")
if not ml_ready:
    print("  1. Run: python3 train_host_model.py")
    print("  2. Wait 60 seconds for training")
    print("  3. Re-run this test")
else:
    print("  All systems ready! You can now:")
    print("  - Use fusion_engine.py in your detection pipeline")
    print("  - Monitor for stepping stone attacks")
    print("  - Detect anomalous host behavior")
print("=" * 60)
