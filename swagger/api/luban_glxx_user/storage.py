#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : storage.py

import allure

class Storage:
    '''
    存储模块
    '''

    @allure.step('删除接口')
    def deleteFileUsingDELETE(self, item_fixture, fileId=None):
        '''
        删除接口
        :param item_fixture: item fixture,
        :param fileId: 文件id
        '''
        resource = f'/luban-glxx-user/storage/delete/{fileId}'
        response = item_fixture.request('DELETE', resource)
        return response

    @allure.step('下载接口')
    def downloadFileUsingGET(self, item_fixture, fileId=None):
        '''
        下载接口
        :param item_fixture: item fixture,
        :param fileId: 文件id
        '''
        resource = f'/luban-glxx-user/storage/download/{fileId}'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('上传接口')
    def uploadUsingPOST(self, item_fixture):
        '''
        上传接口
        :param item_fixture: item fixture,
        '''
        resource = f'/luban-glxx-user/storage/upload'
        response = item_fixture.request('POST', resource)
        return response

    @allure.step('上传Excel接口(2020四川公路工程质检评定用表)')
    def uploadExcelUsingPOST(self, item_fixture):
        '''
        上传Excel接口(2020四川公路工程质检评定用表)
        :param item_fixture: item fixture,
        '''
        resource = f'/luban-glxx-user/storage/upload/excel'
        response = item_fixture.request('POST', resource)
        return response

    @allure.step('上传Excel接口(2020四川公路工程竣工归档用表)')
    def uploadExcel2UsingPOST(self, item_fixture):
        '''
        上传Excel接口(2020四川公路工程竣工归档用表)
        :param item_fixture: item fixture,
        '''
        resource = f'/luban-glxx-user/storage/upload/excel2'
        response = item_fixture.request('POST', resource)
        return response

