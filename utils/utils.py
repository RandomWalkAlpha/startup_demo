import pandas as pd
from pandas import DataFrame
from pandas import read_parquet


def get_raw_table(file_path: str) -> DataFrame:
    table = read_parquet(file_path)
    return table
