import pickle
import numpy as np
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor

MODEL_ID = "fcb6f3bf-cd24-4258-bf01-b58b3ccff7fe"
MODEL_PATH = Path().resolve()/"models"/f"{MODEL_ID}/{MODEL_ID}.pkl"

def load_model():
    with open(MODEL_PATH, 'rb') as rf:
        model = pickle.load(rf)
    return model
