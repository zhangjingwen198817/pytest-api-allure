#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/29
# @Author  :  zhangjingwen
# @File    :  test_add_sheet.py
import pytest, allure
from utils.common import waitForStatus, return_section_dict
from luban_common.base_assert import Assertions
from luban_common import base_utils
from swagger.api.luban_glxx_user.project_template import Project_template
from swagger.api.luban_glxx_user.data_template import Data_template
from swagger.api.inspection.formInstances import FormInstances
from swagger.api.inspection.sort import Sort
from swagger.api.inspection.form_group import FormGroup

new_template_node1 = "工程划分测试" + base_utils.generate_random_str()
new_template_node2 = "工程划分测试" + base_utils.generate_random_str()
new_template_node3 = "工程划分测试" + base_utils.generate_random_str()

@allure.feature("检验评定-新增表单")
class TestInspectionProvisions:
    @allure.story("添加工程模板划分-前置条件")
    @pytest.mark.skiprest
    def test_add_engineering_template_deploy(self, gaolu_login, env_conf):
        # 添加工程模板
        with allure.step("查询工程划分目录"):
            project_tree_resp = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000, pageIndex=1)
            if project_tree_resp.get('data_totalCount')[0] == 0:
                print("工程划分节点为空")
            else:
                allure.attach("工程划分节点有: {0} 条数据".format(project_tree_resp.get('data_totalCount')[0]))
        with allure.step("添加工程划分一级节点: {0}".format(new_template_node1)):
            creat_body_node1 = {
                "nameList": [new_template_node1],
                "parentId": "0"
            }
            creat_node1_resp = Project_template().saveProjectTemplateUsingPOST(gaolu_login, creat_body_node1)
            waitForStatus(creat_node1_resp, 200, 200, 15)
        with allure.step("断言添加工程划分一级节点: {0} 添加成功".format(new_template_node1)):
            check_tree_resp1 = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000, pageIndex=1)
            Assertions.assert_in_value(check_tree_resp1.get('data_result_name'), new_template_node1)
            allure.attach("断言添加工程划分一级节点: {0} 添加成功".format(new_template_node1))
            node_datas = check_tree_resp1.get('source_response')['data']['result']
            dict_name_id1 = {}
            for data in node_datas:
                dict_name_id1[data['name']] = data['id']
        with allure.step("添加工程划分二级节点: {0}".format(new_template_node2)):
            creat_body_node2 = {
                "nameList": [new_template_node2],
                "parentId": dict_name_id1[new_template_node1]
            }
            creat_node2_resp = Project_template().saveProjectTemplateUsingPOST(gaolu_login, creat_body_node2)
            waitForStatus(creat_node2_resp, 200, 200, 15)
        with allure.step("断言添加工程划分二级节点: {0} 添加成功".format(new_template_node2)):
            check_tree_resp2 = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000, pageIndex=1)
            Assertions.assert_in_value(check_tree_resp2.get('data_result_name'), new_template_node2)
            allure.attach("断言添加工程划分二级节点: {0} 添加成功".format(new_template_node2))
            node_datas = check_tree_resp2.get('source_response')['data']['result']
            dict_name_id2 = {}
            for data in node_datas:
                dict_name_id2[data['name']] = data['id']
        with allure.step("添加工程划分三级节点: {0}".format(new_template_node2)):
            creat_body_node3 = {
                "nameList": [new_template_node3],
                "parentId": dict_name_id2[new_template_node2]
            }
            creat_node2_resp = Project_template().saveProjectTemplateUsingPOST(gaolu_login, creat_body_node3)
            waitForStatus(creat_node2_resp, 200, 200, 15)
        with allure.step("断言添加工程划分三级节点: {0} 添加成功".format(new_template_node3)):
            check_tree_resp2 = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000, pageIndex=1)
            Assertions.assert_in_value(check_tree_resp2.get('data_result_name'), new_template_node3)
            allure.attach("断言添加工程划分三级节点: {0} 添加成功".format(new_template_node3))
            node_datas = check_tree_resp2.get('source_response')['data']['result']
            dict_name_id3 = {}
            for data in node_datas:
                dict_name_id3[data['name']] = data['id']
        # 工程模板管理表单
        with allure.step("获取资料模板条目列表"):
            resp_temp = Data_template().pageDataTemplateItemUsingGET(gaolu_login, page_size=10000, page_index=1)
            type_dic = {"开工报告": 1,
                        "质量检验（施工）": 2,
                        "交工评定（施工）": 3,
                        "质量检验（监理）": 4,
                        "交工评定（监理）": 5}
            dic_temp = {}
            for data in resp_temp.get('source_response')['data']['result']:
                dic_temp[data['name']] = data['id']
        with allure.step(
                "关联表单模板: {0} 到模板: {1}".format(new_template_node3, env_conf['用例配置']['增加表单']['应用模板表单'])):
            body1 = {
                "projectTemplateDataTemplates":
                    [{"dataTemplateItemId": dic_temp[env_conf['用例配置']['增加表单']['应用模板表单']],
                      "type": type_dic['开工报告']}],
                "projectTemplateId": dict_name_id3[new_template_node3]
            }
            bind_resp = Project_template().bindDataTemplate2ProjectTemplateUsingPOST(gaolu_login, body1)
            waitForStatus(bind_resp, 200, 200, 15)
        with allure.step(
                "关联表单模板: {0} 到模板: {1} 成功".format(new_template_node3, env_conf['用例配置']['增加表单']['应用模板表单'])):
            check_table_resp5 = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000, pageIndex=1)
            actual_value = None
            for data in check_table_resp5.get('source_response')['data']['result']:
                if data['name'] == new_template_node3:
                    actual_value = data['projectTemplateDataTemplateResponseList']
            Assertions.assert_in_value(actual_value, env_conf['用例配置']['增加表单']['应用模板表单'])

    @allure.story("新增表单-表单上移下移动-上传模板-应用模板-删除表单")
    @pytest.mark.skiprest
    def test_new_sheet(self, gaolu_login, env_conf):
        # 新增表单
        with allure.step("查看标段"):
            section_dict = return_section_dict(gaolu_login, env_conf)
        with allure.step("获取资料模板条目列表"):
            resp_temp = Data_template().pageDataTemplateItemUsingGET(gaolu_login, page_size=10000, page_index=1)
            for data in resp_temp.get('source_response')['data']['result']:
                if data['name'] == env_conf['用例配置']['增加表单']['父表单']:
                    template_id1 = data['formTemplateId']
                    template_db_id1 = data['templateCode']
                elif data['name'] == env_conf['用例配置']['增加表单']['普通表单']:
                    template_id2 = data['formTemplateId']
                    template_db_id2 = data['templateCode']
        with allure.step('添加普通表单'):
            add_sheet_body = {
                "templateId": template_id2,
                "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']],
                "templateDbId": int(template_db_id2),
                "classifier": "report"
            }
            resp_add_sheet = FormGroup().addFormGroupsPOST(gaolu_login, add_sheet_body)
            waitForStatus(resp_add_sheet, 200, 200, 15)
        with allure.step("断言添加普通表单: {0} 成功".format(env_conf['用例配置']['增加表单']['普通表单'])):
            add_sheet_result = {"classifier": "report",
                                "projection": "excerpt",
                                "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']]}
            up_down_resp = FormGroup().formGroupsGET(gaolu_login, add_sheet_result)
            name_id_dict = {}
            for data in up_down_resp.get('source_response')['data']['_embedded']['formGroups']:
                name_id_dict[data['templateName']] = data['id']
            Assertions.assert_in_key(name_id_dict, env_conf['用例配置']['增加表单']['普通表单'])
        # 检验评定添加父表单
        with allure.step('添加父表单'):
            add_parent_sheet_body = {
                "templateId": template_id1,
                "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']],
                "templateDbId": int(template_db_id1),
                "classifier": "report"
            }
            resp_add_parent_sheet = FormGroup().addFormGroupsPOST(gaolu_login, add_parent_sheet_body)
            waitForStatus(resp_add_parent_sheet, 200, 200, 15)
        with allure.step("断言添加父表单: {0} 成功".format(env_conf['用例配置']['增加表单']['父表单'])):
            add_sheet_result = {"classifier": "report",
                                "projection": "excerpt",
                                "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']]}
            up_down_resp = FormGroup().formGroupsGET(gaolu_login, add_sheet_result)
            name_id_dict = {}
            for data in up_down_resp.get('source_response')['data']['_embedded']['formGroups']:
                name_id_dict[data['templateName']] = data['id']
            Assertions.assert_in_key(name_id_dict, env_conf['用例配置']['增加表单']['父表单'])
        with allure.step('添加子表单'):
            body = {"classifier": "report",
                    "projection": "excerpt",
                    "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']]}
            formGroup_resp_dict = {}
            formGroup_resp = FormGroup().formGroupsGET(gaolu_login, body)
            for data in formGroup_resp.get('source_response')['data']['_embedded']['formGroups']:
                formGroup_resp_dict[data['templateName']] = data['_links']['self']['href']

            sheet_name = "测试表单" + base_utils.generate_random_str()
            sheet_body = {"name": sheet_name,
                          "toFormInstance": "",
                          "formGroup": formGroup_resp_dict[env_conf['用例配置']['增加表单']['父表单']]}
            resp_child = FormInstances().formInstancesPOST(gaolu_login, sheet_body)
            waitForStatus(resp_child, 200, 200, 15)
        # 表单上移
        with allure.step("上移表单"):
            up_down_body = {"classifier": "report",
                            "projection": "excerpt",
                            "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']]}
            up_down_resp = FormGroup().formGroupsGET(gaolu_login, up_down_body)

            name_id_dict = {}
            for data in up_down_resp.get('source_response')['data']['_embedded']['formGroups']:
                name_id_dict[data['templateName']] = data['id']

            id_weight_dict = {}
            for data in up_down_resp.get('source_response')['data']['_embedded']['formGroups']:
                id_weight_dict[str(data['id'])] = data['weight']

            weight_body_down = {"weight": id_weight_dict[str(name_id_dict[env_conf['用例配置']['增加表单']['普通表单']])]}

            down_form_resp = FormGroup().upDownFormPatch(gaolu_login,
                                                         name_id_dict[env_conf['用例配置']['增加表单']['父表单']],
                                                         weight_body_down)
            waitForStatus(down_form_resp, 200, 200, 15)

            weight_body_up = {"weight": id_weight_dict[str(name_id_dict[env_conf['用例配置']['增加表单']['父表单']])]}
            up_form_resp = FormGroup().upDownFormPatch(gaolu_login,
                                                       name_id_dict[env_conf['用例配置']['增加表单']['普通表单']],
                                                       weight_body_up)
            waitForStatus(up_form_resp, 200, 200, 15)
        with allure.step("断言上移表单成功"):
            up_down_result_body = {"classifier": "report",
                                   "projection": "excerpt",
                                   "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']]}
            up_down_resp = FormGroup().formGroupsGET(gaolu_login, up_down_result_body)
            result_weight_dict = {}
            for data in up_down_resp.get('source_response')['data']['_embedded']['formGroups']:
                result_weight_dict[str(data['id'])] = data['weight']
            Assertions.assert_equal_value(result_weight_dict[str(name_id_dict[env_conf['用例配置']['增加表单']['普通表单']])],
                                          id_weight_dict[str(name_id_dict[env_conf['用例配置']['增加表单']['父表单']])])
        with allure.step("获取资料模板条目列表"):
            resp_temp = Data_template().pageDataTemplateItemUsingGET(gaolu_login, page_size=10000, page_index=1)
            for data in resp_temp.get('source_response')['data']['result']:
                if data['name'] == env_conf['用例配置']['增加表单']['应用模板表单']:
                    template_id3 = data['formTemplateId']
                    template_db_id3 = data['templateCode']
        with allure.step("应用模板"):
            add_use_sheet_body = {
                "templateId": template_id3,
                "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']],
                "templateDbId": int(template_db_id3),
                "classifier": "report"
            }
            resp_add_parent_sheet = FormGroup().addFormGroupsPOST(gaolu_login, add_use_sheet_body)
            waitForStatus(resp_add_parent_sheet, 200, 200, 15)
        with allure.step("断言应用模板: {0} 成功".format(env_conf['用例配置']['增加表单']['应用模板表单'])):
            add_sheet_result = {"classifier": "report",
                                "projection": "excerpt",
                                "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']]}
            up_down_resp = FormGroup().formGroupsGET(gaolu_login, add_sheet_result)
            name_id_dict = {}
            for data in up_down_resp.get('source_response')['data']['_embedded']['formGroups']:
                name_id_dict[data['templateName']] = data['id']
            Assertions.assert_in_key(name_id_dict, env_conf['用例配置']['增加表单']['应用模板表单'])
        with allure.step("查询可上传的模板"):
            up_body = {"classifier": "report"}
            resp_temp = FormGroup().searchUpTemplatesGET(gaolu_login, up_body)
            up_dict = {}
            for data in resp_temp.get('source_response')['data']['_embedded']['stashNodes']:
                up_dict[data['name']] = data['id']
        with allure.step('上传模板'):
            up_sheet_result = {"classifier": "report",
                               "projection": "excerpt",
                               "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']]}
            up_resp = FormGroup().formGroupsGET(gaolu_login, up_sheet_result)
            body_data = []
            body_params = {"classifier": "report"}
            for data in up_resp.get('source_response')['data']['_embedded']['formGroups']:
                body_data.append({"templateDbId": data['templateDbId'], "templateId": data['templateId'],
                                  "templateName": data['templateName']})
            resp = FormGroup().upTemplatesPUT(gaolu_login, up_dict[new_template_node3], body_data, body_params)
            waitForStatus(resp, 200, 200, 15)
        # 删除表单
        with allure.step('删除子表单'):
            delete_sheet_result = {"classifier": "report",
                                   "projection": "excerpt",
                                   "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']]}
            delete_resp = FormGroup().formGroupsGET(gaolu_login, delete_sheet_result)
            href = None
            templateName_id = {}
            for data in delete_resp.get('source_response')['data']['_embedded']['formGroups']:
                templateName_id[data['templateName']] = data['id']
                if data['templateName'] == env_conf['用例配置']['增加表单']['父表单']:
                    href = data['_links']['formInstances']['href']
            key_value = href.split('?')[1].split('=')[1].split('&')[0]
            body = {
                "formGroup": key_value,
                "projection": "excerpt"
            }
            res = FormInstances().formInstanceSearchGET(gaolu_login, body)
            delete_id = None
            for data in res.get('source_response')['data']['_embedded']['formInstances']:
                if data['name'] == sheet_name:
                    delete_id = data['id']
            delete_sheet3 = Sort().formInstancesDELETE(gaolu_login, delete_id)
            waitForStatus(delete_sheet3, 200, 200, 15)
        with allure.step('删除父表单'):
            delete_sheet1 = FormGroup().deleteFormGroupsDELETE(gaolu_login,
                                                               templateName_id[env_conf['用例配置']['增加表单']['父表单']])
            waitForStatus(delete_sheet1, 200, 200, 15)
        with allure.step('删除普通表单'):
            delete_sheet2 = FormGroup().deleteFormGroupsDELETE(gaolu_login,
                                                               templateName_id[env_conf['用例配置']['增加表单']['普通表单']])
            waitForStatus(delete_sheet2, 200, 200, 15)
        with allure.step('删除应用模板表单'):
            delete_sheet3 = FormGroup().deleteFormGroupsDELETE(gaolu_login,
                                                               templateName_id[env_conf['用例配置']['增加表单']['应用模板表单']])
            waitForStatus(delete_sheet3, 200, 200, 15)

    @allure.story("删除工程模板划分-清理前置条件")
    def test_delete_engineering_template(self, gaolu_login, env_conf):
        check_tree_resp2 = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000, pageIndex=1)
        node_datas = check_tree_resp2.get('source_response')['data']['result']
        dict_name_id3 = {}
        for data in node_datas:
            dict_name_id3[data['name']] = data['id']
        # 删除工程模板节点
        with allure.step("删除工程划分三级节点"):
            delete_project3 = Project_template().deleteProjectTemplateUsingDELETE(gaolu_login,
                                                                                  dict_name_id3[new_template_node3])
            waitForStatus(delete_project3, 200, 200, 15)
        with allure.step("断言删除工程划分三级节点: {0} 添加成功".format(new_template_node3)):
            check_tree_resp3 = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000,
                                                                              pageIndex=1)
            Assertions.assert_not_in_value(check_tree_resp3.get('data_result_name'), new_template_node3)
            allure.attach("断言删除工程划分三级节点: {0} 添加成功".format(new_template_node3))
        with allure.step("删除工程划分二级节点"):
            delete_project2 = Project_template().deleteProjectTemplateUsingDELETE(gaolu_login,
                                                                                  dict_name_id3[new_template_node2])
            waitForStatus(delete_project2, 200, 200, 15)
        with allure.step("断言删除工程划分二级节点: {0} 添加成功".format(new_template_node2)):
            check_tree_resp3 = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000,
                                                                              pageIndex=1)
            Assertions.assert_not_in_value(check_tree_resp3.get('data_result_name'), new_template_node2)
            allure.attach("断言删除工程划分二级节点: {0} 添加成功".format(new_template_node2))
        with allure.step("删除工程划分一级节点"):
            delete_project1 = Project_template().deleteProjectTemplateUsingDELETE(gaolu_login,
                                                                                  dict_name_id3[new_template_node1])
            waitForStatus(delete_project1, 200, 200, 15)
        with allure.step("断言删除工程划分一级节点: {0} 添加成功".format(new_template_node1)):
            check_tree_resp3 = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000,
                                                                              pageIndex=1)
            Assertions.assert_not_in_value(check_tree_resp3.get('data_result_name'), new_template_node1)
            allure.attach("断言删除工程划分一级节点: {0} 添加成功".format(new_template_node1))


if __name__ == '__main__':
    pytest.main(["-s", "test_add_sheet.py"])
