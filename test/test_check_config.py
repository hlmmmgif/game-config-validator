from check_config import csv_print, CheckAbort
import pytest

def test_csv():
    result = csv_print("test_data/valid_case.csv")
    assert result == []

def test_empty_file():
    with pytest.raises(CheckAbort) as e:
        csv_print("test_data/empty.csv")
    assert e.value.code == 2

def test_fee_zero(tmp_path):
    test_csv = tmp_path / "test.csv"
    test_csv.write_text(
        "物品ID,分解产物1_ID,产物1数量,分解产物2_ID,产物2数量,分解手续费,分解耗时(秒)\n"
        "50001,60001,50,,0,0,5\n",  # <- 这是手续费=0的数据
        encoding="utf-8"
    )    
    errors = csv_print(str(test_csv))
    assert errors == []

def test_product2_id_99999(tmp_path):
    test_csv = tmp_path / "bad_test.csv"
    test_csv.write_text(
        "物品ID,分解产物1_ID,产物1数量,分解产物2_ID,产物2数量,分解手续费,分解耗时(秒)\n"
        "50001,60001,50,99999,10,1000,5\n",
        encoding="utf-8"
    )
    errors = csv_print(str(test_csv))
    assert len(errors) == 1
    assert "99999" in errors[0]["问题"]
