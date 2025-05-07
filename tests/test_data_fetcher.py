import pytest
import pandas as pd
from src.data.data_fetcher import DataFetcher

@pytest.fixture
def data_fetcher():
    return DataFetcher("AAPL")

def test_fetch_data(data_fetcher):
    start_date = "2023-01-01"
    end_date = "2025-04-30"
    df = data_fetcher.fetch_data(start_date, end_date)
    assert isinstance(df, pd.DataFrame)
    assert 'Close' in df.columns
    assert not df.empty

def test_preprocess_data(data_fetcher):
    df = pd.DataFrame({'Close': range(100)})
    X_train, y_train, X_test, y_test, scaled_data = data_fetcher.preprocess_data(df, look_back=10)
    assert X_train.shape[1] == 10
    assert X_train.shape[2] == 1
    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)
