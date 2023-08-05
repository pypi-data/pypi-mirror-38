#! python3
# -*- encoding: utf-8 -*-
'''
Current module: httplocust.task

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      httplocust.task,  v1.0 2018年10月23日
    FROM:   2018年10月23日
********************************************************************
======================================================================

Provide a function for the automation test

'''
from rtsf import p_executer, p_exception 
from functools import partial
from httpdriver.driver import LocustDriver

class LocustTask(object):

    def __init__(self, path_or_testsets, locust_client):
        self.task_suite = p_executer.init_test_suite(path_or_testsets, partial(LocustDriver,locust_client))

    def run(self):
        for suite in self.task_suite.tasks:
            for test in suite.tests:
                try:
                    test.runTest()
                except p_exception.MyBaseError as e:
                    from locust.events import request_failure                    
                    request_step = test.testcase_dict["steps"][0]
                    
                    request_failure.fire(
                        request_type=request_step.get("request", {}).get("method"),
                        name=request_step.get("request", {}).get("url"),
                        response_time=0,
                        exception=e
                    )
