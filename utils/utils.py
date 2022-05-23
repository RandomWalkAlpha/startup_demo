from typing import List, Tuple
from pandas import DataFrame
from pandas import read_parquet


def get_raw_table(file_path: str = '../../2015.parquet') -> DataFrame:
    table = read_parquet(file_path)
    return table


def standardize(dataframe: DataFrame, index, columns=None, values=None, subset=None) -> DataFrame:
    if subset is None:
        subset = ['zs_trading_day', 'zs_code']
    dataframe = dataframe.drop_duplicates(subset=subset)
    trading_day_series = dataframe.copy()
    trading_day_series.loc[:, 'zs_trading_day'] = trading_day_series.loc[:, 'zs_trading_day'] * 10000 + 1600
    return trading_day_series.pivot(index=index, columns=columns, values=values)


def load(column_name: str):
    table = get_raw_table()
    return standardize(table, index='zs_trading_day', columns='zs_code', values=column_name)


def ranking(code_list: List[Tuple]) -> List[Tuple]:
    return sorted(code_list, key=lambda x: -x[1])
