#coding=utf-8

import logging,time,os
import logging.handlers


class Logger(object):

    def __init__(self,log_name='api.log',project_name='API',log_path='',log_level='DEBUG'):
        '''

        :param log_name:        日志文件名称
        :param project_name:    项目名称
        :param log_path:        日志输出的路径,非必传
        :param log_level:       日志级别
        '''
        self.logger = logging.getLogger(project_name)  # 指定输出日志的程序名
        self.logger.setLevel(logging.DEBUG)    #设定全局的日志级别
        logging_level = eval("logging." + log_level)
        fh = ''   #初始化fh
        if log_path:
            log_path = os.path.join(log_path,'logs')
            log_path_name=os.path.join(log_path,log_name)
            #对文件日志进行分割,已天为单位
            fh = logging.handlers.TimedRotatingFileHandler(log_path_name, when='D', interval=1, backupCount=10)

            fh.suffix="%Y-%m-%d"+'.log'
            fh.setLevel(logging_level)  # 输入的日志级别
            # # create formatter
            formatterFh = logging.Formatter('%(asctime)s - %(name)s - '
                                            '%(levelname)s - '
                                            '%(filename)s - %(funcName)s - %(lineno)d - %(message)s')
            fh.setFormatter(formatterFh)


        ###向屏幕上打印
        ch = logging.StreamHandler()
        ch.setLevel(logging_level)
        formatterCh = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')

        # 定义handler的输出格式
        ch.setFormatter(formatterCh)

        # 给logger添加handler
        if not self.logger.handlers:
            self.logger.addHandler(ch)
            if fh:
                self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger


if __name__=='__main__':
    logger=Logger('logtest.log','test').get_logger()
    logger.info('111')

