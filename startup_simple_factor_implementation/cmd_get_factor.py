from utils.utils import *


def get_n_days_return(daily_quotation_std: DataFrame, day: int) -> DataFrame:
    return (daily_quotation_std - daily_quotation_std.shift(day)) / daily_quotation_std.shift(day)


def get_n_days_return_std(daily_quotation_std: DataFrame, day: int) -> DataFrame:
    pivot_daily_quotation = get_n_days_return(daily_quotation_std, day)
    return pivot_daily_quotation.rolling(day).std()


def get_daily_return_ranking(daily_quotation_std: DataFrame) -> DataFrame:
    daily_return = get_n_days_return(daily_quotation_std, 1)
    ranking_data_frame = DataFrame(index=daily_return.index, columns=daily_return.columns)
    ranking_data_frame.columns = [f'rank {rank + 1}' for rank in range(len(ranking_data_frame.columns))]
    ranking_code = daily_return.columns
    for date in ranking_data_frame.index:
        return_list = daily_return.loc[date, :]
        cmp_tuple_list = [(code, ret) for code, ret in zip(ranking_code, return_list)]
        ranking_data_frame.loc[date, :] = ranking(cmp_tuple_list)
    return ranking_data_frame


def main():
    df_raw = get_raw_table()
    df_std = standardize(df_raw, index='zs_trading_day', columns='zs_code', values='S_DQ_CLOSE')

    # 计算 1_day_return
    past_1_day_return = get_n_days_return(df_std, 1)
    print(past_1_day_return)

    # 计算 10_day_return
    past_10_day_return = get_n_days_return(df_std, 10)
    print(past_10_day_return)

    # 计算 50_day_std
    past_50_day_std = get_n_days_return_std(df_std, 50)
    print(past_50_day_std)

    # 计算 daily_ranking
    daily_ranking = get_daily_return_ranking(df_std)
    print(daily_ranking)


if __name__ == '__main__':
    main()
