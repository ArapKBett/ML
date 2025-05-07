import pytest
import numpy as np
from src.models.lstm_model import LSTMModel

@pytest.fixture
def lstm_model():
    return LSTMModel(look_back=10)

def test_build_model(lstm_model):
    lstm_model.build_model()
    assert lstm_model.model is not None
    assert len(lstm_model.model.layers) > 0

def test_train_predict(lstm_model):
    X_train = np.random.rand(100, 10, 1)
    y_train = np.random.rand(100)
    X_test = np.random.rand(20, 10, 1)
    lstm_model.build_model()
    lstm_model.train(X_train, y_train, epochs=1)
    predictions = lstm_model.predict(X_test)
    assert predictions.shape[0] == 20
