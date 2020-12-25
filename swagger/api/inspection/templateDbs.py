#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/25
# @Author  :  zhangjingwen
# @File    :  templateDbs
import allure


class ProjectNodes:
    '''
    模板库
    '''

    @allure.step('根据模板分类查询支持的模板库')
    def templateDbsGET(self, item_fixture, body):
        '''
        根据模板分类查询支持的模板库
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/templateDbs'
        response = item_fixture.request('GET', resource, params=body)
        return response

    @allure.step('查询模板库树节点')
    def templateDbsGET(self, item_fixture, body, templateDbId=None):
        '''
        查询模板库树节点
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/templateDbs/{templateDbId}'
        response = item_fixture.request('GET', resource, params=body)
        return response
