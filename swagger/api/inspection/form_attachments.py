#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/25
# @Author  :  zhangjingwen
# @File    :  form_attachments


import allure


class FormAttachments:
    @allure.step('查询表单文件')
    def formInstancesGET(self, item_fixture, formInstanceId=None):
        '''
        查询表单文件
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/document'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('查询表单附件')
    def formInstancesGET(self, item_fixture, formInstanceId=None):
        '''
        查询表单附件
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/attachments'
        response = item_fixture.request('GET', resource)
        return response
