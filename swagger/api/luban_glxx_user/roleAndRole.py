#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : roleAndRole.py

import allure

class Roleandrole:
    '''
    角色用户模块
    '''

    @allure.step('查询角色列表接口')
    def findRolesUsingGET(self, item_fixture, rolename=None):
        '''
        查询角色列表接口
        :param item_fixture: item fixture,
        :param rolename: rolename
        '''
        resource = f'/luban-glxx-user/roleAndRole/findRoles'
        query_params = {'rolename': rolename}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('查询用户列表接口')
    def findUsersUsingGET(self, item_fixture, username=None):
        '''
        查询用户列表接口
        :param item_fixture: item fixture,
        :param username: username
        '''
        resource = f'/luban-glxx-user/roleAndRole/findUsers'
        query_params = {'username': username}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

