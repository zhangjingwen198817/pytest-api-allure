#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2021/1/4
# @Author  :  zhangjingwen
# @File    :  test_approve_form.py
import pytest, allure, datetime, re, os
from luban_common import base_utils
from swagger.api.luban_glxx_user.data_template import Data_template
from swagger.api.inspection.form_group import FormGroup
from swagger.api.inspection.formInstances import FormInstances
from swagger.api.inspection.approval_process import ApprovalProcess
from swagger.api.report.service_template import ServiceTemplate
from swagger.api.inspection.content import Content
from swagger.api.inspection.inspection_userinfo import UserInfo
from swagger.api.luban_glxx_user.roleAndRole import Roleandrole
from utils.common import return_section_dict, return_InstanceSearchBody, return_TemplateName_Id
from luban_common.base_assert import Assertions
from swagger.api.inspection.sort import Sort
from swagger.api.luban_glxx_user.process_template import Process_template
from luban_common.base_assert import Assertions
import random
from utils.common import waitForStatus, key_in_listdict, key_not_in_listdict

new_flow = "流程测试" + base_utils.generate_random_str()


@allure.feature("检验评定-表单审批")
class TestAdvancedForm:

    @allure.story("添加无签名签章审批流程-前置条件")
    @pytest.mark.skiprest
    def test_flow_setting_deploy(self, gaolu_login, env_conf):
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
            get_roleName = Roleandrole().findRolesUsingGET(gaolu_login, roleName)
            roleIdList = get_roleName.get('data_id')[0]
            Assertions.assert_equal_value(get_roleName.get('data_rolename')[0], roleName)
        with allure.step('获取发起人用户信息: {0}'.format(fullName)):
            get_userName = Roleandrole().findUsersUsingGET(gaolu_login)
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
                "typeName": new_flow
            }
            post_newCreat = Process_template().saveOrUpdateProcessTemplateUsingPOST(gaolu_login, body)
            waitForStatus(post_newCreat, 200, 200, 15)
        with allure.step('断言新添加流程: {0} 成功'.format(new_flow)):
            assert_newCreat = Process_template().pageProcessTemplateUsingGET(gaolu_login, page_size=10000, page_index=1)
            result_datas = assert_newCreat.get('source_response')['data']['result']
            key_in_listdict(result_datas, new_flow, 'typeName')
            print("\n新建流程: {0} 成功".format(new_flow))
            processTemplateId = None
            for data in result_datas:
                if data['typeName'] == new_flow:
                    processTemplateId = data['key']
        with allure.step('获取表单模板库id'):
            resp_id = Data_template().pageDataTemplateUsingGET(gaolu_login, pageSize=50, pageIndex=1)
            dict_form_id = {}
            for data in resp_id.get('source_response')['data']['result']:
                dict_form_id[data['name']] = data['id']
            print("现有表单模板: {0} 成功".format(dict_form_id))
        with allure.step('获取原有关联表单json'):
            list_body = []
            itemId = None
            resp_temp = Data_template().pageDataTemplateItemUsingGET(gaolu_login, page_size=10000, page_index=1)
            for data in resp_temp.get('source_response')['data']['result']:
                if data['processTemplateId'] != '':
                    list_body.append({"itemId": data['id'],
                                      "processTemplateId": data['processTemplateId']})
                if data['name'] == env_conf['用例配置']['表单审批']['单个表单']['父表单']:
                    itemId = data['id']
        with allure.step('添加需要关联的表单到原有关联表单json'):
            for data in list_body:
                if data['itemId'] == itemId:
                    list_body.remove(data)
            list_body.append({"itemId": itemId,
                              "processTemplateId": processTemplateId})
        with allure.step('关联流程:{0} 到表单 {1}'.format(new_flow, env_conf['用例配置']['表单审批']['单个表单']['父表单'])):
            templateCode = None
            for data in resp_temp.get('source_response')['data']['result']:
                templateCode = data['templateCode']
            body = {"item2formTemplateItemIdList": list_body,
                    "templateCode": templateCode}
            post_resp = Data_template().updateDataTemplateItem2ProcessTemplateUsingPOST(gaolu_login, body)
            waitForStatus(post_resp, 200, 200, 15)
        with allure.step("断言关联表单成功"):
            resp_result = Data_template().pageDataTemplateItemUsingGET(gaolu_login, page_size=10000, page_index=1)
            for data in resp_result.get('source_response')['data']['result']:
                if data['name'] == env_conf['用例配置']['表单审批']['单个表单']['父表单']:
                    Assertions.assert_equal_value(data['processTemplateId'], processTemplateId)
            print('关联流程:{0} 到表单: {1} 成功'.format(new_flow, env_conf['用例配置']['表单审批']['单个表单']['父表单']))

    @allure.story("单个表单发起-审批-回退至上一步-回退至发起人-删除表单")
    @pytest.mark.skiprest
    def test_approve_single_form(self, gaolu_login, env_conf):
        with allure.step("查看标段"):
            section_dict = return_section_dict(gaolu_login, env_conf)
        with allure.step("获取资料模板条目列表"):
            resp_temp = Data_template().pageDataTemplateItemUsingGET(gaolu_login, page_size=10000, page_index=1)
            for data in resp_temp.get('source_response')['data']['result']:
                if data['name'] == env_conf['用例配置']['表单审批']['单个表单']['父表单']:
                    template_id1 = data['formTemplateId']
                    template_db_id1 = data['templateCode']
        with allure.step('获取roleName'):
            resp = UserInfo().getUserInfoUsingGET(gaolu_login)
            fullName = resp.get('source_response')['data']['fullName']
        with allure.step('获取发起人用户信息: {0}'.format(fullName)):
            get_userName = Roleandrole().findUsersUsingGET(gaolu_login)
            userinfo_datas = get_userName.get('source_response')['data']
            userIdList = None
            for data in userinfo_datas:
                if data['truename'] == fullName:
                    userIdList = data['id']
        # 检验评定添加父表单
        with allure.step('添加父表单: {0}'.format(env_conf['用例配置']['表单审批']['单个表单']['父表单'])):
            add_parent_sheet_body = {
                "templateId": template_id1,
                "projectNodeId": section_dict[env_conf['用例配置']['表单审批']['单个表单']['subItem']],
                "templateDbId": int(template_db_id1),
                "classifier": "report"
            }
            resp_add_parent_sheet = FormGroup().addFormGroupsPOST(gaolu_login, add_parent_sheet_body)
            waitForStatus(resp_add_parent_sheet, 200, 200, 15)
        with allure.step("断言添加父表单: {0} 成功".format(env_conf['用例配置']['表单审批']['单个表单']['父表单'])):
            add_sheet_result = {"classifier": "report",
                                "projection": "excerpt",
                                "projectNodeId": section_dict[env_conf['用例配置']['增加表单']['subItem']]}
            up_down_resp = FormGroup().formGroupsGET(gaolu_login, add_sheet_result)
            name_id_dict = {}
            for data in up_down_resp.get('source_response')['data']['_embedded']['formGroups']:
                name_id_dict[data['templateName']] = data['id']
            Assertions.assert_in_key(name_id_dict, env_conf['用例配置']['表单审批']['单个表单']['父表单'])
        with allure.step('添加子表单'):
            body = {"classifier": "report",
                    "projection": "excerpt",
                    "projectNodeId": section_dict[env_conf['用例配置']['表单审批']['单个表单']['subItem']]}
            formGroup_resp_dict = {}
            formGroup_resp = FormGroup().formGroupsGET(gaolu_login, body)
            for data in formGroup_resp.get('source_response')['data']['_embedded']['formGroups']:
                formGroup_resp_dict[data['templateName']] = data['_links']['self']['href']

            sheet_name = "测试表单" + base_utils.generate_random_str()
            sheet_body = {"name": sheet_name,
                          "toFormInstance": "",
                          "formGroup": formGroup_resp_dict[env_conf['用例配置']['表单审批']['单个表单']['父表单']]}
            resp_child = FormInstances().formInstancesPOST(gaolu_login, sheet_body)
            waitForStatus(resp_child, 200, 200, 15)
            print('添加子表单: {0} 成功'.format(sheet_name))
        with allure.step('获取子表单templateId'):
            body = return_InstanceSearchBody(gaolu_login, section_dict, env_conf)
            res = FormInstances().formInstanceSearchGET(gaolu_login, body)
            templateId_id = None
            id = None
            edit_href = None
            for data in res.get('source_response')['data']['_embedded']['formInstances']:
                if data['name'] == sheet_name:
                    templateId_id = data['templateId']
                    id = data['id']
                    edit_href = data['_links']['edit']['href']
        with allure.step("获取表单内容"):
            pattern = re.compile(r'[?]id=[A-Za-z0-9]{1,}')
            result = pattern.findall(edit_href)
            edit_id = result[0].split('=')[1]
            ServiceTemplate().rbTemplateGET(env_conf, gaolu_login, templateId_id)
            content_resp = ServiceTemplate().rbInstanceGET(env_conf, gaolu_login, edit_id)
            body = content_resp.get('source_response')['data']
        with allure.step("获取提交表单id"):
            submit_resp = ServiceTemplate().rbInstancePUT(env_conf, gaolu_login, edit_id, body)
            waitForStatus(submit_resp, 200, 200, 15)
            base_utils.file_is_exist(env_conf['用例配置']['表单审批']['单个表单']['文件路径'])
            os.rename(env_conf['用例配置']['表单审批']['单个表单']['文件路径'], "data/" + sheet_name + ".pdf")
            resp = Content().contentGET(gaolu_login, id)
        with allure.step("提交表单内容"):
            res = Content().contentPOST(gaolu_login, resp.get('source_response')['data']['id'],
                                        "data/" + sheet_name + ".pdf")
            os.rename("data/" + sheet_name + ".pdf", env_conf['用例配置']['表单审批']['单个表单']['文件路径'])
            waitForStatus(res, 200, 200, 15)
        with allure.step("发起审批"):
            time = datetime.datetime.now().strftime('%Y-%m-%d')
            body = {"deadline": time, "assignee": userIdList}
            start_approve = ApprovalProcess().starApprovePOST(gaolu_login, body, id)
            waitForStatus(start_approve, 200, 200, 15)
        with allure.step("断言发起审批成功"):
            result_body = return_InstanceSearchBody(gaolu_login, section_dict, env_conf)
            res = FormInstances().formInstanceSearchGET(gaolu_login, result_body)
            for data in res.get('source_response')['data']['_embedded']['formInstances']:
                if data['name'] == sheet_name:
                    status = data['status']
            Assertions.assert_equal_value(status, 'PROCESSING')
        with allure.step("审批"):
            body = {"deadline": time, "comment": "test", "assignee": userIdList}
            pass_approve = ApprovalProcess().passApprovePOST(gaolu_login, body, id)
            waitForStatus(pass_approve, 200, 200, 15)
        with allure.step("查询可退回步骤ID"):
            return_step = ApprovalProcess().returnApproveGET(gaolu_login, id)
            data_arr = return_step.get('source_response')['data']
            for data in data_arr:
                if data['name'] == '发起人':
                    step1 = data['id']
                else:
                    step2 = data['id']
        with allure.step("退回一步"):
            body = {"stepId": step2, "deadline": time, "comment": "pre_step"}
            return_step2 = ApprovalProcess().returnApprovePOST(gaolu_login, body, id)
            waitForStatus(return_step2, 200, 200, 15)
        with allure.step("断言退回一步成功"):
            result_body = return_InstanceSearchBody(gaolu_login, section_dict, env_conf)
            res = FormInstances().formInstanceSearchGET(gaolu_login, result_body)
            for data in res.get('source_response')['data']['_embedded']['formInstances']:
                if data['name'] == sheet_name:
                    status = data['status']
            Assertions.assert_equal_value(status, 'RETURN')
        with allure.step("退回到未发起"):
            body = {"stepId": step1, "deadline": time, "comment": "pre"}
            return_step1 = ApprovalProcess().returnApprovePOST(gaolu_login, body, id)
            waitForStatus(return_step1, 200, 200, 15)
        with allure.step("断言退回到未发起成功"):
            result_body = return_InstanceSearchBody(gaolu_login, section_dict, env_conf)
            res = FormInstances().formInstanceSearchGET(gaolu_login, result_body)
            for data in res.get('source_response')['data']['_embedded']['formInstances']:
                if data['name'] == sheet_name:
                    status = data['status']
            Assertions.assert_equal_value(status, 'UNSTART')
        with allure.step("删除子表单"):
            delete_sheet3 = Sort().formInstancesDELETE(gaolu_login, id)
            waitForStatus(delete_sheet3, 200, 200, 15)
        with allure.step('删除父表单'):
            templateName_id = return_TemplateName_Id(gaolu_login, section_dict, env_conf)
            delete_sheet1 = FormGroup().deleteFormGroupsDELETE(gaolu_login,
                                                               templateName_id[env_conf['用例配置']['表单审批']['单个表单']['父表单']])
            waitForStatus(delete_sheet1, 200, 200, 15)

    @allure.story("删除审批流程-删除前置条件数据")
    @pytest.mark.skiprest
    def test_delete_work_flow(self, gaolu_login, env_conf):
        with allure.step("删除流程"):
            assert_newCreat = Process_template().pageProcessTemplateUsingGET(gaolu_login, page_size=10000, page_index=1)
            result_datas = assert_newCreat.get('source_response')['data']['result']
            key_in_listdict(result_datas, new_flow, 'typeName')
            print("\n新建流程: {0} 成功".format(new_flow))
            processTemplateId = None
            for data in result_datas:
                if data['typeName'] == new_flow:
                    processTemplateId = data['key']
            delete_resp = Process_template().deleteProcessTemplateUsingPOST(gaolu_login, processTemplateId)
            waitForStatus(delete_resp, 200, 200, 15)
        with allure.step('断言删除流程: {0} 成功'.format(new_flow)):
            assert_delete = Process_template().pageProcessTemplateUsingGET(gaolu_login, page_size=10000, page_index=1)
            result_delte = assert_delete.get('source_response')['data']['result']
            key_not_in_listdict(result_delte, new_flow, 'typeName')
            print("删除流程: {0} 成功".format(new_flow))


if __name__ == '__main__':
    pytest.main(["-s", "test_approve_form.py"])
