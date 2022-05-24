import click
from pandas import DataFrame
from utils.utils import load

from startup_simple_factor_implementation.cmd_get_factor import \
    past_n_days_return,\
    past_n_days_return_std,\
    past_daily_return_ranking


func_dict = {
    "past_n_days_return": "daily_quotation_std: DataFrame, day: int",
    "past_n_days_return_std": "daily_quotation_std: DataFrame, day: int",
    "past_daily_return_ranking": "daily_quotation_std: DataFrame",
    "load": "column_name: str",
}


def expression_parser(expression: str) -> DataFrame:
    data = eval(expression)
    return data


@click.command()
@click.argument('expression')
def main(expression):
    require = expression_parser(expression)
    print(require.dropna(axis=0, how='all'))


# python cmd_exp_parser.py past_n_days_return(load('S_DQ_CLOSE'),1)
# python cmd_exp_parser.py past_n_days_return(load('S_DQ_CLOSE'),10)
# python cmd_exp_parser.py past_n_days_return_std(load('S_DQ_CLOSE'),50)
# python cmd_exp_parser.py past_daily_return_ranking(load('S_DQ_CLOSE'))
if __name__ == '__main__':
    main()
