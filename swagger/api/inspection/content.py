#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : sort.py

import allure


class Content:
    '''
    文档
    '''

    @allure.step('上次表单')
    def contentPOST(self, item_fixture, id, file):
        '''
        上次表单
        '''
        resource = f'/inspection/api/v1/content/{id}'
        response = item_fixture.request('POST', resource, header={'Content-Type': 'application/pdf'},
                                        files={'file': open(file, 'rb')})
        return response

    @allure.step('获取表单')
    def contentGET(self, item_fixture, id):
        '''
        获取表单
        '''
        resource = f'/inspection/api/v1/formInstances/{id}/document'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('获取表单')
    def downcontentGET(self, item_fixture, id):
        '''
        获取表单
        '''
        resource = f'/inspection/api/v1/binary/{id}'
        response = item_fixture.request('GET', resource)
        return response
