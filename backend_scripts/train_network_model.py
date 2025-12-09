#!/usr/bin/env python3
"""
Network ANN Model Training Script
Trains the neural network for network traffic anomaly detection
"""
import os
import sys
import argparse
import json
import numpy as np
import pandas as pd
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def load_dataset(dataset_path):
    """Load and validate dataset"""
    print(f"[+] Loading dataset from {dataset_path}...")
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    
    df = pd.read_csv(dataset_path)
    print(f"[✓] Loaded {len(df)} samples")
    
    # Check for required columns
    required_cols = ['src_ip', 'dest_ip', 'proto', 'bytes_toserver', 'bytes_toclient',
                     'pkts_toserver', 'pkts_toclient', 'flow_age', 'src_port', 'dest_port']
    
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Check for label column
    if 'alert' not in df.columns and 'label' not in df.columns:
        raise ValueError("Dataset must have 'alert' or 'label' column")
    
    # Standardize label column name
    if 'label' in df.columns and 'alert' not in df.columns:
        df['alert'] = df['label']
    
    return df

def preprocess_data(df):
    """Preprocess and encode features"""
    print("[+] Preprocessing data...")
    
    # Separate features and labels
    X = df.drop(['alert', 'timestamp'], axis=1, errors='ignore')
    y = df['alert']
    
    # Encode categorical features
    encoders = {}
    categorical_cols = ['src_ip', 'dest_ip', 'proto']
    
    for col in categorical_cols:
        if col in X.columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le
    
    # Convert all to numeric
    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)
    
    # Handle infinite values
    X = X.replace([np.inf, -np.inf], 0)
    
    print(f"[✓] Features shape: {X.shape}")
    print(f"[✓] Labels distribution:")
    print(f"    Benign: {(y == 0).sum()} ({(y == 0).sum() / len(y) * 100:.1f}%)")
    print(f"    Malicious: {(y == 1).sum()} ({(y == 1).sum() / len(y) * 100:.1f}%)")
    
    return X, y, encoders

def build_model(input_dim):
    """Build the ANN architecture"""
    print("[+] Building neural network architecture...")
    
    model = Sequential([
        Dense(128, activation='relu', input_shape=(input_dim,)),
        BatchNormalization(),
        Dropout(0.3),
        
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        
        Dense(32, activation='relu'),
        BatchNormalization(),
        Dropout(0.2),
        
        Dense(16, activation='relu'),
        
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', 'AUC']
    )
    
    print("[✓] Model architecture:")
    model.summary()
    
    return model

def train_model(model, X_train, y_train, X_val, y_val, epochs, batch_size, output_dir):
    """Train the model with callbacks"""
    print(f"[+] Training model for {epochs} epochs...")
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            filepath=os.path.join(output_dir, 'best_model.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1
    )
    
    return history

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    print("[+] Evaluating model on test set...")
    
    # Predictions
    y_pred_proba = model.predict(X_test, verbose=0)
    y_pred = (y_pred_proba > 0.5).astype(int).flatten()
    
    # Metrics
    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(classification_report(y_test, y_pred, target_names=['Benign', 'Malicious']))
    
    print("=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)
    cm = confusion_matrix(y_test, y_pred)
    print(f"                Predicted Benign    Predicted Malicious")
    print(f"Actual Benign        {cm[0][0]:6d}              {cm[0][1]:6d}")
    print(f"Actual Malicious     {cm[1][0]:6d}              {cm[1][1]:6d}")
    
    # ROC-AUC
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC-AUC Score: {auc:.4f}")
    
    # Calculate metrics
    tn, fp, fn, tp = cm.ravel()
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    metrics = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'roc_auc': float(auc),
        'true_positives': int(tp),
        'true_negatives': int(tn),
        'false_positives': int(fp),
        'false_negatives': int(fn)
    }
    
    return metrics

def save_artifacts(model, scaler, encoders, X_columns, metrics, output_dir):
    """Save all model artifacts"""
    print(f"[+] Saving model artifacts to {output_dir}...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, 'backdoor_ann_model.h5')
    model.save(model_path)
    print(f"[✓] Model saved: {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(output_dir, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"[✓] Scaler saved: {scaler_path}")
    
    # Save scaler mean and scale as numpy arrays (for compatibility)
    np.save(os.path.join(output_dir, 'scaler_mean.npy'), scaler.mean_)
    np.save(os.path.join(output_dir, 'scaler_scale.npy'), scaler.scale_)
    
    # Save encoders
    encoders_path = os.path.join(output_dir, 'encoders.pkl')
    joblib.dump(encoders, encoders_path)
    print(f"[✓] Encoders saved: {encoders_path}")
    
    # Save column structure
    df_columns = pd.DataFrame(columns=list(X_columns) + ['alert'])
    csv_path = os.path.join(output_dir, 'network_dataset.csv')
    df_columns.to_csv(csv_path, index=False)
    print(f"[✓] Column structure saved: {csv_path}")
    
    # Save training report
    report = {
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics,
        'model_architecture': {
            'layers': len(model.layers),
            'parameters': model.count_params()
        },
        'features': list(X_columns)
    }
    
    report_path = os.path.join(output_dir, 'training_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"[✓] Training report saved: {report_path}")

def main():
    parser = argparse.ArgumentParser(description='Train network anomaly detection model')
    parser.add_argument('--dataset', required=True, help='Path to training dataset CSV')
    parser.add_argument('--output', default='models/', help='Output directory for model artifacts')
    parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=128, help='Batch size')
    parser.add_argument('--test-split', type=float, default=0.2, help='Test set ratio')
    parser.add_argument('--val-split', type=float, default=0.1, help='Validation set ratio')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Network Anomaly Detection Model Training")
    print("=" * 60)
    print(f"Dataset: {args.dataset}")
    print(f"Output: {args.output}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch Size: {args.batch_size}")
    print("=" * 60)
    
    # Load dataset
    df = load_dataset(args.dataset)
    
    # Preprocess
    X, y, encoders = preprocess_data(df)
    
    # Split data
    print(f"[+] Splitting data (test={args.test_split}, val={args.val_split})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_split, random_state=42, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=args.val_split, random_state=42, stratify=y_train
    )
    
    print(f"[✓] Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    # Scale features
    print("[+] Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Build model
    model = build_model(X_train_scaled.shape[1])
    
    # Train model
    history = train_model(
        model, X_train_scaled, y_train,
        X_val_scaled, y_val,
        args.epochs, args.batch_size, args.output
    )
    
    # Evaluate
    metrics = evaluate_model(model, X_test_scaled, y_test)
    
    # Save artifacts
    save_artifacts(model, scaler, encoders, X.columns, metrics, args.output)
    
    print("\n" + "=" * 60)
    print("✓ TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Model Accuracy: {metrics['accuracy'] * 100:.2f}%")
    print(f"Precision: {metrics['precision'] * 100:.2f}%")
    print(f"Recall: {metrics['recall'] * 100:.2f}%")
    print(f"F1-Score: {metrics['f1_score'] * 100:.2f}%")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the training report in models/training_report.json")
    print("2. Test the model: python3 backend_scripts/test_integration.py")
    print("3. Deploy to production: sudo python3 app.py")

if __name__ == '__main__':
    main()
