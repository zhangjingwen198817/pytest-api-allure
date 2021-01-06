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

**配置文件说明:**

    config/release/config.yaml (这几个key对用的value保持一致，需要重复用到)

      表单关联: "测试表10.4.2 明洞防水层现场质量检验表(JL)"
      工程模板:
          dataTemplateItemId1: "测试表10.4.2 明洞防水层现场质量检验表(JL)"
      增加表单:
          应用模板表单: "测试表10.4.2 明洞防水层现场质量检验表(JL)"