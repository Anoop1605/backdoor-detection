# models/

This directory contains the trained machine learning models for the Backdoor Detection System.

## 📋 Required Files

### **Network Detection Model**
- `backdoor_ann_model.h5` - Trained Keras/TensorFlow neural network
- `scaler.pkl` - StandardScaler for feature normalization
- `scaler_mean.npy` - Scaler mean values (numpy array)
- `scaler_scale.npy` - Scaler scale values (numpy array)
- `encoders.pkl` - Label encoders for categorical features
- `network_dataset.csv` - Column structure reference

### **Host Detection Model** (in backend_scripts/)
- `host_iso_forest.pkl` - Isolation Forest model for anomaly detection
- `host_scaler.pkl` - Scaler for host features

## 🚀 Getting Models

### **Option 1: Train Your Own** (Recommended)

```bash
# 1. Collect or download training data
# Download CICIDS2017 dataset or use data collection script
python3 scripts/collect_network_data.py --duration 1800

# 2. Train network model
python3 backend_scripts/train_network_model.py \
    --dataset data/processed/network_traffic.csv \
    --output models/ \
    --epochs 50

# 3. Train host model
cd backend_scripts
python3 train_host_model.py
```

### **Option 2: Use Pre-trained Models**

Pre-trained models are not included in this repository due to size constraints.

**Download from:**
- [Release Page](https://github.com/yourusername/backdoor-detection/releases)
- [Google Drive](https://drive.google.com/your-link)
- [Hugging Face](https://huggingface.co/your-username/backdoor-detection)

```bash
# Download and extract
wget https://github.com/yourusername/backdoor-detection/releases/download/v1.0/models.tar.gz
tar -xzf models.tar.gz -C models/
```

### **Option 3: Use Dummy Models** (Demo Only)

For testing the UI without real detection:

```bash
python3 create_dummy_model.py
```

**Note:** Dummy models will not provide accurate detection!

## 📊 Model Performance

### **Network ANN Model**
- **Architecture**: 4-layer Dense Neural Network
- **Input Features**: 10 (network flow statistics)
- **Output**: Binary classification (BENIGN/MALICIOUS)
- **Expected Accuracy**: >90%
- **Training Time**: ~30-60 minutes on CPU

### **Host Isolation Forest**
- **Algorithm**: Isolation Forest
- **Features**: 4 (CPU, memory, threads, file descriptors)
- **Contamination**: 0.001 (for clean baseline)
- **Training Time**: ~1 minute

## 🔧 Model Files Size

Typical sizes after training:

```
models/
├── backdoor_ann_model.h5      (~500 KB - 2 MB)
├── scaler.pkl                 (~5 KB)
├── scaler_mean.npy            (~100 bytes)
├── scaler_scale.npy           (~100 bytes)
├── encoders.pkl               (~10 KB)
└── network_dataset.csv        (~1 KB - structure only)

backend_scripts/
├── host_iso_forest.pkl        (~500 KB - 1 MB)
└── host_scaler.pkl            (~5 KB)
```

## ⚠️ Important Notes

1. **Git Ignore**: Model files are excluded from git due to size
2. **Training Required**: You must train models before production use
3. **Dataset Needed**: Training requires labeled network traffic data
4. **Performance**: Model accuracy depends on training data quality

## 📚 Training Data Sources

### **Public Datasets**
- **CICIDS2017**: https://www.unb.ca/cic/datasets/ids-2017.html
- **CICIDS2018**: https://www.unb.ca/cic/datasets/ids-2018.html
- **NSL-KDD**: https://www.unb.ca/cic/datasets/nsl.html
- **UNSW-NB15**: https://research.unsw.edu.au/projects/unsw-nb15-dataset

### **Custom Data Collection**
```bash
# Collect your own data
sudo python3 scripts/collect_network_data.py \
    --interface eth0 \
    --duration 3600 \
    --output data/raw
```

## 🆘 Troubleshooting

### **Missing Model Files**
```bash
# Check if models exist
ls -lh models/

# If missing, train them
python3 backend_scripts/train_network_model.py --dataset your_data.csv
```

### **Model Loading Errors**
```bash
# Verify TensorFlow installation
python3 -c "import tensorflow; print(tensorflow.__version__)"

# Reinstall if needed
pip install tensorflow>=2.10.0
```

### **Low Accuracy**
- Collect more diverse training data
- Balance benign/malicious samples (50/50)
- Increase training epochs
- Review feature engineering

## 📖 More Information

- **Training Guide**: See [PRODUCTION_DEPLOYMENT.md](../PRODUCTION_DEPLOYMENT.md)
- **Quick Start**: See [QUICKSTART.md](../QUICKSTART.md)
- **Backend Details**: See [backend_scripts/README.md](../backend_scripts/README.md)

---

**Note**: This directory should contain your trained models. The `.gitignore` file excludes large model files from version control.
