#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/29
# @Author  :  zhangjingwen
# @File    :  test_engineering_template.py
import pytest, allure
from utils.common import waitForStatus, key_in_listdict, key_not_in_listdict
from luban_common.base_assert import Assertions
from luban_common import base_utils
import random
import pprint
from swagger.api.luban_glxx_user.project_template import Project_template


@allure.feature("工程模板")
class TestEngineerTemplate:
    @allure.story("工程划分新建层级-关联表单-删除新建层级")
    def test_engineering_template(self, gaolu_login, env_conf):
        with allure.step("查询工程划分目录"):
            project_tree_resp = Project_template().pageProjectTemplateUsingGET(gaolu_login, pageSize=10000, pageIndex=1)
            # pprint.pprint(project_tree_resp.get('data_totalCount')[0])
            if project_tree_resp.get('data_totalCount')[0] == 0:
                print("工程划分节点为空")
            else:
                allure.attach("工程划分节点有: {0} 条数据".format(project_tree_resp.get('data_totalCount')[0]))
        # with allure.step("添加工程划分节点"):
            # creat_resp = Project_template().saveProjectTemplateUsingPOST(gaolu_login, )


if __name__ == '__main__':
    pytest.main(["-s", "test_engineering_template.py"])
