#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/29
# @Author  :  zhangjingwen
# @File    :  test_add_sheet.py
import pytest, allure, datetime, re
from luban_common import base_utils
from swagger.api.luban_glxx_user.data_template import Data_template
from swagger.api.inspection.form_group import FormGroup
from swagger.api.inspection.approval_process import ApprovalProcess
from swagger.api.report.service_template import ServiceTemplate
from swagger.api.inspection.content import Content
from swagger.api.inspection.inspection_userinfo import UserInfo
from swagger.api.luban_glxx_user.roleAndRole import Roleandrole
from utils.common import return_section_array, get_section_home_id, return_section_dict, get_data, assemble_dict
from swagger.api.luban_glxx_user.process_template import Process_template
from luban_common.base_assert import Assertions
import random
from utils.common import waitForStatus, key_in_listdict, key_not_in_listdict
import pprint
import json
from swagger.api.inspection.summery_sections import Sections
from swagger.api.inspection.projects import Projects
from swagger.api.inspection.home_page import HomePage


def get_summary_value(item_fixture, section):
    resp_id = Projects().projectsGET(item_fixture)
    project_id = resp_id.get('data__embedded_projectModels_id')
    body = {"projectId": project_id}
    resp = Sections().sectionsGET(item_fixture, body)
    biaoduan_resp = resp.get('source_response')['data']['_embedded']['sectionModels']
    biaoduan_dict = {}
    for data in biaoduan_resp:
        biaoduan_dict[data['name']] = data['id']
    body = {"sectionId": biaoduan_dict[section]}
    period_resp = HomePage().getSummaryPeriodGET(item_fixture, body)
    summary_dic = {}
    for data in period_resp.get('source_response')['data']['series'][0]['data']:
        summary_dic[data['name']] = data['value']
    return summary_dic


def get_summary_bySection_value(item_fixture, section):
    resp_id = Projects().projectsGET(item_fixture)
    project_id = resp_id.get('data__embedded_projectModels_id')
    body = {"projectId": project_id}
    resp = Sections().sectionsGET(item_fixture, body)
    biaoduan_resp = resp.get('source_response')['data']['_embedded']['sectionModels']
    biaoduan_dict = {}
    for data in biaoduan_resp:
        biaoduan_dict[data['name']] = data['id']
    body = {"sectionId": biaoduan_dict[section]}
    bySection_resp = HomePage().getSummarybySectionGET(item_fixture, body)
    summary_dic = {}
    datas = bySection_resp.get('source_response')['data']['series'][0]['data']
    for i in range(0, len(datas)):
        if i == 0:
            summary_dic['已评定'] = datas[i]
        elif i == 1:
            summary_dic['已计量'] = datas[i]
        elif i == 2:
            summary_dic['已归档'] = datas[i]
    return summary_dic


def get_projectNodes_value(item_fixture, section):
    resp_id = Projects().projectsGET(item_fixture)
    project_id = resp_id.get('data__embedded_projectModels_id')
    body = {"projectId": project_id}
    resp = Sections().sectionsGET(item_fixture, body)
    biaoduan_resp = resp.get('source_response')['data']['_embedded']['sectionModels']
    biaoduan_dict = {}
    for data in biaoduan_resp:
        biaoduan_dict[data['name']] = data['id']
    body = {
        "sectionId": biaoduan_dict[section],
    }
    resp = Sections().searchAll(item_fixture, body)
    unit_datas = resp.get('source_response')['data']['_embedded']['projectNodeModels']
    projectNodes = {}
    for data in unit_datas:
        projectNodes[data['name']] = data['id']
    return projectNodes


def get_summary_byUnit_value(item_fixture, section, node):
    unitIds = get_projectNodes_value(item_fixture, section)
    body = {
        "unitId": unitIds[node]
    }
    byUnit_resp = HomePage().getSummarybyUnitGET(item_fixture, body)
    datas = byUnit_resp.get('source_response')['data']['titles']
    title_summary = {}
    for data in datas:
        title_summary[data['title']] = data['total']
    return title_summary


def get_new_tasks_value(item_fixture):
    resp_id = Projects().projectsGET(item_fixture)
    project_id = resp_id.get('data__embedded_projectModels_id')
    body = {"projectId": project_id}
    resp = HomePage().searchNewTasksGET(item_fixture, body)
    totalElements = resp.get('source_response')['data']['page']['totalElements']
    return totalElements


def get_todo_value(item_fixture, role):
    resp_id = Projects().projectsGET(item_fixture)
    project_id = resp_id.get('data__embedded_projectModels_id')
    body = {"operator": role, "projectId": project_id}
    resp = HomePage().searchNewToDoGET(item_fixture, body)
    # todo = resp.get('source_response')['data']['page']['totalElements']
    # return todo


def get_trace_value(item_fixture, role):
    resp_id = Projects().projectsGET(item_fixture)
    project_id = resp_id.get('data__embedded_projectModels_id')
    body = {"tracer": role, "projectId": project_id}
    resp = HomePage().searchTraceGET(item_fixture, body)
    waitForStatus(resp, 200, 200, 15)
    trace = resp.get('source_response')['data']['page']['totalElements']
    return trace


@allure.step('获取一级表单状态')
def check_status(item_fixture, formGroup_id, projectNodeId, classifier='test_construction'):
    add_sheet_result = {"classifier": classifier,
                        "projection": "excerpt",
                        "projectNodeId": projectNodeId}
    group_resp = FormGroup().formGroupsGET(item_fixture, add_sheet_result)
    status = None
    for data in group_resp.get('source_response')['data']['_embedded']['formGroups']:
        if str(data['id']) == formGroup_id:
            status = data['status']
    return status


new_flow = "流程测试" + base_utils.generate_random_str()


@allure.feature("检验评定-新增表单")
class TestInspectionProvisions:
    @allure.story("添加无签名签章审批流程-前置条件")
    @pytest.mark.TestInspectionProvisions
    def test_flow_setting_home_page_deploy(self, gaolu_login, gaolu_login_luban, env_conf):
        new_flow_mark = 'mark_' + new_flow
        new_flow_1 = "流程1_" + base_utils.generate_random_str()
        new_flow_2 = "流程2_" + base_utils.generate_random_str()
        with allure.step('获取roleName'):
            resp = UserInfo().getUserInfoUsingGET(gaolu_login)
            roleName = resp.get('source_response')['data']['roleName']
            name = resp.get('source_response')['data']['name']
            fullName = resp.get('source_response')['data']['fullName']
            username = resp.get('source_response')['data']['username']
        with allure.step('获取发起人角色信息: {0}'.format(roleName)):
            get_roleName = Roleandrole().findRolesUsingGET(gaolu_login_luban, roleName)
            roleIdList = get_roleName.get('data_id')[0]
            Assertions.assert_equal_value(get_roleName.get('data_rolename')[0], roleName)
        with allure.step('获取发起人用户信息: {0}'.format(fullName)):
            get_userName = Roleandrole().findUsersUsingGET(gaolu_login_luban)
            userinfo_datas = get_userName.get('source_response')['data']
            userIdList = None
            for data in userinfo_datas:
                if data['truename'] == fullName:
                    userIdList = data['id']
        with allure.step('新建流程: {0}'.format(new_flow)):
            second_id = str(random.randint(1, 4))
            third_id = str(random.randint(5, 9))
            body = {
                "flowChart":
                    {
                        "lineList": [
                            {
                                "id": "1" + "_" + str(random.randint(100, 999)),
                                "nextNodeId": second_id,
                                "prevNodeId": "1"
                            },
                            {
                                "id": second_id + "_" + str(random.randint(100, 999)),
                                "nextNodeId": third_id,
                                "prevNodeId": second_id
                            },
                            {
                                "id": third_id + "_" + str(random.randint(100, 999)),
                                "nextNodeId": "endNode",
                                "prevNodeId": third_id
                            }
                        ],
                        "nodeList": [
                            {"approvalType": 1,
                             "approverType": 0,
                             "id": "1",
                             "nodeName": "发起人",
                             "nodeType": "TASK_NODE",
                             "roleIdList": [roleIdList],
                             "userIdList": []
                             },
                            {"approvalType": 1,
                             "approverType": 0,
                             "id": int(second_id),
                             "nodeName": new_flow_1,
                             "nodeType": "TASK_NODE",
                             "signName": 2,
                             "signStamp": 2,
                             "roleIdList": [roleIdList],
                             "userIdList": []
                             },
                            {
                                "approvalType": 1,
                                "approverType": 1,
                                "id": int(third_id),
                                "nodeName": new_flow_2,
                                "nodeType": "TASK_NODE",
                                "signName": 2,
                                "signStamp": 2,
                                "roleIdList": [],
                                "userIdList": [userIdList]
                            },
                            {"approvalType": 1,
                             "approverType": 0,
                             "id": "endNode",
                             "nodeName": "结束",
                             "nodeType": "END_NODE",
                             "roleIdList": [],
                             "userIdList": []
                             }
                        ]
                    },
                "id": "",
                "remark": new_flow_mark,
                "sponsorRoleList": [roleIdList],
                "sponsorType": 1,
                "sponsorUserList": [],
                "typeName": new_flow,
                "module": "INSPECTION"
            }
            post_newCreat = Process_template().saveOrUpdateProcessTemplateUsingPOST(gaolu_login_luban, body)
            waitForStatus(post_newCreat, 200, 200, 15)
        with allure.step('断言新添加流程: {0} 成功'.format(new_flow)):
            assert_newCreat = Process_template().pageProcessTemplateUsingGET(gaolu_login_luban, page_size=10000,
                                                                             page_index=1)
            result_datas = assert_newCreat.get('source_response')['data']['result']
            key_in_listdict(result_datas, new_flow, 'typeName')
            print("\n新建流程: {0} 成功".format(new_flow))
            processTemplateId = None
            for data in result_datas:
                if data['typeName'] == new_flow:
                    processTemplateId = data['key']
        with allure.step('获取表单模板库id'):
            resp_id = Data_template().pageDataTemplateUsingGET(gaolu_login_luban, pageSize=50, pageIndex=1)
            dict_form_id = {}
            for data in resp_id.get('source_response')['data']['result']:
                dict_form_id[data['name']] = data['id']
            print("现有表单模板: {0} 成功".format(dict_form_id))
        with allure.step('获取原有关联表单json'):
            list_body = []
            itemId = None
            resp_temp = Data_template().pageDataTemplateItemUsingGET(gaolu_login_luban, page_size=10000, page_index=1)
            for data in resp_temp.get('source_response')['data']['result']:
                if data['processTemplateId'] != '':
                    list_body.append({"itemId": data['id'],
                                      "processTemplateId": data['processTemplateId']})
                if data['name'] == env_conf['用例配置']['主页']['父表单']:
                    itemId = data['id']
        with allure.step('添加需要关联的表单到原有关联表单json'):
            for data in list_body:
                if data['itemId'] == itemId:
                    list_body.remove(data)
            list_body.append({"itemId": itemId,
                              "processTemplateId": processTemplateId})
        with allure.step('关联流程:{0} 到表单 {1}'.format(new_flow, env_conf['用例配置']['主页']['父表单'])):
            templateCode = None
            for data in resp_temp.get('source_response')['data']['result']:
                templateCode = data['templateCode']
            body = {"item2formTemplateItemIdList": list_body,
                    "templateCode": templateCode}
            post_resp = Data_template().updateDataTemplateItem2ProcessTemplateUsingPOST(gaolu_login_luban, body)
            waitForStatus(post_resp, 200, 200, 15)
        with allure.step("断言关联表单成功"):
            resp_result = Data_template().pageDataTemplateItemUsingGET(gaolu_login_luban, page_size=10000, page_index=1)
            for data in resp_result.get('source_response')['data']['result']:
                if data['name'] == env_conf['用例配置']['主页']['父表单']:
                    Assertions.assert_equal_value(data['processTemplateId'], processTemplateId)
            print('关联流程:{0} 到表单: {1} 成功'.format(new_flow, env_conf['用例配置']['主页']['父表单']))

    @allure.story("单个交工评定表单发起-审批-删除表单")
    @pytest.mark.TestInspectionProvisions
    def test_completion_form(self, gaolu_login, gaolu_login_luban, gaolu_login_report, env_conf):
        with allure.step("查看标段"):
            # section_dict = return_section_dict(gaolu_login, env_conf['用例配置']['主页']['section'])
            section_K = return_section_dict(gaolu_login)
            # 获取Kxx 下所有元素
            section_home_arr = return_section_array(gaolu_login, section_K, env_conf['用例配置']['主页']['section'])
            # 获取3级节点的详细信息
            pid_1 = get_section_home_id(section_home_arr, env_conf['用例配置']['主页']['项目节点'])
            # 获4级节点的详细信息
            pid_2 = get_data(section_home_arr, pid_1, env_conf['用例配置']['主页']['文件节点'])
            # 获5级节点的详细信息
            data_temp = get_data(section_home_arr, pid_2['id'], env_conf['用例配置']['主页']['subItem'])
            # 组装为{"name":"id"}
            section_dict = assemble_dict(data_temp)
        with allure.step("获取资料模板条目列表"):
            resp_temp = Data_template().pageDataTemplateItemUsingGET(gaolu_login_luban, page_size=10000, page_index=1)
            for data in resp_temp.get('source_response')['data']['result']:
                if data['name'] == env_conf['用例配置']['主页']['父表单']:
                    template_id1 = data['formTemplateId']
                    template_db_id1 = data['templateCode']
        with allure.step('获取roleName'):
            resp = UserInfo().getUserInfoUsingGET(gaolu_login)
            fullName = resp.get('source_response')['data']['fullName']
        with allure.step('获取发起人用户信息: {0}'.format(fullName)):
            get_userName = Roleandrole().findUsersUsingGET(gaolu_login_luban)
            userinfo_datas = get_userName.get('source_response')['data']
            userIdList = None
            for data in userinfo_datas:
                if data['truename'] == fullName:
                    userIdList = data['id']
        # 检验评定添加父表单
        with allure.step('获取原始主页数据'):
            summary_org = get_summary_value(gaolu_login, env_conf['用例配置']['主页']['section'])
            summary_bySection_org = get_summary_bySection_value(gaolu_login, env_conf['用例配置']['主页']['section'])
            summary_byUnit_org = get_summary_byUnit_value(gaolu_login, env_conf['用例配置']['主页']['section'],
                                                          env_conf['用例配置']['主页']['项目节点'])
            new_task_org = get_new_tasks_value(gaolu_login)
            # todo = get_todo_value(gaolu_login, userIdList)
            task_org = get_trace_value(gaolu_login, userIdList)
        with allure.step('添加父表单: {0}'.format(env_conf['用例配置']['主页']['父表单'])):
            add_parent_sheet_body = {
                "templateId": template_id1,
                "projectNodeId": section_dict[env_conf['用例配置']['主页']['subItem']],
                "templateDbId": int(template_db_id1),
                "classifier": "test_construction"
            }
            resp_add_parent_sheet = FormGroup().addFormGroupsPOST(gaolu_login, add_parent_sheet_body)
            waitForStatus(resp_add_parent_sheet, 200, 200, 15)
            href_formGroup = resp_add_parent_sheet.get('response_header')['Location']
            formGroup_id = href_formGroup.split('/')[-1]
        with allure.step("断言添加父表单: {0} 成功".format(env_conf['用例配置']['主页']['父表单'])):
            add_sheet_result = {"classifier": "test_construction",
                                "projection": "excerpt",
                                "projectNodeId": section_dict[env_conf['用例配置']['主页']['subItem']]}
            group_resp = FormGroup().formGroupsGET(gaolu_login, add_sheet_result)
            id_templateName_dict = {}
            edit_hrefs = {}
            ids = {}
            templateId_ids = {}
            for data in group_resp.get('source_response')['data']['_embedded']['formGroups']:
                id_templateName_dict[str(data['id'])] = data['templateName']
                edit_hrefs[str(data['id'])] = data['instance']['_links']['edit']['href']
                ids[str(data['id'])] = data['instance']['id']
                templateId_ids[str(data['id'])] = data['templateId']
            Assertions.assert_equal_value(id_templateName_dict[formGroup_id], env_conf['用例配置']['主页']['父表单'])
        with allure.step('获取现在主页表单数据'):
            summary_new1 = get_summary_value(gaolu_login, env_conf['用例配置']['主页']['section'])
        with allure.step('断言未发起数量变化'):
            except_value = int(summary_org['未发起'])
            actual_value = int(summary_new1['未发起'])
            if except_value - 200 <= actual_value <= except_value + 200:
                assert True
            else:
                assert False, f'实际值为:{actual_value},预期值为:{except_value}'
        with allure.step("获取表单内容"):
            pattern = re.compile(r'[?]id=[A-Za-z0-9]{1,}')
            result = pattern.findall(edit_hrefs[formGroup_id])
            edit_id = result[0].split('=')[1]
            ServiceTemplate().rbTemplateGET(gaolu_login_report, templateId_ids[formGroup_id])
            ServiceTemplate().rbInstanceGET(gaolu_login_report, edit_id)
            with open('data/测试表6.2.2-2 干砌挡土墙分项工程质量检验评定表(JL).json', 'r', encoding='utf8') as fp:
                json_data = json.load(fp)
            body = {"id": edit_id,
                    "name": id_templateName_dict[formGroup_id],
                    "templateId": templateId_ids[formGroup_id],
                    "data": json_data
                    }
        with allure.step("获取提交表单id"):
            submit_resp = ServiceTemplate().rbInstancePUT(gaolu_login_report, edit_id, body)
            waitForStatus(submit_resp, 200, 200, 15)
            base_utils.file_is_exist(env_conf['用例配置']['主页']['文件路径'])
            resp = Content().contentGET(gaolu_login, ids[formGroup_id])
        with allure.step("提交表单内容"):
            res = Content().contentPOST(gaolu_login, resp.get('source_response')['data']['id'],
                                        env_conf['用例配置']['主页']['文件路径'], 'application/pdf')
            waitForStatus(res, 200, 200, 15)
        with allure.step("发起审批"):
            time = datetime.datetime.now().strftime('%Y-%m-%d')
            body = {"deadline": time, "assignee": userIdList}
            start_approve = ApprovalProcess().starApprovePOST(gaolu_login, body, ids[formGroup_id])
            waitForStatus(start_approve, 200, 200, 15)
        with allure.step("断言发起审批成功"):
            status = check_status(gaolu_login, formGroup_id, section_dict[env_conf['用例配置']['主页']['subItem']])
            Assertions.assert_equal_value(status, 'PROCESSING')
        with allure.step('获取-表单(总)数据统计-数据'):
            summary_new2 = get_summary_value(gaolu_login, env_conf['用例配置']['主页']['section'])
        with allure.step('断言-表单(总)数据统计-审批中-数量变化'):
            except_value = int(summary_org['审批中'])
            actual_value = int(summary_new2['审批中'])
            if except_value - 200 <= actual_value <= except_value + 200:
                assert True
            else:
                assert False, f'实际值为:{actual_value},预期值为:{except_value}'
        with allure.step('获取-项目概况-数据'):
            summary_byUnit_new1 = get_summary_byUnit_value(gaolu_login, env_conf['用例配置']['主页']['section'],
                                                           env_conf['用例配置']['主页']['项目节点'])
        with allure.step('断言-项目概况-评定中-数量变化'):
            except_value = int(summary_byUnit_org['评定中'])
            actual_value = int(summary_byUnit_new1['评定中'])
            if except_value - 200 <= actual_value <= except_value + 200:
                assert True
            else:
                assert False, f'实际值为:{actual_value},预期值为:{except_value}'
        with allure.step('获取-我的代发-数据'):
            except_value = new_task_org
            actual_value = get_new_tasks_value(gaolu_login)
            if except_value - 200 <= actual_value <= except_value + 200:
                assert True
            else:
                assert False, f'实际值为:{actual_value},预期值为:{except_value}'
        with allure.step("审批一"):
            body = {"deadline": time, "comment": "test", "assignee": userIdList}
            pass_approve = ApprovalProcess().passApprovePOST(gaolu_login, body, ids[formGroup_id])
            waitForStatus(pass_approve, 200, 200, 15)
        with allure.step("审批二"):
            body = {"deadline": time, "comment": "test", "assignee": userIdList}
            pass_approve = ApprovalProcess().passApprovePOST(gaolu_login, body, ids[formGroup_id])
            waitForStatus(pass_approve, 200, 200, 15)
        with allure.step("审批完成"):
            status = check_status(gaolu_login, formGroup_id, section_dict[env_conf['用例配置']['主页']['subItem']])
            Assertions.assert_equal_value(status, 'COMPLETED')
        with allure.step('获取-表单(总)数据统计-数据'):
            summary_new3 = get_summary_value(gaolu_login, env_conf['用例配置']['主页']['section'])
            summary_bySection_new = get_summary_bySection_value(gaolu_login, env_conf['用例配置']['主页']['section'])
        with allure.step('断言-表单(总)数据统计-已完成-数量变化'):
            except_value = int(summary_org['已完成'])
            actual_value = int(summary_new3['已完成'])
            if except_value - 200 <= actual_value <= except_value + 200:
                assert True
            else:
                assert False, f'实际值为:{actual_value},预期值为:{except_value}'
        with allure.step('断言-项目数据统计-已评定-数量变化'):
            except_value = int(summary_bySection_org['已评定'])
            actual_value = int(summary_bySection_new['已评定'])
            if except_value - 20 <= actual_value <= except_value + 20:
                assert True
            else:
                assert False, f'实际值为:{actual_value},预期值为:{except_value}'
        with allure.step('获取-项目概况-数据'):
            summary_byUnit_new2 = get_summary_byUnit_value(gaolu_login, env_conf['用例配置']['主页']['section'],
                                                           env_conf['用例配置']['主页']['项目节点'])
        with allure.step('断言-项目概况-已评定-数量变化'):
            except_value = int(summary_byUnit_org['已评定'])
            actual_value = int(summary_byUnit_new2['已评定'])
            if except_value - 200 <= actual_value <= except_value + 200:
                assert True
            else:
                assert False, f'实际值为:{actual_value},预期值为:{except_value}'
        with allure.step('获取-我的已办-数据'):
            except_value = task_org
            actual_value = get_trace_value(gaolu_login, userIdList)
            if except_value - 200 <= actual_value <= except_value + 200:
                assert True
            else:
                assert False, f'实际值为:{actual_value},预期值为:{except_value}'
        with allure.step('删除父表单'):
            delete_sheet1 = FormGroup().deleteFormGroupsDELETE(gaolu_login, formGroup_id)
            waitForStatus(delete_sheet1, 200, 200, 15)

    @allure.story("删除审批流程-删除前置条件数据")
    def test_delete_work_flow_home_page(self, gaolu_login, gaolu_login_luban, env_conf):
        with allure.step("删除流程"):
            assert_newCreat = Process_template().pageProcessTemplateUsingGET(gaolu_login_luban, page_size=10000,
                                                                             page_index=1)
            result_datas = assert_newCreat.get('source_response')['data']['result']
            key_in_listdict(result_datas, new_flow, 'typeName')
            print("\n新建流程: {0} 成功".format(new_flow))
            processTemplateId = None
            for data in result_datas:
                if data['typeName'] == new_flow:
                    processTemplateId = data['key']
            delete_resp = Process_template().deleteProcessTemplateUsingPOST(gaolu_login_luban, processTemplateId)
            waitForStatus(delete_resp, 200, 200, 15)
        with allure.step('断言删除流程: {0} 成功'.format(new_flow)):
            assert_delete = Process_template().pageProcessTemplateUsingGET(gaolu_login_luban, page_size=10000,
                                                                           page_index=1)
            result_delte = assert_delete.get('source_response')['data']['result']
            key_not_in_listdict(result_delte, new_flow, 'typeName')
            print("删除流程: {0} 成功".format(new_flow))


if __name__ == '__main__':
    pytest.main(["-s", "test_add_sheet.py"])
