#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/12/25 15:02
# @Author  : system
# @File    : project.py

import allure


class Projects:
    '''
    项目
    '''

    @allure.step('查询所有有权限的项目')
    def projectsGET(self, item_fixture):
        '''
        查询所有有权限的项目
        :param item_fixture: item fixture,
        :param id:
        '''
        resource = f'/inspection/api/v1/projects'
        response = item_fixture.request('get', resource)
        return response

    @allure.step('项目级别的统计信息')
    def summaryTasksGET(self, item_fixture, projectId=None):
        '''
        项目级别的统计信息
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/summery/tasks/{projectId}'
        response = item_fixture.request('get', resource)
        return response

    @allure.step('项目数据统计（全部）')
    def summaryByProjectGET(self, item_fixture, projectId=None):
        '''
        项目数据统计（全部）
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/summary/byProject/{projectId}'
        response = item_fixture.request('get', resource)
        return response

    @allure.step('新增任务')
    def searchNewTasksGET(self, item_fixture, body):
        '''
        新增任务统计
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/search/newTasks'
        response = item_fixture.request('get', resource, body)
        return response

    @allure.step('待办任务')
    def searchNewToDoGET(self, item_fixture, body):
        '''
        待办任务
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/search/todo'
        response = item_fixture.request('get', resource, body)

    @allure.step('任务追踪')
    def searchTraceGET(self, item_fixture, body):
        '''
        任务追踪
        :param item_fixture: item fixture,
        '''
        resource = f'/inspection/api/v1/formInstances/search/trace'
        response = item_fixture.request('get', resource, body)
        return response
