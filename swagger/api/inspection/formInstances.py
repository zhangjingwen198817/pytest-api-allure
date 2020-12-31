#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/25
# @Author  :  zhangjingwen
# @File    :  formInstances
import allure


class FormInstances:
    '''
    表单实例
    '''

    @allure.step('根据分组查询表单实例')
    def formInstanceSearchGET(self, item_fixture, body):
        '''
        根据分组查询表单实例
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/search/paged'
        response = item_fixture.request('GET', resource, params=body)
        return response

    @allure.step('表单数量统计')
    def byFormGroupIdGET(self, item_fixture, body):
        '''
        表单数量统计
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/search/byFormGroupId'
        response = item_fixture.request('GET', resource, params=body)
        return response

    @allure.step('添加表单')
    def formInstancesPOST(self, item_fixture, body):
        '''
        添加表单
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances'
        response = item_fixture.request('post', resource, body)
        return response

    @allure.step('关联表单文件')
    def byFormGroupIdPOST(self, item_fixture, formInstanceId=None):
        '''
        关联表单文件
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/document'
        response = item_fixture.request('PUT', resource)
        return response

    @allure.step('关联附件')
    def byFormGroupIdPOST(self, item_fixture, body, formInstanceId=None):
        '''
        关联附件
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/attachments'
        response = item_fixture.request('PUT', resource, body)
        return response

    @allure.step('修改表单名称')
    def byFormGroupIdPOST(self, item_fixture, body, formInstanceId=None):
        '''
        修改表单名称
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}'
        response = item_fixture.request('PATCH', resource, body)
        return response
