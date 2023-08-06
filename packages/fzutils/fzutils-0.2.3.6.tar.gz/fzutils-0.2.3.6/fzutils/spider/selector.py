# coding:utf-8

'''
@author = super_fazai
@File    : selector.py
@connect : superonesfazai@gmail.com
'''

"""
selector
"""

import re
from scrapy.selector import Selector
from ..common_utils import _print

__all__ = [
    'parse_field',          # 同步根据类型解析字段
    'async_parse_field',    # 异步根据类型解析字段
]

def parse_field(parser: dict,
                       target_obj: (str, dict),
                       re_is_first=True,
                       logger=None) -> (str, list):
    '''
    ** 异步根据类型解析字段
    :param parser: 解析对象 eg: {'method': 'css', 'selector': '.sss'}
    :param target_obj: 待处理的目标对象
    :param re_is_first: bool 是否re只提取第一个
    :return:
    '''
    res = ''
    if parser is not None:
        parser_method = parser.get('method', '')
        parser_selector = parser.get('selector')
        if parser_method == 're':
            try:
                _ = re.compile(parser_selector).findall(target_obj)
                if re_is_first: res = _[0]
                else: res = _
            except IndexError as e:
                _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)

        elif parser_method == 'css':
            res = Selector(text=target_obj).css(parser_selector).extract_first() or ''

        elif parser_method == 'xpath':
            res = Selector(text=target_obj).xpath(parser_selector).extract_first() or ''

        elif parser_method == 'dict_path':
            # print(parser_selector)
            res = parser_selector

        else:
            raise ValueError('解析该字段的method值未知!')

    return res


async def async_parse_field(*params, **kwargs) -> (str, list):
    '''
    ** 异步根据类型解析字段
    :param parser: 解析对象 eg: {'method': 'css', 'selector': '.sss'}
    :param target_obj: 待处理的目标对象
    :param re_is_first: bool 是否re只提取第一个
    :return:
    '''
    return parse_field(*params, **kwargs)