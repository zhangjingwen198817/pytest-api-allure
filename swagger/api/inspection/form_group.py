#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/25
# @Author  :  zhangjingwen
# @File    :  form_group

import allure


class FormGroup:
    '''
    用户模块
    '''

    @allure.step('查询表单分组')
    def formGroupsGET(self, item_fixture, body):
        '''
        查询表单分组
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formGroups/search/list'
        response = item_fixture.request('GET', resource, params=body)
        return response

    @allure.step('表单数量统计')
    def formInstancesByProjectNodeGET(self, item_fixture, body):
        '''
        表单数量统计
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/search/byProjectNode'
        response = item_fixture.request('GET', resource, params=body)
        return response

    @allure.step('添加表单分组')
    def addFormGroupsPOST(self, item_fixture, body):
        '''
        添加表单分组
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formGroups'
        response = item_fixture.request('post', resource, body)
        return response

    @allure.step('查询可应用于的模板')
    def searchTemplatesGET(self, item_fixture, body, templateDbId=None, templateId=None):
        '''
        查询可应用于的模板
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/templateDbs/{templateDbId}/templates/{templateId}/to'
        response = item_fixture.request('post', resource, params=body)
        return response
