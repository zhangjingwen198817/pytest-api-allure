#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 14:38
# @Author  : system
# @File    : process_template.py

import allure

class Process_template:
    '''
    流程模版模块
    '''

    @allure.step('复制流程模版接口')
    def copyProcessTemplateUsingPOST(self, item_fixture, procName=None, procKey=None):
        '''
        复制流程模版接口
        :param item_fixture: item fixture,
        :param procKey: 流程模版key
        :param procName: 流程模版名称
        '''
        resource = f'/luban-glxx-user/process/template/copy'
        body = {'procKey': procKey, 'procName': procName}
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('删除流程模版接口')
    def deleteProcessTemplateUsingPOST(self, item_fixture, prockeys=None):
        '''
        删除流程模版接口
        :param item_fixture: item fixture,
        :param prockeys: 流程模版key
        '''
        resource = f'/luban-glxx-user/process/template/delete'
        query_params = {'prockeys': prockeys}
        response = item_fixture.request('POST', resource, params = query_params)
        return response

    @allure.step('流程模版历史版本接口')
    def listProcessTemplateHistoryUsingGET(self, item_fixture, templKey=None):
        '''
        流程模版历史版本接口
        :param item_fixture: item fixture,
        :param templKey: 流程模版key
        '''
        resource = f'/luban-glxx-user/process/template/list_history'
        query_params = {'templKey': templKey}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('流程模版列表接口（分页）')
    def pageProcessTemplateUsingGET(self, item_fixture, switch_status=None, keyword=None, page_size=None, page_index=None):
        '''
        流程模版列表接口（分页）
        :param item_fixture: item fixture,
        :param keyword: 关键字
        :param page_index: 分页索引
        :param page_size: 分页条数
        :param switch_status: 流程启用状态(0:不启用 1:启用   默认查询所有状态)
        '''
        resource = f'/luban-glxx-user/process/template/page'
        query_params = {'keyword': keyword, 'page_index': page_index, 'page_size': page_size, 'switch_status': switch_status}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('流程模版详情接口(根据id)')
    def getProcessTemplateByIdUsingGET(self, item_fixture, id=None):
        '''
        流程模版详情接口(根据id)
        :param item_fixture: item fixture,
        :param id: 流程模版id
        '''
        resource = f'/luban-glxx-user/process/template/query_info_by_id/{id}'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('新增或修改流程模版接口')
    def saveOrUpdateProcessTemplateUsingPOST(self, item_fixture, remark=None, nodeList=None, lineList=None, typeName=None, sponsorType=None, id=None, sponsorRoleList=None, sponsorUserList=None):
        '''
        新增或修改流程模版接口
        :param item_fixture: item fixture,
        :param lineList: 流程节点的连线
        :param nodeList: 流程节点列表
        :param id: 流程模板id（新增时为空,更新时传流程模板id）
        :param remark: 备注
        :param sponsorRoleList: 发起人角色id列表
        :param sponsorType: 发起人类型，0：全员可发起 1:指定类型发起
        :param sponsorUserList: 发起人用户名列表
        :param typeName: 流程类型名称
        '''
        resource = f'/luban-glxx-user/process/template/save_or_update'
        body = {'flowChart': {'lineList': lineList, 'nodeList': nodeList}, 'id': id, 'remark': remark, 'sponsorRoleList': sponsorRoleList, 'sponsorType': sponsorType, 'sponsorUserList': sponsorUserList, 'typeName': typeName}
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('修改流程模版启用状态接口')
    def updateProcessTemplateEnableUsingPOST(self, item_fixture, templKey=None):
        '''
        修改流程模版启用状态接口
        :param item_fixture: item fixture,
        :param templKey: 流程模版key
        '''
        resource = f'/luban-glxx-user/process/template/update_enable'
        body = {'templKey': templKey}
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('流程模版详情接口')
    def getProcessTemplateUsingGET(self, item_fixture, templKey=None):
        '''
        流程模版详情接口
        :param item_fixture: item fixture,
        :param templKey: 流程模版key
        '''
        resource = f'/luban-glxx-user/process/template/{templKey}'
        response = item_fixture.request('GET', resource)
        return response

