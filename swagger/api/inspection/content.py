#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : sort.py

import allure
from luban_common import base_utils


class Content:
    '''
    文档
    '''

    # @allure.step('上传表单')
    # def contentPOST(self, item_fixture, id, file, type='pdf', fileType=None):
    #     '''
    #     上次表单
    #     '''
    #     filename = base_utils.getFileName(file)
    #     content_Type = None
    #     if type == "pdf":
    #         content_Type = {'Content-Type': 'application/pdf'}
    #     if fileType is not None:
    #         files = {'file': (filename, open(file, 'rb'), fileType)}
    #     else:
    #         files = {'file': open(file, 'rb')}
    #     resource = f'/inspection/api/v1/content/{id}'
    #     response = item_fixture.request('POST', resource, header=content_Type,
    #                                     files=files)
    #     return response
    @allure.step('上传表单')
    def contentPOST(self, item_fixture, id, file, fileType=None):
        '''
        上次表单
        '''
        filename = base_utils.getFileName(file)
        resource = f'/inspection/api/v1/content/{id}'
        response = item_fixture.request('POST', resource, files={'file': (filename, open(file, 'rb'), fileType)})
        return response

    @allure.step('获取表单')
    def contentGET(self, item_fixture, id):
        '''
        获取表单
        '''
        resource = f'/inspection/api/v1/formInstances/{id}/document'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('下载表单附件')
    def downcontentGET(self, item_fixture, id):
        '''
        下载表单附件
        '''
        resource = f'/inspection/api/v1/binary/{id}'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('上传附件')
    def documentsPOST(self, item_fixture, body):
        '''
        上传附件
        '''
        resource = f'/inspection/api/v1/documents'
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('获取上传附件id')
    def documentsGET(self, item_fixture, id):
        '''
        获取上传附件url
        '''
        resource = f'/inspection/api/v1/documents/{id}'
        response = item_fixture.request('GET', resource)
        return response
