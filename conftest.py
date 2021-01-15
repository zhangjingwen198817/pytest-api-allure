#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TIME    : 2018/10/9 18:07
# Author  : hubiao
# File    : conftest.py
import os
import time

import pytest
from luban_common import base_requests
from luban_common.msg.weixin import WeiXinMessage
from luban_common.msg.youdu import send_msg
from luban_common.operation import yaml_file

from business import public_login
from swagger.jump import Jump
from utils.utils import file_absolute_path
from py._xmlgen import html


def pytest_addoption(parser):
    '''
    注册Pytest的命令行参数
    :param parser:
    :return:
    '''
    # 自定义的配置选项需要先注册如果，才能在ptest.ini中使用，注册方法如下
    # parser.addini('email_subject', help='test reports email subject')
    parser.addini('globalConf', help='global configuration')
    parser.addini('message_switch', help='message_switch configuration')
    parser.addini('success_message', help='success_message configuration')
    # 注册命令行参数
    group = parser.getgroup("testing environment configuration")
    group.addoption("--lb-driver",
                    default=os.getenv("Pytest_Driver", "chrome"),
                    choices=["chrome", "firefox", "ie"],
                    help="set Browser")
    group.addoption("--lb-base-url",
                    default=os.getenv("Pytest_Base_Url", None),
                    help="base url for the application under test")
    group.addoption("--lb-env",
                    default=os.getenv("Pytest_Env", None),
                    help="set testing environment")


def pytest_configure(config):
    '''
    在测试报告中添加环境信息
    :param config:
    :return:
    '''
    envConf = config.getoption("--lb-env")
    browser = config.getoption("--lb-driver")
    baseUrl = config.getoption("--lb-base-url")
    if hasattr(config, '_metadata'):
        if envConf is not None:
            config._metadata['运行配置'] = envConf
        if browser is not None:
            config._metadata['浏览器'] = browser
        if baseUrl is not None:
            config._metadata['基础URL'] = baseUrl


def pytest_report_header(config):
    '''
    向terminal打印custom环境信息
    :param config:
    :param startdir:
    :return:
    '''
    envConf = config.getoption("--lb-env")
    browser = config.getoption("--lb-driver")
    baseUrl = config.getoption("--lb-base-url")
    if envConf:
        return f"browser: {browser}, baseUrl: {baseUrl}, configuration: {envConf}"


@pytest.fixture(scope="session")
def env_conf(pytestconfig):
    '''
    获取lb-env和globalConf环境配置文件
    :return:
    '''
    envConf = pytestconfig.getoption("--lb-env")
    globalConf = pytestconfig.getini("globalConf")
    if envConf:
        if globalConf:
            return {**yaml_file.get_yaml_data(file_absolute_path(envConf)),
                    **yaml_file.get_yaml_data(file_absolute_path(globalConf))}
        return yaml_file.get_yaml_data(file_absolute_path(envConf))
    else:
        raise RuntimeError("Configuration --lb-env not found")


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    '''
    base URL
    :return:
    '''
    base_url = pytestconfig.getoption('--lb-base-url')
    if base_url:
        return base_url


@pytest.fixture(scope="session")
def global_cache(request):
    '''
    全局缓存，当前执行生命周期有效
    :param request:
    :return:
    '''
    return request.config.cache


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果并发送到对应IM'''
    # 读取配置文件
    envConf = yaml_file.get_yaml_data(file_absolute_path(config.getoption("--lb-env")))
    # 定义测试结果
    total = terminalreporter._numcollected
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    total_times = time.time() - terminalreporter._sessionstarttime
    message_switch = True if config.getini("message_switch") == "True" else False
    success_message = True if config.getini("success_message") == "True" else False
    html_report = config.getoption("--html")
    # 判断是否要发送消息
    if message_switch:
        send = WeiXinMessage()
        youdu_users = envConf.get("youdu_users")
        weixin_toparty = envConf.get("weixin_toparty")
        # 通过jenkins构件时，可以获取到JOB_NAME
        JOB_NAME = "通用" if config._metadata.get('JOB_NAME') is None else config._metadata.get('JOB_NAME')
        if failed + error != 0:
            content = f"共执行 {total} 条用例\n有 {passed} 条执行成功\n有 {failed} 条执行失败\n有 {error} 条执行出错\n有 {skipped} 条跳过"
            if weixin_toparty:
                send.send_message_textcard(title=f"警告！{JOB_NAME} 巡检出现异常", content=content, toparty=weixin_toparty)
            if youdu_users:
                send_msg(title=f"警告！{JOB_NAME} 巡检出现异常", content=content, sendTo=youdu_users + "_FAIL", session=0,
                         file=html_report)
        elif success_message:
            content = f"共执行 {total} 条用例，全部执行通过，耗时 {round(total_times, 2)} 秒"
            if weixin_toparty:
                send.send_message_textcard(title=f"恭喜，{JOB_NAME} 巡检通过，请放心", content=content, toparty=weixin_toparty)
            if youdu_users:
                send_msg(title=f"恭喜，{JOB_NAME} 巡检通过，请放心", content=content, sendTo=youdu_users + "_PASS", session=0,
                         file=html_report)


@pytest.fixture(scope="session")
def bimadmin_login(env_conf, global_cache):
    '''
    BIM Aadmin运维管理系统登录
    :return:
    '''
    BimAdminLogin = public_login.BimAdmin(env_conf).login()
    yield BimAdminLogin


@pytest.fixture(scope="session")
def center_cas(env_conf, global_cache):
    '''
    获取Center CAS登录凭证
    :return:
    '''
    public_login.Center(env_conf["center"]["username"], env_conf["center"]["password"], env_conf, global_cache).login()
    yield


@pytest.fixture(scope="session")
def center_builder(center_cas, env_conf, global_cache):
    '''
    获取Builder登录凭证
    :return:
    '''
    CenterBuilder = base_requests.Send(global_cache.get("builder", False), env_conf, global_cache)
    yield CenterBuilder


@pytest.fixture(scope="session")
def center_process(center_cas, env_conf, global_cache):
    '''
    获取Process登录凭证
    :return:
    '''
    CenterProcess = base_requests.Send(global_cache.get("process", False), env_conf, global_cache)
    yield CenterProcess


@pytest.fixture(scope="session")
def iworks_app_cas(env_conf, global_cache):
    '''
    获取PDS登录凭证
    :return:
    '''
    public_login.IworksApp(env_conf["iworksApp"]["username"], env_conf["iworksApp"]["password"], env_conf,
                           global_cache).login()
    yield


@pytest.fixture(scope="session")
def lbbv(iworks_app_cas, env_conf, global_cache):
    '''
    获取LBBV登录凭证
    :return:
    '''
    LBBV = base_requests.Send(global_cache.get("lbbv", False), env_conf, global_cache)
    yield LBBV


@pytest.fixture(scope="session")
def bimco(iworks_app_cas, env_conf, global_cache):
    '''
    获取BimCO登录凭证
    :return:
    '''
    BimCO = base_requests.Send(global_cache.get("bimco", False), env_conf, global_cache)
    yield BimCO


@pytest.fixture(scope="session")
def process(iworks_app_cas, env_conf, global_cache):
    '''
    获取Process登录凭证
    :return:
    '''
    Process = base_requests.Send(global_cache.get("lbprocess", False), env_conf, global_cache)
    yield Process


@pytest.fixture(scope="session")
def pds_common(iworks_app_cas, env_conf, global_cache):
    '''
    获取PDSCommon登录凭证
    :return:
    '''
    PDSCommon = base_requests.Send(global_cache.get("pdscommon", False), env_conf, global_cache)
    yield PDSCommon


@pytest.fixture(scope="session")
def pds_doc(iworks_app_cas, env_conf, global_cache):
    '''
    获取pdsdoc登录凭证
    :return:
    '''
    PDSDoc = base_requests.Send(global_cache.get("pdsdoc", False), env_conf, global_cache)
    yield PDSDoc


@pytest.fixture(scope="session")
def builder_common_business_data(iworks_app_cas, env_conf, global_cache):
    '''
    获取BusinessData登录凭证
    :return:
    '''
    builderCommonBusinessData = base_requests.Send(global_cache.get("buildercommonbusinessdata", False), env_conf,
                                                   global_cache)
    yield builderCommonBusinessData


@pytest.fixture(scope="session")
def bimapp_login(env_conf, global_cache):
    '''
    BIMApp 通行证系统登录
    :return:
    '''
    BimAppLogin = public_login.Bimapp(env_conf["bimapp"]["username"], env_conf["bimapp"]["password"], env_conf,
                                      global_cache).login()
    yield BimAppLogin


@pytest.fixture(scope="session")
def myluban_web_login(env_conf, global_cache):
    '''
    Myluban web 登录
    :return:
    '''
    MylubanWebLogin = public_login.MylubanWeb(env_conf["MylubanWeb"]["username"], env_conf["MylubanWeb"]["password"],
                                              env_conf, global_cache).login()
    yield MylubanWebLogin


@pytest.fixture(scope="session")
def bussiness_login(env_conf, global_cache):
    '''
    Bussiness 业务管理系统登录
    :return:
    '''
    BussinessLogin = public_login.Bussiness(env_conf["Bussiness"]["username"], env_conf["Bussiness"]["password"],
                                            env_conf,
                                            global_cache).login()
    yield BussinessLogin


@pytest.fixture(scope="session")
def lubansoft_login(env_conf, global_cache):
    '''
    算量软件登录
    :return:
    '''
    LubansoftLogin = public_login.LubanSoft(env_conf["lubansoft"]["username"], env_conf["lubansoft"]["password"],
                                            env_conf,
                                            global_cache).login()
    yield LubansoftLogin


@pytest.fixture(scope="session")
def iworks_web_cas(env_conf, global_cache):
    '''
    获取cas登录凭证
    :return:
    '''
    public_login.IworksWeb(env_conf["iworksWeb"]["username"], env_conf["iworksWeb"]["password"], env_conf,
                           global_cache).login()
    yield


@pytest.fixture(scope="session")
def iworks_web_common(iworks_web_cas, env_conf, global_cache):
    '''
    获取common登录凭证
    :return:
    '''
    resule = base_requests.Send(global_cache.get("pdscommon", False), env_conf, global_cache)
    # 处理第一次 302跳转接口不能是post、put、update接口,必须用get接口调用
    Jump().jump(resule, resource='/rs/jump')
    yield resule


@pytest.fixture(scope="session")
def iworks_web_process(iworks_web_cas, env_conf, global_cache):
    '''
    获取process登录凭证
    :return:
    '''
    resule = base_requests.Send(global_cache.get("LBprocess", False), env_conf, global_cache)
    # 处理第一次 302跳转接口不能是post、put、update接口,必须用get接口调用
    Jump().jump(resule, resource='/process/jump')
    yield resule


@pytest.fixture(scope="session")
def iworks_web_businessdata(iworks_web_cas, env_conf, global_cache):
    '''
    获取businessdata登录凭证
    :return:
    '''
    resule = base_requests.Send(global_cache.get("BuilderCommonBusinessdata", False), env_conf, global_cache)
    # 处理第一次 302跳转接口不能是post、put、update接口,必须用get接口调用
    Jump().jump(resule, resource='/jump')
    yield resule


@pytest.fixture(scope="session")
def iworks_web_plan(iworks_web_cas, env_conf, global_cache):
    '''
    获取plan登录凭证
    :return:
    '''
    resule = base_requests.Send(global_cache.get("LBSP", False), env_conf, global_cache)
    # 处理第一次 302跳转接口不能是post、put、update接口,必须用get接口调用
    Jump().jump(resule, resource='/rs/jump')
    yield resule


@pytest.fixture(scope="session")
def iworks_web_bimco(iworks_web_cas, env_conf, global_cache):
    '''
    获取bimco登录凭证
    :return:
    '''
    resule = base_requests.Send(global_cache.get("bimco", False), env_conf, global_cache)
    # 处理第一次 302跳转接口不能是post、put、update接口,必须用get接口调用
    Jump().jump(resule, resource='/rs/co/jump')
    yield resule


@pytest.fixture(scope="session")
def iworks_web_pdsdoc(iworks_web_cas, env_conf, global_cache):
    '''
    获取doc登录凭证
    :return:
    '''
    resule = base_requests.Send(global_cache.get("pdsdoc", False), env_conf, global_cache)
    # 处理第一次 302跳转接口不能是post、put、update接口,必须用get接口调用
    Jump().jump(resule, resource='/rs/jump')
    yield resule


@pytest.fixture(scope="session")
def token(env_conf, global_cache):
    '''
    获取登录凭证Token
    :return:
    '''
    resule = public_login.Token(env_conf["iworksWeb"]["username"], env_conf["iworksWeb"]["password"], env_conf,
                                global_cache)
    yield resule.login()
    # resule.logout()


@pytest.fixture(scope="session")
def openapi_motor_token(token, env_conf, global_cache):
    '''
    获取openapi_motor_token
    :return:
    '''
    resule = public_login.OpenApiMotorToken(token).login()
    yield resule


@pytest.fixture(scope="session")
def gaolu_login(env_conf, global_cache):
    '''
    gaolu系统登录
    '''
    GaolLulogin = public_login.Gaolu(env_conf["Gaolu"]["username"], env_conf["Gaolu"]["password"], env_conf,
                                     global_cache).login()
    yield GaolLulogin


@pytest.fixture(scope="session")
def gaolu_login_luban(env_conf, global_cache):
    '''
    gaolu_login_luban系统登录
    '''
    GaolLulogin_luban = public_login.Gaolu_luban(env_conf["Gaolu"]["username"], env_conf["Gaolu"]["password"], env_conf,
                                                 global_cache).login()
    yield GaolLulogin_luban


def pytest_sessionstart(session):
    session.failednames = set()


def pytest_runtest_makereport(item, call):
    markers = {marker.name for marker in item.iter_markers()}
    if call.excinfo is not None and 'skiprest' in markers:
        item.session.failednames.add(item.originalname)


def pytest_runtest_setup(item):
    markers = {marker.name for marker in item.iter_markers()}
    if item.originalname in item.session.failednames and 'skiprest' in markers:
        pytest.skip(item.name)
