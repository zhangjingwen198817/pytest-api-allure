#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/11
# @Author  :  zhangjingwen
# @File    :  common.py

import time
import allure
import json
from luban_common.base_assert import Assertions


@allure.step("循环等待状态码")
def waitForStatus(response, status_code, code, times):
    '''
    循环等待状态码
    :param response: 响应数据
    :param expected_http_code: 预期的http状态码
    :param expected_code: 预期code状态码
    :param times 等待秒数
    '''
    for i in range(times):
        if response.get("code")[0] != code or response.get("status_code") != status_code:
            time.sleep(1)
            print('wait {0}s'.format(i))
        else:
            break
    Assertions().assert_all_code(response, status_code, code)


@allure.step("list组装json")
def list_to_tree(data):
    '''
    循环等待状态码
    :param data: 需要遍历的list
    '''
    out = {
        0: {'id': 0, 'parentId': 0, 'name': "Root node", 'children': []}
    }

    for p in data:
        out.setdefault(p['parentId'], {'children': []})
        out.setdefault(p['id'], {'children': []})
        out[p['id']].update(p)
        out[p['parentId']]['children'].append(out[p['id']])
    return out['0']['children']


@allure.step("遍历list中字典子项,删除所有包含key为key_value的value")
def delte_key_from_dict(data, key_value):
    '''
    循环等待状态码
    :param data: 需要遍历的list
    :param key_value: 期望值
    '''
    new_data = []
    for temp_dict in data:
        del temp_dict[key_value]
        new_data.append(temp_dict)
    return new_data


@allure.step("断言字典类型的list中否包含key为index的value值")
def key_in_listdict(data, value, index):
    '''
    循环等待状态码
    :param data: 需要遍历的list
    :param value: 期望值
    :param index: 字典的key
    '''
    Flag = False
    for item in data:
        if value == item[index]:
            Flag = True
            break

    if (Flag):
        assert True, '{0}列表存在{1}'.format(data, value)
    else:
        assert False, '{0}列表不存在{1}'.format(data, value)


@allure.step("断言字典类型的list中不包含key为index的value值")
def key_not_in_listdict(data, value, index):
    '''
    循环等待状态码
    :param data: 需要遍历的list
    :param value: 期望值
    :param index: 字典的key
    '''
    Flag = False
    for item in data:
        if value == item[index]:
            Flag = True
            break

    if (Flag):
        assert False, '{0}列表不存在{1}'.format(data, value)
    else:
        assert True, '{0}列表存在{1}'.format(data, value)
