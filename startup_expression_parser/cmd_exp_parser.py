import sys
sys.path.append('../../startup_demo/')

import argparse
from startup_simple_factor_implementation.cmd_get_factor import *


func_dict = {
    "past_n_days_return": "daily_quotation_std: DataFrame, day: int",
    "past_n_days_return_std": "daily_quotation_std: DataFrame, day: int",
    "past_daily_return_ranking": "daily_quotation_std: DataFrame",
    "load": "column_name: str",
}


def syntax_check(expression: str) -> bool:
    if expression is None:
        return True
    # 验证函数名称是否有效
    func = expression[: expression.find('(')]
    assert func in func_dict, f"'{func}' is an invalid function."
    # 验证其参数列表
    next_exp_l = expression.find('(') + 1
    next_exp_r = expression.rfind(')')
    param_list = expression[next_exp_l: next_exp_r].split(',')
    assert len(param_list) == len(func_dict[func].split(',')), "Illegal parameter(s)"
    # 若参数包含函数，递归验证
    for arg in param_list:
        if '(' in arg:
            if syntax_check(arg):
                continue
    return True


def expression_parser(expression: str) -> DataFrame:
    assert syntax_check(expression) is True, "Illegal expression."
    data = eval(expression)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', help='因子计算表达式', type=str)
    args = parser.parse_args()
    require = expression_parser(args.expression)
    print(require)


# python .\cmd_exp_parser.py past_n_days_return(load('S_DQ_CLOSE'),1)
# python .\cmd_exp_parser.py past_n_days_return(load('S_DQ_CLOSE'),10)
# python .\cmd_exp_parser.py past_n_days_return_std(load('S_DQ_CLOSE'),50)
# python .\cmd_exp_parser.py past_daily_return_ranking(load('S_DQ_CLOSE'))
if __name__ == '__main__':
    main()
