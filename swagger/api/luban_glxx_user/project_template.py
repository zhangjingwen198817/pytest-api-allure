#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : project_template.py

import allure

class Project_template:
    '''
    工程模板模块
    '''

    @allure.step('工程模板和资料模板条目绑定接口')
    def bindDataTemplate2ProjectTemplateUsingPOST(self, item_fixture, projectTemplateId=None, dataTemplateItemId=None, type=None):
        '''
        工程模板和资料模板条目绑定接口
        :param item_fixture: item fixture,
        :param projectTemplateDataTemplates: 资料模板
        :param dataTemplateItemId: 资料模板条目id
        :param type: 表单分类,1：开工报告，2：质量检验（施工），3：交工评定（施工），4：质量检验（监理），5：交工评定（监理）
        :param projectTemplateId: 工程模板id
        '''
        resource = f'/luban-glxx-user/project_template/bind/dataTemplate_projectTemplate'
        body = {'projectTemplateDataTemplates': [{'dataTemplateItemId': dataTemplateItemId, 'type': type}], 'projectTemplateId': projectTemplateId}
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('删除工程模板接口')
    def deleteProjectTemplateUsingDELETE(self, item_fixture, ids=None):
        '''
        删除工程模板接口
        :param item_fixture: item fixture,
        :param ids: 工程模板id集合
        '''
        resource = f'/luban-glxx-user/project_template/delete'
        query_params = {'ids': ids}
        response = item_fixture.request('DELETE', resource, params = query_params)
        return response

    @allure.step('根据id查询工程模板接口')
    def getProjectTemplateByIdUsingGET(self, item_fixture, id=None):
        '''
        根据id查询工程模板接口
        :param item_fixture: item fixture,
        :param id: 工程模板id
        '''
        resource = f'/luban-glxx-user/project_template/getById'
        query_params = {'id': id}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('查询工程模板接口(分页)')
    def pageProjectTemplateUsingGET(self, item_fixture, pageSize=50, pageIndex=None):
        '''
        查询工程模板接口(分页)
        :param item_fixture: item fixture,
        :param pageIndex: 分页索引
        :param pageSize: 分页条数
        '''
        resource = f'/luban-glxx-user/project_template/page'
        query_params = {'pageIndex': pageIndex, 'pageSize': pageSize}
        response = item_fixture.request('GET', resource, params = query_params)
        return response

    @allure.step('添加工程模板接口')
    def saveProjectTemplateUsingPOST(self, item_fixture, body):
        '''
        添加工程模板接口
        :param item_fixture: item fixture,
        :param nameList: 工程名称
        :param parentId: 父节点id，一级节点为0
        '''
        resource = f'/luban-glxx-user/project_template/save'
        # body = {'nameList': nameList, 'parentId': parentId}
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('工程模板和资料模板条目取消绑定接口')
    def unBindDataTemplate2ProjectTemplateUsingDELETE(self, item_fixture, projectTemplateId=None, dataTemplateItemId=None, type=None):
        '''
        工程模板和资料模板条目取消绑定接口
        :param item_fixture: item fixture,
        :param dataTemplateItemId: 资料模板条目id
        :param projectTemplateId: 工程模板id
        :param type: 表单分类,1：开工报告，2：质量检验（施工），3：交工评定（施工），4：质量检验（监理），5：交工评定（监理）
        '''
        resource = f'/luban-glxx-user/project_template/unbind/dataTemplate_projectTemplate'
        body = {'dataTemplateItemId': dataTemplateItemId, 'projectTemplateId': projectTemplateId, 'type': type}
        response = item_fixture.request('DELETE', resource, body)
        return response

    @allure.step('修改工程模板接口')
    def updateProjectTemplateUsingPOST(self, item_fixture, id=None, name=None):
        '''
        修改工程模板接口
        :param item_fixture: item fixture,
        :param id: 工程模板id
        :param name: 工程名称
        '''
        resource = f'/luban-glxx-user/project_template/update'
        body = {'id': id, 'name': name}
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('修改工程模板排序接口')
    def updateProjectTemplateSortUsingPOST(self, item_fixture, id=None, offset=None):
        '''
        修改工程模板排序接口
        :param item_fixture: item fixture,
        :param id: 工程模板id
        :param offset: 偏移量
        '''
        resource = f'/luban-glxx-user/project_template/updateSort'
        body = {'id': id, 'offset': offset}
        response = item_fixture.request('POST', resource, body)
        return response

