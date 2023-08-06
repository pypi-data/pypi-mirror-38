# -*- coding: utf-8 -*-
import logging
import sys
import os
 
class Logger:
    def __init__(self):
        self.logger = logging.getLogger('cisdi')
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s - %(filename)s - line:%(lineno)d [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        path = os.getcwd()+"\\Log"
        if not os.path.exists(path):
            os.mkdir(path)
        fh = logging.handlers.TimedRotatingFileHandler(
             'Log/' + os.path.basename(sys.argv[0]).split(".")[0], 'midnight', 1, 365)
        fh.setFormatter(fmt)
        fh.setLevel(logging.DEBUG)

        self.logger.addHandler(fh)
    def debug(self,message):
        self.logger.debug(message)
 
    def info(self,message):
        self.logger.info(message)
 
    def warn(self,message):
        self.logger.warn(message)
 
    def error(self,message):
        self.logger.error(message)
 
    def critical(self,message):
        self.logger.critical(message)
 
if __name__ =='__main__':
    # print log info
    logger = Logger()
