#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/29
# @Author  :  zhangjingwen
# @File    :  test_engineering_template.py
import pytest, allure
from utils.common import waitForStatus
from luban_common.base_assert import Assertions
from luban_common import base_utils
import pprint
from swagger.api.luban_glxx_user.project_template import Project_template
from swagger.api.luban_glxx_user.data_template import Data_template


@allure.feature("工程模板")
class TestEngineerTemplate:
    @allure.story("工程划分新建层级-关联表单-删除新建层级")
    def test_engineering_template(self, gaolu_login, gaolu_login_luban, env_conf):
        new_template_node1 = "工程划分测试" + base_utils.generate_random_str()
        new_template_node2 = "工程划分测试" + base_utils.generate_random_str()
        new_template_node3 = "工程划分测试" + base_utils.generate_random_str()

        with allure.step("查询工程划分目录"):
            project_tree_resp = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                               pageIndex=1)
            if project_tree_resp.get('data_totalCount')[0] == 0:
                print("工程划分节点为空")
            else:
                allure.attach("工程划分节点有: {0} 条数据".format(project_tree_resp.get('data_totalCount')[0]))
        with allure.step("添加工程划分一级节点: {0}".format(new_template_node1)):
            creat_body_node1 = {
                "nameList": [new_template_node1],
                "parentId": "0"
            }
            creat_node1_resp = Project_template().saveProjectTemplateUsingPOST(gaolu_login_luban, creat_body_node1)
            waitForStatus(creat_node1_resp, 200, 200, 15)
        with allure.step("断言添加工程划分一级节点: {0} 添加成功".format(new_template_node1)):
            check_tree_resp1 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                              pageIndex=1)
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
            creat_node2_resp = Project_template().saveProjectTemplateUsingPOST(gaolu_login_luban, creat_body_node2)
            waitForStatus(creat_node2_resp, 200, 200, 15)
        with allure.step("断言添加工程划分二级节点: {0} 添加成功".format(new_template_node2)):
            check_tree_resp2 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                              pageIndex=1)
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
            creat_node2_resp = Project_template().saveProjectTemplateUsingPOST(gaolu_login_luban, creat_body_node3)
            waitForStatus(creat_node2_resp, 200, 200, 15)
        with allure.step("断言添加工程划分三级节点: {0} 添加成功".format(new_template_node3)):
            check_tree_resp2 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                              pageIndex=1)
            Assertions.assert_in_value(check_tree_resp2.get('data_result_name'), new_template_node3)
            allure.attach("断言添加工程划分三级节点: {0} 添加成功".format(new_template_node3))
            node_datas = check_tree_resp2.get('source_response')['data']['result']
            dict_name_id3 = {}
            for data in node_datas:
                dict_name_id3[data['name']] = data['id']
        with allure.step("获取资料模板条目列表"):
            resp_temp = Data_template().pageDataTemplateItemUsingGET(gaolu_login_luban, page_size=10000, page_index=1)
            type_dic = {"开工报告": 1,
                        "质量检验（施工）": 2,
                        "交工评定（施工）": 3,
                        "质量检验（监理）": 4,
                        "交工评定（监理）": 5}
            dic_temp = {}
            for data in resp_temp.get('source_response')['data']['result']:
                dic_temp[data['name']] = data['id']
        with allure.step(
                "关联表单模板: {0} 到模板: {1}".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId1'])):
            body1 = {
                "projectTemplateDataTemplates":
                    [{"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId1']],
                      "type": type_dic['开工报告']}],
                "projectTemplateId": dict_name_id3[new_template_node3]
            }
            bind_resp = Project_template().bindDataTemplate2ProjectTemplateUsingPOST(gaolu_login_luban, body1)
            waitForStatus(bind_resp, 200, 200, 15)
        with allure.step(
                "关联表单模板: {0} 到模板: {1} 成功".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId1'])):
            check_table_resp5 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                               pageIndex=1)
            actual_value = None
            for data in check_table_resp5.get('source_response')['data']['result']:
                if data['name'] == new_template_node3:
                    actual_value = data['projectTemplateDataTemplateResponseList']
            Assertions.assert_in_value(actual_value, env_conf['用例配置']['工程模板']['dataTemplateItemId1'])
        with allure.step(
                "关联表单模板: {0} 到模板: {1}".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId2'])):
            body2 = {
                "projectTemplateDataTemplates":
                    [{"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId1']],
                      "type": type_dic['开工报告']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId2']],
                      "type": type_dic['质量检验（施工）']}],
                "projectTemplateId": dict_name_id3[new_template_node3]
            }
            bind_resp = Project_template().bindDataTemplate2ProjectTemplateUsingPOST(gaolu_login_luban, body2)
            waitForStatus(bind_resp, 200, 200, 15)
        with allure.step(
                "关联表单模板: {0} 到模板: {1} 成功".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId2'])):
            check_table_resp5 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                               pageIndex=1)
            actual_value = None
            for data in check_table_resp5.get('source_response')['data']['result']:
                if data['name'] == new_template_node3:
                    actual_value = data['projectTemplateDataTemplateResponseList']
            Assertions.assert_in_value(actual_value, env_conf['用例配置']['工程模板']['dataTemplateItemId2'])
        with allure.step(
                "关联表单模板: {0} 到模板: {1}".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId3'])):
            body3 = {
                "projectTemplateDataTemplates":
                    [{"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId1']],
                      "type": type_dic['开工报告']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId2']],
                      "type": type_dic['质量检验（施工）']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId3']],
                      "type": type_dic['交工评定（施工）']}],
                "projectTemplateId": dict_name_id3[new_template_node3]
            }
            bind_resp = Project_template().bindDataTemplate2ProjectTemplateUsingPOST(gaolu_login_luban, body3)
            waitForStatus(bind_resp, 200, 200, 15)
        with allure.step(
                "关联表单模板: {0} 到模板: {1} 成功".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId3'])):
            check_table_resp5 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                               pageIndex=1)
            actual_value = None
            for data in check_table_resp5.get('source_response')['data']['result']:
                if data['name'] == new_template_node3:
                    actual_value = data['projectTemplateDataTemplateResponseList']
            Assertions.assert_in_value(actual_value, env_conf['用例配置']['工程模板']['dataTemplateItemId3'])
        with allure.step(
                "关联表单模板: {0} 到模板: {1}".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId4'])):
            body4 = {
                "projectTemplateDataTemplates":
                    [{"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId1']],
                      "type": type_dic['开工报告']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId2']],
                      "type": type_dic['质量检验（施工）']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId3']],
                      "type": type_dic['交工评定（施工）']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId4']],
                      "type": type_dic['质量检验（监理）']}],
                "projectTemplateId": dict_name_id3[new_template_node3]
            }
            bind_resp = Project_template().bindDataTemplate2ProjectTemplateUsingPOST(gaolu_login_luban, body4)
            waitForStatus(bind_resp, 200, 200, 15)
        with allure.step(
                "关联表单模板: {0} 到模板: {1} 成功".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId4'])):
            check_table_resp5 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                               pageIndex=1)
            actual_value = None
            for data in check_table_resp5.get('source_response')['data']['result']:
                if data['name'] == new_template_node3:
                    actual_value = data['projectTemplateDataTemplateResponseList']
            Assertions.assert_in_value(actual_value, env_conf['用例配置']['工程模板']['dataTemplateItemId4'])
        with allure.step(
                "关联表单模板: {0} 到模板: {1}".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId5'])):
            body5 = {
                "projectTemplateDataTemplates":
                    [{"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId1']],
                      "type": type_dic['开工报告']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId2']],
                      "type": type_dic['质量检验（施工）']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId3']],
                      "type": type_dic['交工评定（施工）']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId4']],
                      "type": type_dic['质量检验（监理）']},
                     {"dataTemplateItemId": dic_temp[env_conf['用例配置']['工程模板']['dataTemplateItemId5']],
                      "type": type_dic['交工评定（监理）']}],
                "projectTemplateId": dict_name_id3[new_template_node3]
            }
            bind_resp = Project_template().bindDataTemplate2ProjectTemplateUsingPOST(gaolu_login_luban, body5)
            waitForStatus(bind_resp, 200, 200, 15)
        with allure.step(
                "关联表单模板: {0} 到模板: {1} 成功".format(new_template_node3, env_conf['用例配置']['工程模板']['dataTemplateItemId5'])):
            check_table_resp5 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                               pageIndex=1)
            actual_value = None
            for data in check_table_resp5.get('source_response')['data']['result']:
                if data['name'] == new_template_node3:
                    actual_value = data['projectTemplateDataTemplateResponseList']
            Assertions.assert_in_value(actual_value, env_conf['用例配置']['工程模板']['dataTemplateItemId5'])
        with allure.step("删除工程划分三级节点"):
            delete_project3 = Project_template().deleteProjectTemplateUsingDELETE(gaolu_login_luban,
                                                                                  dict_name_id3[new_template_node3])
            waitForStatus(delete_project3, 200, 200, 15)
        with allure.step("断言删除工程划分三级节点: {0} 添加成功".format(new_template_node3)):
            check_tree_resp3 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                              pageIndex=1)
            Assertions.assert_not_in_value(check_tree_resp3.get('data_result_name'), new_template_node3)
            allure.attach("断言删除工程划分三级节点: {0} 添加成功".format(new_template_node3))
        with allure.step("删除工程划分二级节点"):
            delete_project2 = Project_template().deleteProjectTemplateUsingDELETE(gaolu_login_luban,
                                                                                  dict_name_id3[new_template_node2])
            waitForStatus(delete_project2, 200, 200, 15)
        with allure.step("断言删除工程划分二级节点: {0} 添加成功".format(new_template_node2)):
            check_tree_resp3 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                              pageIndex=1)
            Assertions.assert_not_in_value(check_tree_resp3.get('data_result_name'), new_template_node2)
            allure.attach("断言删除工程划分二级节点: {0} 添加成功".format(new_template_node2))
        with allure.step("删除工程划分一级节点"):
            delete_project1 = Project_template().deleteProjectTemplateUsingDELETE(gaolu_login_luban,
                                                                                  dict_name_id3[new_template_node1])
            waitForStatus(delete_project1, 200, 200, 15)
        with allure.step("断言删除工程划分一级节点: {0} 添加成功".format(new_template_node1)):
            check_tree_resp3 = Project_template().pageProjectTemplateUsingGET(gaolu_login_luban, pageSize=10000,
                                                                              pageIndex=1)
            Assertions.assert_not_in_value(check_tree_resp3.get('data_result_name'), new_template_node1)
            allure.attach("断言删除工程划分一级节点: {0} 添加成功".format(new_template_node1))


if __name__ == '__main__':
    pytest.main(["-s", "test_engineering_template.py"])
