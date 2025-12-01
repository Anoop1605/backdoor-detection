# Backend Scripts

This directory contains the core detection engines and training scripts for the Backdoor Detection System.

## 📁 Files

### Detection Engines
- **`fusion_engine.py`** - Main fusion engine combining ANN, host-based ML, and network-based detection
- **`stepping_stone.py`** - Network relay attack (stepping stone) detector
- **`stream_connection.py`** - Real-time Suricata log streaming and ANN prediction

### Training & Testing
- **`train_host_model.py`** - Trains the Isolation Forest model for host-based anomaly detection
- **`test_integration.py`** - Integration tests for all detection components

### Utilities
- **`hybrid_monitor.py`** - Hybrid monitoring utilities

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Train the Host ML Model
```bash
python3 train_host_model.py
```
**Note:** This takes 60 seconds. Don't run attacks during training!

### 3. Test Everything
```bash
python3 test_integration.py
```

## 📊 Detection Architecture

The fusion engine combines three detection layers:

| Layer | Weight | Method |
|-------|--------|--------|
| ANN | 50% | Neural network traffic analysis |
| Host ML | 30% | Isolation Forest anomaly detection |
| Network | 20% | Stepping stone relay detection |

## 🔧 Configuration

### Stepping Stone Detector
Edit `fusion_engine.py` (line 26):
```python
stepping_stone = SteppingStoneDetector(
    local_network="192.168.0.0/16",  # Your network
    time_threshold=2.0,               # Seconds
    byte_threshold_pct=0.1            # 10% tolerance
)
```

### Detection Weights
Edit `fusion_engine.py` (line 147):
```python
final = (ann * 0.5) + (host * 0.3) + (stepping_stone_score * 0.2)
```

## 📝 Generated Files (Not in Git)

These files are created during training and should NOT be committed:
- `host_iso_forest.pkl` - Trained Isolation Forest model
- `host_scaler.pkl` - Feature scaler for the model

## 📖 Documentation

See [`SETUP_GUIDE.md`](./SETUP_GUIDE.md) for detailed setup instructions and troubleshooting.
