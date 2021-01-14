#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2021/1/13
# @Author  :  zhangjingwen
# @File    :  home_page.py

import allure


class HomePage:
    @allure.step('获取表单统计数据')
    def getSummaryPeriodGET(self, item_fixture, body):
        '''
        获取表单统计数据
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/summary/period'
        response = item_fixture.request('GET', resource, params=body)
        return response

    @allure.step('获取项目统计数据')
    def getSummarybySectionGET(self, item_fixture, body):
        '''
        获取表单统计数据
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/summary/bySection'
        response = item_fixture.request('GET', resource, params=body)
        return response

    @allure.step('获取项目概况数据')
    def getSummarybyUnitGET(self, item_fixture, body):
        '''
        获取表单统计数据
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/summary/byUnit'
        response = item_fixture.request('GET', resource, params=body)
        return response

    @allure.step('代发')
    def searchNewTasksGET(self, item_fixture, body):
        '''
        代发
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/search/newTasks'
        response = item_fixture.request('get', resource, params=body)
        return response

    @allure.step('待办任务')
    def searchNewToDoGET(self, item_fixture, body):
        '''
        待办任务
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/search/todo'
        response = item_fixture.request('get', resource, params=body)

    @allure.step('已办')
    def searchTraceGET(self, item_fixture, body):
        '''
        已办
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/search/trace'
        response = item_fixture.request('get', resource, params=body)
        return response
