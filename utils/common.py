#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/11
# @Author  :  zhangjingwen
# @File    :  common.py

import time
import allure
import json
from luban_common.base_assert import Assertions
from swagger.api.inspection.form_group import FormGroup
from swagger.api.inspection.projects import Projects
from swagger.api.inspection.summery_sections import Sections
import pprint


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


@allure.step("返回标段信息")
def return_section_dict(item_fixture, env_conf):
    resp_id = Projects().projectsGET(item_fixture)
    project_id = resp_id.get('data__embedded_projectModels_id')
    body = {"projectId": project_id}
    resp = Sections().sectionsGET(item_fixture, body)
    biaoduan_resp = resp.get('source_response')['data']['_embedded']['sectionModels']
    biaoduan_dict = {}
    for data in biaoduan_resp:
        biaoduan_dict[data['name']] = data['id']
    body = {
        "sectionId": biaoduan_dict[env_conf['用例配置']['表单审批']['单个表单']['section']],
    }
    resp = Sections().searchAll(item_fixture, body)
    unit_datas = resp.get('source_response')['data']['_embedded']['projectNodeModels']
    section_dict = {}
    for data in unit_datas:
        section_dict[data['name']] = data['id']
    return section_dict


@allure.step("返回组装子表单信息的body")
def return_InstanceBody(item_fixture, section_dict, node, group_id,):
    # section_dict[env_conf['用例配置']['表单审批']['单个表单']['subItem']
    sheet_result = {"classifier": "report",
                    "projection": "excerpt",
                    "projectNodeId": section_dict[node]}
    sheet_resp = FormGroup().formGroupsGET(item_fixture, sheet_result)
    href = None
    for data in sheet_resp.get('source_response')['data']['_embedded']['formGroups']:
        if str(data['id']) == group_id:
            href = data['_links']['formInstances']['href']
    key_value = href.split('?')[1].split('=')[1].split('&')[0]
    body = {
        "formGroup": key_value,
        "projection": "excerpt"
    }
    return body


@allure.step("查看子表单信息的templateName")
def return_TemplateName_Id(item_fixture, section_dict, env_conf):
    sheet_result = {"classifier": "report",
                    "projection": "excerpt",
                    "projectNodeId": section_dict[env_conf['用例配置']['表单审批']['单个表单']['subItem']]}
    sheet_resp = FormGroup().formGroupsGET(item_fixture, sheet_result)
    templateName_id = {}
    datas = sheet_resp.get('source_response')['data']['_embedded']['formGroups']
    for data in datas:
        templateName_id[data['templateName']] = data['id']
    return templateName_id
