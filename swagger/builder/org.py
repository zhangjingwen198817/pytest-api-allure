#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/5/9 21:24
# @Author  : hubiao
# @File    : org_controller.py

import allure

class Org:
    '''
    组织机构、项目部相关接口
    '''
    @allure.step("查询组织机构树（包括项目部）")
    def org_nodes(self,CenterBuilder):
        '''
        查询组织机构树（包括项目部）
        '''
        resource = '/org/nodes'
        response = CenterBuilder.request('get', resource)
        return response

    @allure.step("创建新的组织机构")
    def org_orgId_add(self, CenterBuilder,orgId,orgName,dataType=1,type=0):
        '''
        创建新的组织机构
        orgId：组织机构节点ID
        orgName：创建的组织机构名称
        dataType：数据类型,1、组织数据类型2、项目部门数据类型
        type：组织类型 0:分公司,2:部门(已废弃)
        '''
        resource = f'/org/{orgId}/subs'
        body = {
            "name": orgName,
            "remarks": orgName+"的备注",
            "labels": [],
            "latitude": "121.517675",
            "longitude": "31.312552",
            "dataType":dataType,
            "type": type
        }
        response = CenterBuilder.request('post', resource, body)
        return response

    @allure.step("编辑组织机构")
    def org_orgId_edit(self, CenterBuilder,orgId,orgName):
        '''
        编辑组织机构
        orgId：组织机构节点ID
        orgName：创建的组织机构名称
        '''
        resource = f'/org/{orgId}'
        body = {
            "labels": [],
            "latitude": "121.517675",
            "longitude": "31.312552",
            "name": orgName,
            "remarks": orgName+"的备注"
        }
        response = CenterBuilder.request('put', resource, body)
        return response

    @allure.step("删除组织机构、项目部")
    def org_orgId_del(self, CenterBuilder,orgId):
        '''
        删除组织机构
        orgId：组织机构节点ID
        '''
        resource = f'/org/{orgId}'
        response = CenterBuilder.request('delete', resource)
        return response