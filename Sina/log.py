#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
# import os
import time
# 创建一个logger
class Logger():
    def log(self):
        logger = logging.getLogger()
        logging.basicConfig(filename ='log.log',level = logging.WARNING,format = '%(asctime)s - %(levelname)s: %(message)s')
        return logger
if __name__ == '__main__':
    log=Logger().log()
    date='hhhhh'
    log.warning('date=%s', date)