import sys
sys.path.append('../../startup_demo/')

import argparse
from startup_simple_factor_implementation.cmd_get_factor import *


def expression_parser(expression: str) -> DataFrame:
    data = eval(expression)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', help='因子计算表达式', type=str)
    args = parser.parse_args()
    require = expression_parser(args.expression)
    print(require)


# python .\cmd_exp_parser.py past_n_days_return(load('S_DQ_CLOSE'),1)
if __name__ == '__main__':
    main()
