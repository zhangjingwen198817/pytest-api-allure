#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : service_template.py

import allure
import pprint


class ServiceTemplate:
    '''
    获取表单文档内容
    '''

    # @allure.step('获取表单文档内容')
    # def rbTemplateGET(self, env_conf, item_fixture, templateId):
    #     '''
    #     登录信息查询接口
    #     :param item_fixture: item fixture,
    #     '''
    #     resource = f"{env_conf['url_tmp']}/report/v2.0/service/rb/template/{templateId}"
    #     response = item_fixture.request('GET', resource)
    #     return response
    #
    # @allure.step('获取表单文档数据')
    # def rbInstanceGET(self, env_conf, item_fixture, instanceId):
    #     '''
    #     获取表单文档数据
    #     :param item_fixture: item fixture,
    #     '''
    #     resource = f"{env_conf['url_tmp']}/report/v2.0/service/rb/instance/{instanceId}"
    #     response = item_fixture.request('GET', resource)
    #     return response
    #
    # @allure.step('提交表单文档数据')
    # def rbInstancePUT(self, env_conf, item_fixture, instanceId, body):
    #     '''
    #     提交表单文档数据
    #     :param item_fixture: item fixture,
    #     '''
    #     resource = f"{env_conf['url_tmp']}/report/v2.0/service/rb/instance/{instanceId}"
    #     response = item_fixture.request('PUT', resource, body)
    #     return response
    @allure.step('获取表单文档内容')
    def rbTemplateGET(self, item_fixture, templateId):
        '''
        登录信息查询接口
        :param item_fixture: item fixture,
        '''
        resource = f"/report/v2.0/service/rb/template/{templateId}"
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('获取表单文档数据')
    def rbInstanceGET(self, item_fixture, instanceId):
        '''
        获取表单文档数据
        :param item_fixture: item fixture,
        '''
        resource = f"/report/v2.0/service/rb/instance/{instanceId}"
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('提交表单文档数据')
    def rbInstancePUT(self, item_fixture, instanceId, body):
        '''
        提交表单文档数据
        :param item_fixture: item fixture,
        '''
        resource = f"/report/v2.0/service/rb/instance/{instanceId}"
        response = item_fixture.request('PUT', resource, body)
        return response
