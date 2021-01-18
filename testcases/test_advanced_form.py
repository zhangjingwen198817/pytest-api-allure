#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2021/1/4
# @Author  :  zhangjingwen
# @File    :  test_advanced_form
import pytest, allure
from utils.common import waitForStatus, return_InstanceBody, return_section_array, get_section_home_id, \
    return_section_dict, get_data, assemble_dict
from luban_common.base_assert import Assertions
from luban_common import base_utils
from swagger.api.luban_glxx_user.data_template import Data_template
from swagger.api.inspection.form_group import FormGroup
from swagger.api.inspection.projects import Projects
from swagger.api.inspection.summery_sections import Sections
from swagger.api.inspection.formInstances import FormInstances
from swagger.api.inspection.sort import Sort
from swagger.api.report.service_template import ServiceTemplate
from swagger.api.inspection.content import Content
import re
import os


@allure.feature("检验评定-高级表单")
class TestAdvancedForm:
    @allure.story("表单编辑-表单保存")
    def test_advance_form(self, gaolu_login, gaolu_login_luban, gaolu_login_report, env_conf):
        with allure.step("查看标段"):
            section_K = return_section_dict(gaolu_login)
            # 获取Kxx 下所有元素
            section_home_arr = return_section_array(gaolu_login, section_K, env_conf['用例配置']['高级表单']['section'])
            # 获取3级节点的详细信息
            pid_1 = get_section_home_id(section_home_arr, env_conf['用例配置']['高级表单']['项目节点'])
            # 获4级节点的详细信息
            pid_2 = get_data(section_home_arr, pid_1, env_conf['用例配置']['高级表单']['文件节点'])
            # 获5级节点的详细信息
            data_temp = get_data(section_home_arr, pid_2['id'], env_conf['用例配置']['高级表单']['subItem'])
            # 组装为{"name":"id"}
            section_dict = assemble_dict(data_temp)
        with allure.step("获取资料模板条目列表"):
            resp_temp = Data_template().pageDataTemplateItemUsingGET(gaolu_login_luban, page_size=10000, page_index=1)
            for data in resp_temp.get('source_response')['data']['result']:
                if data['name'] == env_conf['用例配置']['高级表单']['父表单']:
                    template_id1 = data['formTemplateId']
                    template_db_id1 = data['templateCode']
        # 检验评定添加父表单
        with allure.step('添加父表单: {0}'.format(env_conf['用例配置']['高级表单']['父表单'])):
            add_parent_sheet_body = {
                "templateId": template_id1,
                "projectNodeId": section_dict[env_conf['用例配置']['高级表单']['subItem']],
                "templateDbId": int(template_db_id1),
                "classifier": "report"
            }
            resp_add_parent_sheet = FormGroup().addFormGroupsPOST(gaolu_login, add_parent_sheet_body)
            waitForStatus(resp_add_parent_sheet, 200, 200, 15)
            href_formGroup = resp_add_parent_sheet.get('response_header')['Location']
            formGroup_id = href_formGroup.split('/')[-1]
        with allure.step("断言添加父表单: {0} 成功".format(env_conf['用例配置']['高级表单']['父表单'])):
            add_sheet_result = {"classifier": "report",
                                "projection": "excerpt",
                                "projectNodeId": section_dict[env_conf['用例配置']['高级表单']['subItem']]}
            group_resp = FormGroup().formGroupsGET(gaolu_login, add_sheet_result)
            id_templateName_dict = {}
            for data in group_resp.get('source_response')['data']['_embedded']['formGroups']:
                id_templateName_dict[str(data['id'])] = data['templateName']
            Assertions.assert_equal_value(id_templateName_dict[formGroup_id], env_conf['用例配置']['高级表单']['父表单'])
        with allure.step('添加子表单'):
            body = {"classifier": "report",
                    "projection": "excerpt",
                    "projectNodeId": section_dict[env_conf['用例配置']['高级表单']['subItem']]}
            formGroup_resp_dict = {}
            formGroup_resp = FormGroup().formGroupsGET(gaolu_login, body)
            for data in formGroup_resp.get('source_response')['data']['_embedded']['formGroups']:
                formGroup_resp_dict[str(data['id'])] = data['_links']['self']['href']

            sheet_name = "测试表单" + base_utils.generate_random_str()
            sheet_body = {"name": sheet_name,
                          "toFormInstance": "",
                          "formGroup": formGroup_resp_dict[formGroup_id]}
            resp_child = FormInstances().formInstancesPOST(gaolu_login, sheet_body)
            waitForStatus(resp_child, 200, 200, 15)
            print('添加子表单: {0} 成功'.format(sheet_name))
        with allure.step('获取子表单templateId'):
            node = env_conf['用例配置']['高级表单']['subItem']
            body = return_InstanceBody(gaolu_login, section_dict, node, formGroup_id)
            res = FormInstances().formInstanceSearchGET(gaolu_login, body)
            templateId_ids = {}
            ids = {}
            edit_hrefs = {}
            for data in res.get('source_response')['data']['_embedded']['formInstances']:
                templateId_ids[data['name']] = data['templateId']
                ids[data['name']] = data['id']
                edit_hrefs[data['name']] = data['_links']['edit']['href']
        with allure.step("获取表单内容"):
            pattern = re.compile(r'[?]id=[A-Za-z0-9]{1,}')
            result = pattern.findall(edit_hrefs[sheet_name])
            edit_id = result[0].split('=')[1]
            ServiceTemplate().rbTemplateGET(gaolu_login_report, templateId_ids[sheet_name])
            content_resp = ServiceTemplate().rbInstanceGET(gaolu_login_report, edit_id)
            body = content_resp.get('source_response')['data']
        with allure.step("获取提交表单id"):
            submit_resp = ServiceTemplate().rbInstancePUT(gaolu_login_report, edit_id, body)
            waitForStatus(submit_resp, 200, 200, 15)
            base_utils.file_is_exist(env_conf['用例配置']['高级表单']['文件路径'])
            os.rename(env_conf['用例配置']['高级表单']['文件路径'], "data/" + sheet_name + ".pdf")
            resp = Content().contentGET(gaolu_login, ids[sheet_name])
        with allure.step("提交表单内容"):
            res = Content().contentPOST(gaolu_login, resp.get('source_response')['data']['id'],
                                        "data/" + sheet_name + ".pdf", 'application/pdf')
            os.rename("data/" + sheet_name + ".pdf", env_conf['用例配置']['高级表单']['文件路径'])
            waitForStatus(res, 200, 200, 15)
        with allure.step("删除子表单"):
            delete_sheet3 = Sort().formInstancesDELETE(gaolu_login, ids[sheet_name])
            waitForStatus(delete_sheet3, 200, 200, 15)
        with allure.step('删除父表单'):
            delete_sheet1 = FormGroup().deleteFormGroupsDELETE(gaolu_login, formGroup_id)
            waitForStatus(delete_sheet1, 200, 200, 15)


if __name__ == '__main__':
    pytest.main(["-s", "test_advanced_form.py"])
