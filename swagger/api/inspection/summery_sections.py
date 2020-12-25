#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : summery_sections.py

import allure


class Sections:
    '''
    标段
    '''

    @allure.step('查询标段')
    def sectionsGET(self, item_fixture):
        '''
        查询标段
        :param item_fixture: item fixture,
        :param id:
        '''
        resource = f'/inspection/api/v1/sections'
        response = item_fixture.request('get', resource)
        return response

    @allure.step('表单（总）数据统计（标段）')
    def summaryPeriodGET(self, item_fixture):
        '''
        表单（总）数据统计（标段）
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/summery/period'
        response = item_fixture.request('get', resource)
        return response

    @allure.step('项目数据统计（标段）')
    def summaryBySectionGET(self, item_fixture, body):
        '''
        项目数据统计（标段）
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/summary/bySection'
        response = item_fixture.request('get', resource, body)
        return response

    @allure.step('项目概况')
    def summaryByUnitGET(self, item_fixture, body):
        '''
        项目概况
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/summary/byUnit'
        response = item_fixture.request('get', resource, body)
        return response
