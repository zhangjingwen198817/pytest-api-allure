#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/1/2 11:19
# @Author  : hubiao
# @File    : public_login.py
import json
import re
import xmltodict

from urllib.parse import quote
from luban_common import base_utils
from luban_common import base_requests
from luban_common.base_assert import Assertions
from luban_common.global_map import Global_Map


class BimAdmin:
    '''
    BimAdmin 登录类
    '''

    def __init__(self, envConf):
        self.header = envConf["headers"]["urlencoded_header"]
        self.body = envConf["sysadmin"]["logininfo"]
        self.BimAdminLogin = base_requests.Send(envConf["sysadmin"]["host"], envConf)

    def login(self):
        '''
        后台登录
        :param BimAadminLogin:
        :return:
        '''
        resource = "/login.htm"
        response = self.BimAdminLogin.request("post", resource, self.body, self.header)
        Assertions().assert_equal_value(response["status_code"], 200)
        return self.BimAdminLogin


class Center:
    '''
    Center CAS登录类
    '''

    def __init__(self, centerusername, centerpassword, envConf, global_cache):
        self.cache = global_cache
        self.productId = envConf['centerProductid']
        self.username = centerusername if isinstance(centerusername, int) else quote(centerusername)
        self.password = centerpassword
        self.header = envConf["headers"]["plain_header"]
        self.CenterLogin = base_requests.Send(envConf['pds'], envConf, global_cache=self.cache)

    def getServerUrl(self):
        '''
        获取服务器地址信息
        '''
        resource = '/rs/centerLogin/serverurl'
        response = self.CenterLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        assert len(response["serverURL"]) != 0
        for server in response["serverURL"]:
            number = response["serverURL"].index(server)
            self.cache.set(response["serverName"][number], response["serverURL"][number])

    def getDeployType(self):
        '''
        获取部署类型
        :return:
        '''
        resource = '/rs/centerLogin/deployType'
        response = self.CenterLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        deployType = response["Response_body"]
        self.cache.set('deployType', deployType)

    def getLT(self):
        '''
        获取LT
        :return:
        '''
        resource = '/login'
        response = self.CenterLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        html = response["Response_body"]
        pattern = 'value="LT(.+?)" />'
        lt = re.findall(pattern, html)[0]
        return lt

    def getTGC(self):
        '''
        获取TGC，依赖getLT接口
        :return:
        '''
        resource = '/login'  # ?service=+serverlist[6]["serverURL"].replace("://","%3A%2F%2F")
        body = f'_eventId=submit&execution=e1s1&lt=LT{self.getLT()}&password={self.password}&productId={self.productId}&submit=%25E7%2599%25BB%25E5%25BD%2595&username={self.username}'
        response = self.CenterLogin.request('post', resource, body, self.header)
        Assertions().assert_equal_value(response["status_code"], 200)

    def getCompanyList(self):
        '''
        获取企业id列表
        :return:
        '''
        resource = "/rs/centerLogin/companyList"
        body = {"password": self.password, "username": self.username}
        response = self.CenterLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        if len(response["epid"]) > 0:
            self.cache.set('CenterEpid', response["epid"][0])

    def switchCompany(self):
        '''
        切换到指定企业，依赖getCompanyList接口
        :return:
        '''
        resource = "/rs/centerLogin/login"
        body = {"epid": self.cache.get("CenterEpid", False), "password": self.password, "username": self.username}
        response = self.CenterLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)

    def login(self):
        '''
        Center登录
        :return:
        '''
        self.getServerUrl()
        self.getDeployType()
        self.getTGC()
        self.getCompanyList()
        self.switchCompany()


class IworksApp:
    '''
    BV CAS登录类
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.productId = envConf['iworksAppProductId']
        self.username = username if isinstance(username, int) else quote(username)
        self.password = password
        self.header = envConf["headers"]["plain_header"]
        self.clientVersion = envConf["iworksApp"]["clientVersion"]
        self.casLogin = base_requests.Send(envConf['pds'], envConf, global_cache=self.cache)
        self.epid = ''

    def getServerUrl(self):
        '''
        获取服务器地址信息
        '''
        resource = '/rs/casLogin/serverUrl'
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        assert len(response["serverURL"]) != 0
        for server in response["serverURL"]:
            number = response["serverURL"].index(server)
            self.cache.set(response["serverName"][number], response["serverURL"][number])

    def getLT(self):
        '''
        获取LT
        :return:
        '''
        resource = '/login'
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        html = response["Response_body"]
        pattern = 'value="LT(.+?)" />'
        lt = re.findall(pattern, html)[0]
        return lt

    def getTGC(self):
        '''
        获取TGC，依赖getLT接口
        :return:
        '''
        resource = '/login'  # ?service=+serverlist[6]["serverURL"].replace("://","%3A%2F%2F")
        body = f'_eventId=submit&execution=e1s1&lt=LT{self.getLT()}&password={self.password}&productId={self.productId}&submit=%25E7%2599%25BB%25E5%25BD%2595&username={self.username}'
        response = self.casLogin.request('post', resource, body, self.header)
        Assertions().assert_equal_value(response["status_code"], 200)

    def getCompanyList(self):
        '''
        获取企业id列表
        :return:
        '''
        resource = "/rs/casLogin/companyList"
        body = {"password": self.password, "userName": self.username, "clientVersion": self.clientVersion,
                "phoneModel": "国行(A1865)、日行(A1902)iPhone X", "platform": "ios", "innetIp": "192.168.7.184",
                "productId": self.productId,
                "token": "f54d6c8c13445a723a2863a72d460e5aec48010560ea2351bda6474de5164899", "systemVersion": "13.5.1",
                "hardwareCodes": "3465192946d57f13482640578c77ffa77d1f66a4"}
        response = self.casLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        if len(response["enterpriseId"]) > 0:
            self.cache.set('iworksAppEpid', response["enterpriseId"][0])
            self.epid = response["enterpriseId"][0]
            return self.epid

    def switchCompany(self):
        '''
        切换到指定企业
        :return:
        '''
        resource = f"/rs/casLogin/changeEnterprise/{self.epid}"
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)

    def login(self):
        '''
        登录BV CAS流程方法
        :return:
        '''
        self.getServerUrl()
        self.getTGC()
        self.getCompanyList()
        self.switchCompany()


class Iworks:
    '''
    iWorks CAS登录类
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        # self.rf = ManageConfig().getConfig(self.section)
        # self.wf = ManageConfig()
        self.productId = envConf['iWorksProductId']
        self.username = username if isinstance(username, int) else quote(username)
        self.password = password
        self.header = envConf["headers"]["soap_header"]
        self.header1 = envConf["headers"]["urlencoded_header"]
        self.casLogin = base_requests.Send(envConf['pds'], envConf, global_cache=self.cache)
        self.epid = ''

    def getServerUrl(self):
        '''
        获取服务器地址信息
        '''
        resource = '/webservice/lbws/casLoginService'
        body = '''<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:SASS="http://login.webservice.login.sso.lubansoft.com/">
    <SOAP-ENV:Body>
        <SASS:getServUrl/>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''
        response = self.casLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        convertedXml = xmltodict.parse(response['Response_body'])
        Response_serverURL = \
            base_utils.ResponseData(convertedXml)['soap:Envelope_soap:Body_ns2:getServUrlResponse_return_list'][0]
        assert len(Response_serverURL) != 0, "serverURL不能为空"
        for server in Response_serverURL:
            self.cache.set(dict(server)["serverName"], dict(server)["serverURL"])

    def getLT(self):
        '''
        获取LT
        :return:
        '''
        resource = '/login'
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        html = response["Response_body"]
        pattern = 'value="LT(.+?)" />'
        lt = re.findall(pattern, html)[0]
        return lt

    def getTGC(self):
        '''
        获取TGC，依赖getLT接口
        :return:
        '''
        resource = '/login'  # ?service=+serverlist[6]["serverURL"].replace("://","%3A%2F%2F")
        body = f'_eventId=submit&execution=e1s1&lt=LT{self.getLT()}&password={self.password}&productId={self.productId}&submit=%25E7%2599%25BB%25E5%25BD%2595&username={self.username}'
        response = self.casLogin.request('post', resource, body, self.header1)
        Assertions().assert_equal_value(response["status_code"], 200)

    def getCompanyList(self):
        '''
        获取企业id列表
        :return:
        '''
        resource = "/webservice/lbws/casLoginService"
        body = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:log="http://login.webservice.login.sso.lubansoft.com/">
    <soapenv:Header/>
    <soapenv:Body>
        <log:getCompanyList/>
    </soapenv:Body>
</soapenv:Envelope>'''
        response = self.casLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        convertedXml = xmltodict.parse(response['Response_body'])
        enterpriseId = base_utils.ResponseData(convertedXml)[
            'soap:Envelope_soap:Body_ns2:getCompanyListResponse_return_enterpriseId']
        print(enterpriseId)
        if len(enterpriseId) > 0:
            epids = eval(json.dumps(enterpriseId))[0]
            self.cache.set('epid', epids)
            self.epid = epids
            return self.epid

    def switchCompany(self):
        '''
        切换到指定企业
        :return:
        '''
        resource = f"/rs/casLogin/changeEnterprise/{self.epid}"
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)

    def casLoginService(self):
        '''
        登录获取权限码（cas）casLogin(登录cas)
        :return:
        '''
        resource = "/webservice/lbws/casLoginService"
        body = f'''
       <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:log="http://login.webservice.login.sso.lubansoft.com/">
    <soapenv:Header/>
    <soapenv:Body>
        <log:casLogin>
            <!--Optional:-->
            <param>
                <!--Optional:-->
                <!--Optional:-->
                <epid>{self.epid}</epid>
                <!--Optional:-->
                <hardwareCodes>eb4af7830e478a6191b38f7687a81e81-f6d5e226a50d8a7ff4cd47252efaa128</hardwareCodes>
                <!--Optional:-->
                <!--Optional:-->
                <innetIp>172.16.21.147</innetIp>
                <platform>pc64</platform>
                <version>1.0.0</version>
            </param>
        </log:casLogin>
    </soapenv:Body>
</soapenv:Envelope>
'''
        response = self.casLogin.request('post', resource, body, self.header)
        Assertions().assert_equal_value(response["status_code"], 200)
        convertedXml = xmltodict.parse(response['Response_body'])
        Response_authCodes = base_utils.ResponseData(convertedXml)[
            'soap:Envelope_soap:Body_ns2:casLoginResponse_return_clientAuthGroupResultList_list']
        print(Response_authCodes)

    def login(self):
        '''
        登录BV CAS流程方法
        :return:
        '''
        self.getServerUrl()
        self.getTGC()
        self.getCompanyList()
        self.casLoginService()


class IworksWeb:
    '''
    iworks web 登录类
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.productId = envConf['iworksWebProductId']
        self.username = username
        self.password = password
        self.header = envConf["headers"]["json_header"]
        self.casLogin = base_requests.Send(envConf['pds'], envConf, global_cache=self.cache)
        self.epid = ''

    def getServerUrl(self):
        '''
        获取服务器地址信息
        '''
        resource = '/rs/casLogin/serverUrl'
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        assert len(response["serverURL"]) != 0
        for server in response["serverURL"]:
            number = response["serverURL"].index(server)
            self.cache.set(response["serverName"][number], response["serverURL"][number])

    def getTGC(self):
        '''
        获取TGT
        :return:
        '''
        resource = '/rs/v2/tickets/tgt?'
        body = {"password": self.password, "username": self.username, "productId": self.productId}
        response = self.casLogin.request('post', resource, body, self.header)
        Assertions().assert_equal_value(response["status_code"], 200)

    def getCompanyList(self):
        '''
        获取企业id列表
        :return:
        '''
        resource = "/rs/v2/casLogin/listCompany"
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        if len(response["data_enterpriseId"]) > 0:
            self.cache.set('iworksWebEpid', response["data_enterpriseId"][0])
            self.epid = response["data_enterpriseId"][0]
            Global_Map().set_map("epid", response["data_enterpriseId"][0])
            Global_Map().set_map("enterpriseName", response["data_enterpriseName"][0])
            return self.epid

    def switchCompany(self):
        '''
        切换到指定企业
        :return:
        '''
        resource = f"/rs/casLogin/casLogin"
        body = {"epid": self.epid}
        response = self.casLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)

    def enterpriseInfo(self):
        '''
        获取企业信息
        :return:
        '''
        resource = f"/rs/casLogin/enterpriseInfo"
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)

    def authgroup(self):
        '''
        获取授权
        :return:
        '''
        resource = f"/rs/v2/casLogin/authgroup/{self.productId}"
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)

    def login(self):
        '''
        iworks web流程方法
        :return:
        '''
        self.getServerUrl()
        self.getTGC()
        self.getCompanyList()
        self.switchCompany()
        self.enterpriseInfo()
        self.authgroup()


class Token:
    '''
    token登录流程
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.productId = envConf['iworksWebProductId']
        self.username = username
        self.password = password
        self.header = envConf["headers"]["json_header"]
        self.casLogin = base_requests.Send(envConf['auth_url'], envConf, global_cache=self.cache)
        self.epid = ''
        self.Authorization = ""

    def getToken(self):
        '''
        获取token接口
        '''
        resource = "/auth-server/auth/token"
        body = {"loginType": "CLIENT_WEB", "password": self.password, "username": self.username}
        response = self.casLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        if len(response.get("data")) > 0:
            self.Authorization = response.get("data")[0]
            Global_Map().set_map("Authorization", response.get("data")[0])
        # 验证token中账号是否正确
        userinfo = base_utils.FromBase64(self.Authorization.split(".")[1])
        Assertions().assert_in_value(userinfo, self.username)

    def getEnterprises(self):
        '''
        获取企业列表
        '''
        resource = f"/auth-server/auth/enterprises/productId/{self.productId}"
        response = self.casLogin.request('get', resource, header={"Authorization": self.Authorization},
                                         flush_header=True)
        Assertions().assert_equal_value(response["status_code"], 200)
        if len(response.get("data_epid")) > 0:
            self.epid = response.get("data_epid")[0]
            Global_Map().set_map("epid", response.get("data_epid")[0])
            Global_Map().set_map("enterpriseName", response.get("data_enterpriseName")[0])

    def enterprise(self):
        '''
        切换企业
        '''
        resource = f"/auth-server/auth/enterprise"
        body = {"epid": self.epid}
        response = self.casLogin.request('put', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)

    def logout(self):
        '''
        退出登录接口
        '''
        resource = "/auth-server/auth/logout"
        response = self.casLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)

    def login(self):
        self.getToken()
        self.getEnterprises()
        self.enterprise()
        return self.casLogin


class OpenAPI:
    '''
    开放平台登录类
    '''

    def __init__(self, apikey, apisecret, envConf, global_cache):
        self.cache = global_cache
        self.apikey = apikey
        self.apisecret = apisecret
        self.username = envConf["openapi"]['username']
        self.OpenAPIToken = base_requests.Send(envConf["openapi"]['host'], envConf, global_cache=self.cache)

    def login(self):
        '''
        登录获取token
        '''
        resource = f"/rs/token/{self.apikey}/{self.apisecret}/{self.username}"
        response = self.OpenAPIToken.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        # 获取到响应的token并更新到header中
        header = json.loads(self.OpenAPIToken.header)
        header.update({"token": response["data"][0]})
        self.OpenAPIToken.header = json.dumps(header)
        return self.OpenAPIToken


class OpenApiMotorToken:
    '''
    开放平台motor token获取
    '''

    def __init__(self, token):
        self.token = token

    def getMotorClientTokenUsingGET(self, token):
        '''
        获取访问motor模型的token
        :param item_fixture: item fixture,
        '''
        resource = f'/auth-server/auth/motor/client_token'
        response = token.request('GET', resource)
        return response

    def validateToken(self, item_fixture, WebToken):
        '''
        验证token是否有效
        :param item_fixture: item fixture
        '''
        header = {"access_token": WebToken}
        resource = f'/openapi/motor/v1.0/service/uc/auth/validateToken'
        response = item_fixture.request('GET', resource, header=header, flush_header=True)
        return response

    def login(self):
        '''
        登录获取token
        '''
        GetToken = self.getMotorClientTokenUsingGET(self.token).get("data")[0]
        self.validateToken(self.token, WebToken=GetToken)
        return self.token


class Bimapp:
    '''
    Bimapp 登录类
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.username = base_utils.ToBase64(username)
        self.password = password
        self.token = ''
        self.AcAddress = ''
        self.BimappLogin = base_requests.Send(envConf["bimapp"]['host'], envConf, global_cache=self.cache)

    def getCookie(self):
        '''
        获取cookie
        '''
        resource = "/login.htm"
        response = self.BimappLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)

    def getAcAddress(self):
        '''
        获取ac地址
        '''
        resource = "/getAcAddress.htm"
        response = self.BimappLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        if response["Response_body"] is not None:
            self.AcAddress = response["Response_body"]

    def gettoken(self):
        '''
        获取token
        '''
        resource = f"{self.AcAddress}/rs/rest/user/login/{self.username}/{self.password}"
        response = self.BimappLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)
        self.token = response['loginToken'][0]

    def doLoginWithToken(self):
        '''
         token登录
        '''
        resource = f"/bimapp/doLoginWithToken.htm?token={self.token}"
        response = self.BimappLogin.request('get', resource)
        Assertions().assert_equal_value(response["status_code"], 200)

    def login(self):
        '''
        登录
        '''
        self.getCookie()
        self.getAcAddress()
        self.gettoken()
        self.doLoginWithToken()
        return self.BimappLogin


class MylubanWeb:
    '''
    MylubanWeb 登录类
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.username = username
        self.password = password
        self.MylubanWebLogin = base_requests.Send(envConf["MylubanWeb"]['host'], envConf, global_cache=self.cache)

    def login(self):
        '''
        MylubanWeb登录
        :param MylubanWebLogin:
        :return:
        '''
        resource = "/myluban/rest/login"
        body = {"username": self.username, "password": self.password}
        response = self.MylubanWebLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        return self.MylubanWebLogin


class Bussiness:
    '''
    Bussiness 登录类
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.username = username
        self.password = password
        self.BussinessLogin = base_requests.Send(envConf["Bussiness"]['host'], envConf, global_cache=self.cache)

    def login(self):
        '''
        Bussiness 登录
        :param BussinessLogin:
        :return:
        '''
        resource = "/login"
        body = {"username": self.username, "password": self.password}
        response = self.BussinessLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        return self.BussinessLogin


class LubanSoft:
    '''
    lubansoft 登录类
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.username = username
        self.password = password
        self.header = envConf["headers"]["soap_header"]
        self.lubansoftLogin = base_requests.Send(envConf["lubansoft"]['host'], envConf)

    def login(self):
        '''
        lubansoft rest 登录
        :return:
        '''
        resource = "/webservice/clientInfo/LBClient"
        body = '''<?xml version="1.0" encoding="UTF-8"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:ns1="http://cloudnorm.webservice.lbapp.lubansoft.com/" xmlns:ns10="http://webservice.clientcomponent.lbapp.lubansoft.com/" xmlns:ns11="http://webservice.cloudcomponent.lbapp.lubansoft.com/" xmlns:ns12="http://webservice.lbim.lbapp.lubansoft.com/" xmlns:ns13="http://webservice.common.lbapp.lubansoft.com/" xmlns:ns14="http://webservice.costlib.lbapp.lubansoft.com/" xmlns:ns15="http://webservice.usergrade.lbapp.lubansoft.com/" xmlns:ns16="http://webservice.cloudautoset.lbapp.lubansoft.com/" xmlns:ns17="http://webservice.lbcert.lbapp.lubansoft.com/" xmlns:ns18="http://webservice.clientinfo.lbapp.lubansoft.com/" xmlns:ns19="http://webservice.onlineservice.lbapp.lubansoft.com/" xmlns:ns2="http://lbmsg.webservice.lbapp.lubansoft.com/" xmlns:ns20="http://webservice.localbim.lbapp.lubansoft.com/" xmlns:ns21="http://webservice.adimage.lbapp.lubansoft.com/" xmlns:ns22="http://webservice.banbankDrainage.lbapp.lubansoft.com/" xmlns:ns3="http://upgrade.webservice.lbapp.lubansoft.com/" xmlns:ns4="http://cloudpush.webservice.lbapp.lubansoft.com/" xmlns:ns5="http://common.webservice.lbapp.lubansoft.com/" xmlns:ns6="http://clientInfo.webservice.lbapp.lubansoft.com/" xmlns:ns7="http://validate.webservice.lbapp.lubansoft.com/" xmlns:ns8="http://LBUFS.webservice.lbapp.lubansoft.com/" xmlns:ns9="http://webservice.dataserver.LBUFS.lubansoft.com/">
        <SOAP-ENV:Header><LBTag>Kick</LBTag><LBSessionId></LBSessionId></SOAP-ENV:Header>
        <SOAP-ENV:Body>
        <ns6:login>
        <LBLoginParam>
        <computerName>DESKTOP-S2CJPRR</computerName>
        <hardwareCodes>0d80c194d531820c71de04a3998b435e-4ece03d1c7f03a151b241cbd455505ef</hardwareCodes>
        <intranet_IP>172.16.21.178</intranet_IP>
        <lubanNetVersion>4.9.0.5</lubanNetVersion>
        <password>96e79218965eb72c92a549dd5a330112</password>
        <platform>64</platform>
        <productId>3</productId>
        <softwareEnvironment>hostType=CAD;hostVer=2012;OSName=Windows 10;OSBit=64;OSVer=6-2;</softwareEnvironment>
        <username>hubiao</username>
        <version>30.2.1</version>
        </LBLoginParam>
        </ns6:login></SOAP-ENV:Body></SOAP-ENV:Envelope>'''
        response = self.lubansoftLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        return self.lubansoftLogin


class Gaolu:
    '''
    token登录流程
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.username = username
        self.password = password
        self.header = envConf["headers"]["json_header"]
        self.GaoluLogin = base_requests.Send(envConf["pds"], envConf, global_cache=self.cache)
        self.glxxUser = None

    def getConfig(self):
        resource = "/inspection/inspection-webjars/dist/config.js"
        response = self.GaoluLogin.request('get', resource)
        self.glxxUser = response["Response_text"].split("\n")[2].split(":", 1)[-1].replace(" ", "")

    def auth_login(self):
        '''
        Gaolu 登录
        '''
        resource = self.glxxUser.replace('"', '') + "/auth/login"
        body = {"username": self.username, "password": self.password}
        response = self.GaoluLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        # 获取到响应的token并更新到header中
        header = json.loads(self.GaoluLogin.header)
        header.update({"access-token": response['data_accessToken'][0]})
        self.GaoluLogin.header = json.dumps(header)

    def login(self):
        self.getConfig()
        self.auth_login()
        return self.GaoluLogin


class Gaolu_luban:
    '''
    token登录流程
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.username = username
        self.password = password
        self.header = envConf["headers"]["json_header"]
        self.GaoluLogin = base_requests.Send(envConf["pds_luban"], envConf, global_cache=self.cache)

    def login(self):
        '''
        Gaolu 登录
        '''
        resource = "/luban-glxx-user/auth/login"
        body = {"username": self.username, "password": self.password}
        response = self.GaoluLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        # 获取到响应的token并更新到header中
        header = json.loads(self.GaoluLogin.header)
        header.update({"access-token": response['data_accessToken'][0]})
        self.GaoluLogin.header = json.dumps(header)
        return self.GaoluLogin


class Gaolu_report:
    '''
    token登录流程
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.username = username
        self.password = password
        self.header = envConf["headers"]["json_header"]
        self.GaoluLogin = base_requests.Send(envConf["url_tmp"], envConf, global_cache=self.cache)
        self.glxxUser = None
        self.master_url = envConf["pds_luban"]

    def auth_login(self):
        '''
        Gaolu 登录
        '''
        resource = self.master_url + "/luban-glxx-user/auth/login"
        body = {"username": self.username, "password": self.password}
        response = self.GaoluLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        # 获取到响应的token并更新到header中
        header = json.loads(self.GaoluLogin.header)
        header.update({"access-token": response['data_accessToken'][0]})
        self.GaoluLogin.header = json.dumps(header)

    def login(self):
        self.auth_login()
        return self.GaoluLogin

class Gaolu_permission:
    '''
    token登录流程
    '''

    def __init__(self, username, password, envConf, global_cache):
        self.cache = global_cache
        self.username = username
        self.password = password
        self.header = envConf["headers"]["json_header"]
        self.GaoluLogin = base_requests.Send(envConf["permission"], envConf, global_cache=self.cache)
        self.glxxUser = None
        self.master_url = envConf["pds_luban"]

    def auth_login(self):
        '''
        Gaolu 登录
        '''
        resource = self.master_url + "/luban-glxx-user/auth/login"
        body = {"username": self.username, "password": self.password}
        response = self.GaoluLogin.request('post', resource, body)
        Assertions().assert_equal_value(response["status_code"], 200)
        # 获取到响应的token并更新到header中
        header = json.loads(self.GaoluLogin.header)
        header.update({"access-token": response['data_accessToken'][0]})
        self.GaoluLogin.header = json.dumps(header)

    def login(self):
        self.auth_login()
        return self.GaoluLogin


if __name__ == '__main__':
    pass
