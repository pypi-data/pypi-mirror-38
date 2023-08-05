#! python3
# -*- encoding: utf-8 -*-
'''
Current module: httplocust.cli

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      httplocust.cli,  v1.0 2018年10月23日
    FROM:   2018年10月23日
********************************************************************
======================================================================

this module reference from httprunner 

'''


import sys, multiprocessing
from rtsf.p_applog import logger
from httplocust import locusts

def main_locust():
    """ Performance test with locust: parse command line options and run commands.
    """
    logger.setup_logger("INFO")

    sys.argv[0] = 'locust'
    if len(sys.argv) == 1:
        sys.argv.extend(["-h"])

    if sys.argv[1] in ["-h", "--help", "-V", "--version"]:
        locusts.main()
        sys.exit(0)

    try:
        testcase_index = sys.argv.index('-f') + 1
        assert testcase_index < len(sys.argv)
    except (ValueError, AssertionError):
        logger.log_error("Testcase file is not specified, exit.")
        sys.exit(1)

    testcase_file_path = sys.argv[testcase_index]
    sys.argv[testcase_index] = locusts.parse_locustfile(testcase_file_path)

    if "--processes" in sys.argv:
        """ locusts -f locustfile.py --processes 4
        """
        if "--no-web" in sys.argv:
            logger.log_error("conflict parameter args: --processes & --no-web. \nexit.")
            sys.exit(1)

        processes_index = sys.argv.index('--processes')

        processes_count_index = processes_index + 1

        if processes_count_index >= len(sys.argv):
            """ do not specify processes count explicitly
                locusts -f locustfile.py --processes
            """
            processes_count = multiprocessing.cpu_count()
            logger.log_warning("processes count not specified, use {} by default.".format(processes_count))
        else:
            try:
                """ locusts -f locustfile.py --processes 4 """
                processes_count = int(sys.argv[processes_count_index])
                sys.argv.pop(processes_count_index)
            except ValueError:
                """ locusts -f locustfile.py --processes -P 8888 """
                processes_count = multiprocessing.cpu_count()
                logger.log_warning("processes count not specified, use {} by default.".format(processes_count))

        sys.argv.pop(processes_index)
        locusts.run_locusts_with_processes(sys.argv, processes_count)
    else:
        locusts.main()