#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/25
# @Author  :  zhangjingwen
# @File    :  projectNodes_searcg_all

import allure


class ProjectNodes:
    '''
    用户模块
    '''

    @allure.step('获取当前用户信息')
    def getUserInfoUsingGET(self, item_fixture, sectionId=None):
        '''
        项目节点接口
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/projectNodes/search/all'
        response = item_fixture.request('GET', resource, params=sectionId)
        return response
