#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : permission.py

import allure

class Permission:
    '''
    功能权限模块
    '''

    @allure.step('角色和权限绑定接口(新的)')
    def saveRoleMenuUsingPOST(self, item_fixture, roleId=None, moduleType=None, perm=None):
        '''
        角色和权限绑定接口(新的)
        :param item_fixture: item fixture,
        :param moduleType: 系统模块，0：质检评定，1：电子档案
        :param perm: 权限码
        :param roleId: 角色id
        '''
        resource = f'/luban-glxx-user/permission/saveMenu'
        body = [{'moduleType': moduleType, 'perm': perm, 'roleId': roleId}]
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('查询权限列表接口')
    def findPermissionUsingGET(self, item_fixture, roleId=None):
        '''
        查询权限列表接口
        :param item_fixture: item fixture,
        :param roleId: roleId
        '''
        resource = f'/luban-glxx-user/permission/select'
        query_params = {'roleId': roleId}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('模糊查询角色列表接口带分页')
    def findLikeRoleUsingGET(self, item_fixture, page_size=None, rolename=None, page_index=None):
        '''
        模糊查询角色列表接口带分页
        :param item_fixture: item fixture,
        :param page_index: page_index
        :param page_size: 分页条数
        :param rolename: rolename
        '''
        resource = f'/luban-glxx-user/permission/select/page'
        query_params = {'page_index': page_index, 'page_size': page_size, 'rolename': rolename}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('查询权限列表接口(新的)')
    def findPermissionMenuUsingGET(self, item_fixture, roleId=None, moduleType=None):
        '''
        查询权限列表接口(新的)
        :param item_fixture: item fixture,
        :param moduleType: 菜单类型id
        :param roleId: 角色id
        '''
        resource = f'/luban-glxx-user/permission/selectMenu'
        query_params = {'moduleType': moduleType, 'roleId': roleId}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

