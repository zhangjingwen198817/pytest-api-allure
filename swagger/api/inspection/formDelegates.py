#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/25
# @Author  :  zhangjingwen
# @File    :  formDelegates.py


import allure


class DelegatesForm:
    @allure.step('创建委托实例')
    def createFormDelegatesPOST(self, item_fixture, body):
        '''
        创建委托实例
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formDelegates'
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('删除委托对象')
    def deleteFormDelegatesDELETE(self, item_fixture, instance):
        '''
        删除委托对象
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formDelegates/{instance}'
        response = item_fixture.request('DELETE', resource)
        return response

    @allure.step('查询委托实例')
    def searchFormDelegatesPOST(self, item_fixture, instance):
        '''
        查询委托实例
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formDelegates/{instance}'
        response = item_fixture.request('GET', resource)
        return response
