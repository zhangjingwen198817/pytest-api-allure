#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/25
# @Author  :  zhangjingwen
# @File    :  commissioned_form.py


import allure


class CommissionedForm:
    @allure.step('创建委托实例')
    def formInstancesPOST(self, item_fixture, instance):
        '''
        创建委托实例
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{instance}'
        response = item_fixture.request('POST', resource)
        return response

    @allure.step('删除委托对象')
    def formInstancesPOST(self, item_fixture, instance):
        '''
        删除委托对象
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formDelegates/{instance}'
        response = item_fixture.request('POST', resource)
        return response

    @allure.step('查询委托实例')
    def formInstancesGET(self, item_fixture, instance):
        '''
        查询委托实例
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formDelegates/{instance}'
        response = item_fixture.request('GET', resource)
        return response
