# rtsf-locust
基于rtsf-http及locust对http(s)等api，进行性能的自动化测试

## 环境准备

### 安装rtsf-locust
pip install rtsf-locust
 

## 关于用例的编写
rtsf-locust与rtsf-http的测试用例，是同一份，唯一的区别就是在执行的时候，命令不一样.

```
# rtsf-http 进行接口的自动化测试
hdriver c:\test_case.yaml
httpdriver c:\test_case.yaml 

#rtsf-locust 进行接口性能的自动化测试
hlocust -f c:\test_case.yaml
httplocust -f c:\test_case.yaml
```

rtsf-locust,具有如下特性：

- 支持yaml、json的测试用例
- 支持case的分层
- 支持case的数据驱动，在locust压测过程中，每个模拟的用户，都会对数据驱动的数据进行遍历，遍历结束，默认使用最后一组数据继续进行压测 


## 关于测试报告

1. 压测过程，实际上是 locust的运行过程，跟rtsf-http不同的是，rtsf-locust**未记录日志和生成报告**
2. 但是，您可以访问locust的控制台，查看实时报告和日志: http://localhost:8089/


## 示例

压测场景：在站点pypi中搜索项目，其中项目名称，使用数据驱动的方式，写在poject.csv中，如下

```
# test_locust.yaml
- project:
    name: xxx系统
    module: xxx模块-性能
    data:
      - csv: projects.csv
        
- case:
    name: search-$project_name
    glob_var:
      expected_result: <title>Search results
    steps:
        - request:
            url: https://pypi.org/search/?q=$project_name
            method: GET
    verify:
        - ${VerifyCode(200)}
        - ${VerifyContain($expected_result)}
        
# project.csv
project_name
rtsf
rtsf-http
rtsf-app
rtsf-win
rtsf-web
```

![hlocust-demo.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-locust-img/hlocust-demo.png)

