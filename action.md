# 使用手册

## 一、release下的配置文件

**不同测试环境需要更改一下参数：**
    
    pytest.ini(真实环境)
    [pytest]
    addopts =
        --lb-env=Config/enterprise/config.yaml

    pytest.ini(测试环境)
    [pytest]
    addopts =
        --lb-env=Config/release/config.yaml

    pytest.ini(测试环境)
    [pytest]
    addopts =
        --lb-env=Config/preRelease/config.yaml

**运行方式：**

    1. 整个文件夹的所有用例都运行
        pytest testcases
    2. 指定文件运行：
        pytest testcases\test_add_sheet.py
    3. 指定文件下某条用例运行
        pytest testcases\test_approve_form.py::TestApproveForm::test_flow_setting_deploy

**测试用例运行报告：**

    1. 如果在本地运行测试用例：
        测试报告存在：reports下，也可以通过(pytest.ini)文件参数修改，如下：
        addopts =
         xx
         xx
         --html=reports/report.html --self-contained-html
    2. 如果在CI上运行测试用例：
        测试报告为aller report格式