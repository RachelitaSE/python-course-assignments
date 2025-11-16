# test_cpi_logic.py
import pandas as pd
import datetime
import pytest
from cpi_logic import get_cpi, adjust_cpi

@pytest.fixture
def sample_df():
    data = {
        "date": ["2020-01-01", "2021-01-01"],
        "cpi": [100000, 110000],
    }
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    return df

def test_get_cpi_valid(sample_df):
    value = get_cpi(sample_df, datetime.date(2020, 1, 15))
    assert value == 100000

def test_get_cpi_invalid(sample_df):
    with pytest.raises(ValueError):
        get_cpi(sample_df, datetime.date(2019, 5, 1))

def test_adjust_cpi_increase(sample_df):
    adjusted = adjust_cpi(sample_df, 100000, datetime.date(2020, 1, 1), datetime.date(2021, 1, 1))
    assert adjusted == 110000

def test_adjust_cpi_reverse_dates(sample_df):
    with pytest.raises(ValueError):
        adjust_cpi(sample_df, 100000, datetime.date(2021, 1, 1), datetime.date(2020, 1, 1))
