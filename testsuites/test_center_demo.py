#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/5/13 17:12
# @Author  : hubiao
# @File    : test_center_demo.py

import pytest
import allure
from luban_common.base_assert import Assertions
from swagger.builder.org import Org
from luban_common import base_utils


@allure.feature("组织机构、项目部")
class TestOrg:
    '''
    组织机构、项目部相关接口
    '''

    def setup_class(self):
        '''
        定义接口需要用到的字段信息
        '''
        pass

    @allure.story("组织机构")
    @allure.title("编辑组织机构")
    @pytest.mark.parametrize("dataType", [1,2])
    def test_org_edit(self, center_builder, dataType):
        '''
        编辑组织机构接口测试
        '''
        # 查询组织机构树
        response = Org().org_nodes(center_builder)
        rootID = response["result_id"][response["result_root"].index(True)]
        # 创建组织机构
        orgName = '接口测试新增机构' + base_utils.generate_random_str()
        org_add = Org().org_orgId_add(center_builder, rootID, orgName=orgName, dataType=dataType)
        org_id = org_add["result_id"][0]
        org_pathId = org_add["result_pathId"][0]
        org_path = org_add["result_path"][0]
        # 编辑组织机构
        newOrgName = '接口测试编辑机构' + base_utils.generate_random_str()
        org_edit = Org().org_orgId_edit(center_builder, orgId=org_id, orgName=newOrgName)
        # 查询组织机构树
        response = Org().org_nodes(center_builder)
        try:
            Assertions().assert_all_code(response, 200, 200)
            # 验证编辑组织接口是否正常
            Assertions().assert_equal_value(org_edit["result_id"][0],org_id)
            Assertions().assert_equal_value(org_edit["result_name"][0],newOrgName)
            Assertions().assert_equal_value(org_edit["result_type"][0],0)
            Assertions().assert_equal_value(org_edit["result_parentId"][0],rootID)
            Assertions().assert_equal_value(org_edit["result_root"][0],False)
            Assertions().assert_equal_value(org_edit["result_dataType"][0],dataType)
            # 验证组织树接口是否返回了新加的组织
            Assertions().assert_in_value(response["result_id"],org_id)
            Assertions().assert_equal_value(response["result_name"][response["result_id"].index(org_id)],newOrgName)
            Assertions().assert_equal_value(response["result_type"][response["result_id"].index(org_id)],0)
            Assertions().assert_equal_value(response["result_parentId"][response["result_id"].index(org_id)],rootID)
            Assertions().assert_equal_value(response["result_root"][response["result_id"].index(org_id)],False)
            Assertions().assert_equal_value(response["result_pathId"][response["result_id"].index(org_id)],org_pathId)
            Assertions().assert_equal_value(response["result_path"][response["result_id"].index(org_id)],org_path)
            Assertions().assert_equal_value(response["result_dataType"][response["result_id"].index(org_id)],dataType)
        finally:
            # 删除组织机构
            Org().org_orgId_del(center_builder, orgId=org_id)


if __name__ == '__main__':
    pytest.main(["-s", "test_center_demo.py"])