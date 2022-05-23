from utils.utils import *


def get_n_days_return(daily_quotation: DataFrame, day: int) -> DataFrame:
    pivot_daily_quotation = standardize(
        daily_quotation,
        index='zs_trading_day',
        columns='zs_code',
        values=['S_DQ_CLOSE']
    )
    pivot_daily_quotation.columns = pivot_daily_quotation.columns.set_levels([f'{day}_days_return'], level=0)
    return (pivot_daily_quotation - pivot_daily_quotation.shift(day)) / pivot_daily_quotation.shift(day)


def get_n_days_return_std(daily_quotation: DataFrame, day: int) -> DataFrame:
    pivot_daily_quotation = get_n_days_return(daily_quotation, day)
    pivot_daily_quotation.columns = pivot_daily_quotation.columns.set_levels([f'{day}_days_return_std'], level=0)
    return pivot_daily_quotation.rolling(day).std()


def get_daily_return_ranking(daily_quotation: DataFrame) -> DataFrame:
    daily_return = get_n_days_return(daily_quotation, 1)
    ranking_data_frame = DataFrame(index=daily_return.index, columns=daily_return.columns)
    ranking_data_frame.columns = ranking_data_frame.columns.set_levels(['daily_return_ranking'], level=0)
    ranking_data_frame.columns = ranking_data_frame.columns.set_levels(
        [f'rank {rank + 1}' for rank in range(len(ranking_data_frame.columns))], level=1
    )
    ranking_code = [code[1] for code in daily_return.columns]
    for date in ranking_data_frame.index:
        return_list = daily_return.loc[date, :]
        cmp_tuple_list = [(code, ret) for code, ret in zip(ranking_code, return_list)]
        ranking_data_frame.loc[date, :] = ranking(cmp_tuple_list)
    return ranking_data_frame


def main():
    df = get_raw_table()

    # 计算 1_day_return
    past_1_day_return = get_n_days_return(df, 1)

    # 计算 10_day_return
    past_10_day_return = get_n_days_return(df, 10)

    # 计算 50_day_std
    past_50_day_std = get_n_days_return_std(df, 50)

    # 计算 daily_ranking
    daily_ranking = get_daily_return_ranking(df)


if __name__ == '__main__':
    main()
