import numpy as np
from pandas import DataFrame
from utils.utils import load, ranking


def past_n_days_return(daily_quotation_std: DataFrame, day: int) -> DataFrame:
    n_days_return = (daily_quotation_std - daily_quotation_std.shift(day)) / daily_quotation_std.shift(day)
    return n_days_return


def past_n_days_return_std(daily_quotation_std: DataFrame, day: int) -> DataFrame:
    pivot_daily_quotation = past_n_days_return(daily_quotation_std, day)
    n_days_return_std = pivot_daily_quotation.rolling(day).std()
    return n_days_return_std


def past_daily_return_ranking(daily_quotation_std: DataFrame) -> DataFrame:
    daily_return = past_n_days_return(daily_quotation_std, 1)
    ranking_data_frame = DataFrame(index=daily_return.index, columns=daily_return.columns)
    code_query = {v: k for k, v in enumerate(daily_return.columns)}
    for date in ranking_data_frame.index:
        return_list = daily_return.loc[date, :]
        ranking_tuple_list = ranking([*zip(code_query.keys(), return_list)])
        rank_list = [np.nan] * len(code_query.keys())
        rank = 1
        for c, _ in ranking_tuple_list:
            if not np.isnan(_):
                rank_list[code_query[c]] = rank
                rank += 1
        ranking_data_frame.loc[date, :] = rank_list
    return ranking_data_frame


def main():
    # 计算 1_day_return
    past_1_day_return = past_n_days_return(load('S_DQ_CLOSE'), 1)
    print(past_1_day_return.dropna(axis=0, how='all'))

    # 计算 10_day_return
    past_10_day_return = past_n_days_return(load('S_DQ_CLOSE'), 10)
    print(past_10_day_return.dropna(axis=0, how='all'))

    # 计算 50_day_std
    past_50_day_std = past_n_days_return_std(load('S_DQ_CLOSE'), 50)
    print(past_50_day_std.dropna(axis=0, how='all'))

    # 计算 daily_ranking
    daily_ranking = past_daily_return_ranking(load('S_DQ_CLOSE'))
    print(daily_ranking)


if __name__ == '__main__':
    main()
