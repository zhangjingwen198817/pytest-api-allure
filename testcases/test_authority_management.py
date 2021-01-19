#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2021/1/18
# @Author  :  zhangjingwen
# @File    :  test_authority_management.py
import pytest, allure
from swagger.api.luban_glxx_user.permission import Permission
import jsonpath, copy
from utils.common import waitForStatus
import pprint


@allure.feature("权限管理")
class TestAuthorityManagement:
    @allure.story("权限管理-修改")
    def test_authority_management(self, gaolu_login_permission, gaolu_login_luban, env_conf):
        with allure.step('获取修改角色信息'):
            resp = Permission().findLikeRoleUsingGET(gaolu_login_luban, page_size=10000,
                                                     rolename=env_conf['用例配置']['权限管理']['角色名称'], page_index=1)
            role_id = None
            for data in resp.get('source_response')['data']['result']:
                if data['rolename'] == '乐西管理员':
                    role_id = data['id']
        with allure.step('查询权限列表接口'):
            # 查看接口是否可用
            Permission().findPermissionMenuUsingGET(gaolu_login_luban, roleId=role_id, moduleType=0)
            resp_1 = Permission().findPermissionMenuUsingGET(gaolu_login_luban, roleId=role_id, moduleType=0)
            data = resp_1.get('source_response')['data']
            delete_value = {'perm': jsonpath.jsonpath(data,
                                                      '$..[?(@.menuname=="质检评定")]..[?(@.menuname=="开工报告")]..[?(@.menuname=="添加表单")]..perms')[
                0]}
            value = jsonpath.jsonpath(data, '$..perms')
            dict_body = []
            dict_body.append({
                "roleId": role_id,
                "moduleType": 0
            })
            for data in value:
                if data != '':
                    dict_body.append({
                        "perm": data
                    })
            old_body = copy.deepcopy(dict_body)
            for data in dict_body:
                if data == delete_value:
                    dict_body.remove(data)
        with allure.step('取消勾选保存'):
            save_resp = Permission().saveRoleMenuUsingPOST(gaolu_login_permission, dict_body)
            waitForStatus(save_resp, 200, 200, 15)
        with allure.step('恢复权限设置'):
            save_resp = Permission().saveRoleMenuUsingPOST(gaolu_login_permission, old_body)
            waitForStatus(save_resp, 200, 200, 15)


if __name__ == '__main__':
    pytest.main(["-s", "test_authority_management.py"])
