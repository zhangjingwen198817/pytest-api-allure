#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : data_template.py

import allure

class Data_template:
    '''
    资料模版模块
    '''

    @allure.step('资料模版条目列表接口（分页）')
    def pageDataTemplateItemUsingGET(self, item_fixture, page_size=None, filterNoFormTemplate=None, type=None, page_index=None, templateCode=None):
        '''
        资料模版条目列表接口（分页）
        :param item_fixture: item fixture,
        :param filterNoFormTemplate: 是否过滤掉未绑定表单模板的数据(1- 过滤，2-不过滤)
        :param page_index: 分页索引
        :param page_size: 分页条数
        :param templateCode: 表单库编码(20000000 - 2020四川公路工程质检评定用表，20000010 - 2020四川公路工程竣工归档用表)
        :param type: 类型
        '''
        resource = f'/luban-glxx-user/data/template/item/page'
        query_params = {'filterNoFormTemplate': filterNoFormTemplate, 'page_index': page_index, 'page_size': page_size, 'templateCode': templateCode, 'type': type}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('资料模版条目关联列表接口')
    def listDataTemplateItemRefUsingGET(self, item_fixture, fromItemIds=None):
        '''
        资料模版条目关联列表接口
        :param item_fixture: item fixture,
        :param fromItemIds: 条目ID
        '''
        resource = f'/luban-glxx-user/data/template/item/rel/list'
        query_params = {'fromItemIds': fromItemIds}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('更新资料模版条目关联表单模版接口')
    def updateDataTemplateItem2FormTemplateUsingPOST(self, item_fixture, formTemplateId=None, itemId=None):
        '''
        更新资料模版条目关联表单模版接口
        :param item_fixture: item fixture,
        :param formTemplateId: 表单模版ID
        :param itemId: 资料条目ID
        '''
        resource = f'/luban-glxx-user/data/template/item/update_formtemplate'
        body = {'formTemplateId': formTemplateId, 'itemId': itemId}
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('更新资料模版条目关联流程模版接口')
    def updateDataTemplateItem2ProcessTemplateUsingPOST(self, item_fixture, templateCode=None, processTemplateId=None, itemId=None):
        '''
        更新资料模版条目关联流程模版接口
        :param item_fixture: item fixture,
        :param item2formTemplateItemIdList: 资料模版条目ID
        :param itemId: 资料模版条目ID
        :param processTemplateId: 流程模版ID
        :param templateCode: 模板库编码
        '''
        resource = f'/luban-glxx-user/data/template/item/update_processtemplate'
        body = {'item2formTemplateItemIdList': [{'itemId': itemId, 'processTemplateId': processTemplateId}], 'templateCode': templateCode}
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('更新资料模版条目关联接口')
    def updateDataTemplateItemRelUsingPOST(self, item_fixture, fromFormTemplateId=None, toFormTemplateIds=None):
        '''
        更新资料模版条目关联接口
        :param item_fixture: item fixture,
        :param dataTemplateItemRefList: 资料-模版-条目关联
        :param fromFormTemplateId: 高级表单ID
        :param toFormTemplateIds: 关联高级表单ID
        '''
        resource = f'/luban-glxx-user/data/template/item/update_rel'
        body = {'dataTemplateItemRefList': [{'fromFormTemplateId': fromFormTemplateId, 'toFormTemplateIds': toFormTemplateIds}]}
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('资料模板库列表接口（分页）')
    def pageDataTemplateUsingGET(self, item_fixture, pageSize=50, pageIndex=None):
        '''
        资料模板库列表接口（分页）
        :param item_fixture: item fixture,
        :param pageIndex: 分页索引
        :param pageSize: 分页条数
        '''
        resource = f'/luban-glxx-user/data/template/page'
        query_params = {'pageIndex': pageIndex, 'pageSize': pageSize}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

