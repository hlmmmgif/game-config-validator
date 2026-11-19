from check_config import csv_print
def test_csv():
    result = csv_print("test_data/valid_case.csv")
    assert result == []

def test_empty_file():
    csv_print("test_data/empty.csv")
