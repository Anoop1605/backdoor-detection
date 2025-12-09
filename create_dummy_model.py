import os
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

# Paths matching your config.py
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

print("Creating placeholder Network Models...")

# 1. Create a dummy Scaler (StandardScaler)
class DummyScaler:
    def transform(self, X): return X
    def fit(self, X): pass
    @property
    def mean_(self): return np.zeros(10) # Matches 10 features in stream_connection.py
    @property
    def scale_(self): return np.ones(10)

joblib.dump(DummyScaler(), os.path.join(MODEL_DIR, "scaler.pkl"))
np.save(os.path.join(MODEL_DIR, "scaler_mean.npy"), np.zeros(10))
np.save(os.path.join(MODEL_DIR, "scaler_scale.npy"), np.ones(10))

# 2. Create a dummy Keras Model
model = Sequential([Dense(1, input_shape=(10,), activation='sigmoid')])
model.compile(optimizer='adam', loss='binary_crossentropy')
model.save(os.path.join(MODEL_DIR, "backdoor_ann_model.h5"))

# 3. Create dummy Encoders
joblib.dump({}, os.path.join(MODEL_DIR, "encoders.pkl"))

# 4. Create dummy CSV for column structure
pd.DataFrame(columns=["src_ip", "dest_ip", "proto", "bytes_toserver", "bytes_toclient", 
                      "pkts_toserver", "pkts_toclient", "flow_age", "src_port", "dest_port"]
            ).to_csv(os.path.join(MODEL_DIR, "network_dataset.csv"), index=False)

print("✅ DONE! You can now run the production app.")