#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/25
# @Author  :  zhangjingwen
# @File    :  test_longin
import pytest, allure
from swagger.api.inspection.inspection_userinfo import UserInfo
from swagger.api.luban_glxx_user.roleAndRole import Roleandrole
from swagger.api.luban_glxx_user.process_template import Process_template
from swagger.api.luban_glxx_user.data_template import Data_template
import pprint
from luban_common.base_assert import Assertions
from luban_common import base_utils
import random
from utils.common import waitForStatus, key_in_listdict, key_not_in_listdict


@allure.feature("流程设置")
class TestFlow:
    @allure.story("新建流程-关联表单-删除流程")
    def test_flow_setting(self, gaolu_login, gaolu_login_luban, env_conf):
        new_flow = "流程测试" + base_utils.generate_random_str()
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
                if data['name'] == env_conf['用例配置']['表单关联']:
                    itemId = data['id']
        with allure.step('添加需要关联的表单到原有关联表单json'):
            for data in list_body:
                if data['itemId'] == itemId:
                    list_body.remove(data)
            list_body.append({"itemId": itemId,
                              "processTemplateId": processTemplateId})
        with allure.step('关联流程:{0} 到表单 {1}'.format(new_flow, env_conf['用例配置']['表单关联'])):
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
                if data['name'] == env_conf['用例配置']['表单关联']:
                    Assertions.assert_equal_value(data['processTemplateId'], processTemplateId)
            print('关联流程:{0} 到表单: {1} 成功'.format(new_flow, env_conf['用例配置']['表单关联']))
        with allure.step("删除流程"):
            delete_resp = Process_template().deleteProcessTemplateUsingPOST(gaolu_login_luban, processTemplateId)
            waitForStatus(delete_resp, 200, 200, 15)
        with allure.step('断言删除流程: {0} 成功'.format(new_flow)):
            assert_delete = Process_template().pageProcessTemplateUsingGET(gaolu_login_luban, page_size=10000,
                                                                           page_index=1)
            result_delte = assert_delete.get('source_response')['data']['result']
            key_not_in_listdict(result_delte, new_flow, 'typeName')
            print("删除流程: {0} 成功".format(new_flow))


if __name__ == '__main__':
    pytest.main(["-s", "test_workflow_setting.py"])
