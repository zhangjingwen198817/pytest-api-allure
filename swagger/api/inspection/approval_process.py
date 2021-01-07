#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    :  2020/12/25
# @Author  :  zhangjingwen
# @File    :  approval_process

import allure


class ApprovalProcess:
    '''
    流程审批
    '''

    @allure.step('任务认领')
    def claimGET(self, item_fixture, formInstanceId=None):
        '''
        任务认领
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/claim'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('发起或者审批时指定候选人')
    def candidatesPOST(self, item_fixture, body, formInstanceId=None):
        '''
        发起或者审批时指定候选人
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/candidates'
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('发起审批')
    def starApprovePOST(self, item_fixture, body, formInstanceId=None):
        '''
        发起审批
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/start'
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('审批')
    def passApprovePOST(self, item_fixture, body, formInstanceId=None):
        '''
        审批
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/pass'
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('查询可退回得步骤')
    def returnApproveGET(self, item_fixture, formInstanceId=None):
        '''
        查询可退回得步骤
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/return'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('退回')
    def returnApprovePOST(self, item_fixture, body, formInstanceId=None):
        '''
        退回
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/return'
        response = item_fixture.request('POST', resource, body)
        return response

    @allure.step('查询审批日志')
    def passGET(self, item_fixture, body, formInstanceId=None):
        '''
        查询审批日志
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/logs'
        response = item_fixture.request('GET', resource, body)
        return response

    @allure.step('查询待审批的步骤')
    def passGET(self, item_fixture, formInstanceId=None):
        '''
        查询审批日志
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/pass'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('查询下一步审批人员')
    def passGET(self, item_fixture, formInstanceId=None):
        '''
        查询下一步审批人员
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/next'
        response = item_fixture.request('GET', resource)
        return response

    @allure.step('查询流程版本号')
    def passGET(self, item_fixture, formInstanceId=None):
        '''
        查询流程版本号
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/{formInstanceId}/version'
        response = item_fixture.request('GET', resource)
        return response
