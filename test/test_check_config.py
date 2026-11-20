from check_config import csv_print, CheckAbort
import pytest
def test_csv():
    result = csv_print("test_data/valid_case.csv")
    assert result == []

def test_empty_file():
    with pytest.raises(CheckAbort) as e:
        csv_print("test_data/empty.csv")
    assert e.value.code == 2
