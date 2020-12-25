#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : inspection_userinfo.py

import allure


class User:
    '''
    用户模块
    '''

    @allure.step('获取当前用户信息')
    def getUserInfoUsingGET(self, item_fixture):
        '''
        登录信息查询接口
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/userinfo'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('获取指定id用户信息')
    def getUserInfoUsingIdGET(self, item_fixture, identifier=None):
        '''
        获取指定id用户信息
        :param item_fixture: item fixture,
        :param identifier: 指定id
        '''
        resource = f'/inspection/userinfo/{identifier}'
        response = item_fixture.request('GET', resource)
        return response
