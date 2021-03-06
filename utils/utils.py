#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2020/7/5 9:47
# @Author  : hubiao
# @File    : base_utils.py
import os
import allure
from luban_common import base_utils

def file_absolute_path(rel_path):
    '''
    通过文件相对路径，返回文件绝对路径
    :param rel_path: 相对于项目根目录的路径，如data/check_lib.xlsx
    :return:
    '''
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path,'..', rel_path)
    return file_path

@allure.step("上传文件")
def upFiles(item_fixture, resource, filePath):
    '''
    封装上传文件方法，要求传二个参数，上传成功返回文件UUID
    item_fixture：item fixture
    resource：请求的地址
    filePath：要上传的文件，相对于项目根目录，如 data/Doc/Lubango20191205.docx
    :return: 返回文件uuid
    '''
    file = base_utils.file_is_exist(filePath)
    try:
        response = item_fixture.request('post', resource, files={'file': open(file, 'rb')})
        return response["Response_body"]
    except Exception as e:
        raise FileNotFoundError(f"上传文件失败，错误原因:{e}")