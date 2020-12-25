#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : auth.py

import allure

class Auth:
    '''
    鉴权模块
    '''

    @allure.step('登录信息查询接口')
    def getUserInfoUsingGET(self, item_fixture):
        '''
        登录信息查询接口
        :param item_fixture: item fixture,
        '''
        resource = f'/luban-glxx-user/auth/info'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('建管跳转登录接口')
    def loginFromJsglUsingGET(self, item_fixture, jsgl_token=None):
        '''
        建管跳转登录接口
        :param item_fixture: item fixture,
        :param jsgl_token: 建管系统token
        '''
        resource = f'/luban-glxx-user/auth/jsgl_redirect_login'
        query_params = {'jsgl_token': jsgl_token}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('帐号密码登录接口（独立登录）')
    def loginUsingPOST(self, item_fixture, username=None, password=None):
        '''
        帐号密码登录接口（独立登录）
        :param item_fixture: item fixture,
        :param password: 密码（md5加密）
        :param username: 账户
        '''
        resource = f'/luban-glxx-user/auth/login'
        body = {'password': password, 'username': username}
        response = item_fixture.request('POST', resource, body)
        return response

