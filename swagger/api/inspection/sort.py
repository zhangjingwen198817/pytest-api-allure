#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : sort.py

import allure


class Sort:
    '''
    排序
    '''

    @allure.step('表单分组')
    def formGroupsPOST(self, item_fixture, id=None):
        '''
        建管跳转登录接口
        :param item_fixture: item fixture,
        :param jsgl_token: 建管系统token
        '''
        resource = f'/inspection/api/v1/formGroups/{id}'
        response = item_fixture.request('post', resource)
        return response

    @allure.step('表单实例分组')
    def formInstancesPOST(self, item_fixture, id=None):
        '''
        登录信息查询接口
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{id}'
        response = item_fixture.request('post', resource)
        return response

    @allure.step(' 删除表单实例')
    def formInstancesDELETE(self, item_fixture, id=None):
        '''
        删除表单实例
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{id}'
        response = item_fixture.request('delete', resource)
        return response
