import hashlib
import schedule
import urllib3
import time
import json
from dophon import logger

logger.inject_logger(globals())

_sech = schedule.Scheduler()

req_pool = urllib3.PoolManager()

start_flag=False


class ServiceCell():
    __host = None
    __port = None
    __heart_interface = None
    __id = None

    def __init__(self, host, port, hear_url='/heart'):
        self.__host = host
        self.__port = port
        self.__heart_interface = hear_url
        self.__id = hashlib.sha1(
            (str(self.__host) + str(self.__port) + str(self.__heart_interface)).encode('utf8')).hexdigest()

    def __dict__(self):
        return {
            'id': self.__id,
            'host': self.__host,
            'port': self.__port,
            'heart_interface': self.__heart_interface
        }

    def __eq__(self, other):
        return self.__id == other['id']


class HeartSech():

    def __init__(self, time):
        self.__reg={}
        _sech.every(time).seconds.do(self.heart_beat)

    '''
    心跳一跳操作
    '''
    def heart_beat(self):
        try:
            # 获取每个服务
            # print(self.__reg)
            for service_name in self.__reg:
                if service_name == 'DOPHON_REG_CENTER_CLUSTERS':
                    # 跳过注册中心集群配置
                    continue
                # 获取每个服务的实例列表
                services = self.__reg[service_name]
                # print(services)
                services_copy = services
                for instence in services:
                    # 获取每个具体实例
                    ip_addr = str(instence['host']).split(':')[0]
                    url = 'http://' + ip_addr + ':' + instence['port'] + instence[
                        'heart_interface'] + '/as/' + service_name
                    logger.info('%s reg_info: %s' % (id(self),str(self.__reg)))
                    logger.info('发送心跳: %s' % (url))
                    try:
                        res = req_pool.request(method='POST', url=url,
                                               body=bytes(json.dumps(self.__reg), encoding='utf8'),
                                               headers={
                                                   'Content-Type': 'application/json'
                                               })
                        res_result = eval(res.data.decode('utf8'))
                        if res_result['event'] == 404:
                            # 实例注册信息有误
                            services_copy.remove(instence)
                            self.__reg[service_name] = services_copy
                    except Exception as e:
                        # 连接失败打印错误信息
                        logger.info( '%s \n %s \n %s:%s \n连接失败,移除对应实例' % (e, service_name, ip_addr, instence['port']) )
                        services_copy.remove(instence)
                        self.__reg[service_name] = services_copy
                if 0 >= len(services):
                    self.__reg.pop(service_name)
                    if 0 >= len(self.__reg):
                        break;
        except Exception as e:
            print(e)
        # print(self.__reg)

    def update_reg(self, reg_info):
        self.__reg = reg_info

def start_heart(round_sec: int):
    global start_flag
    if start_flag:
        return
    else:
        start_flag=True
    while True:
        _sech.run_all()
        time.sleep(round_sec)


def get_heart(sech_time: int = 15) -> HeartSech:
    """
        :param sech_time: 心跳检查时间,默认15秒,最低15秒(线程等待时间)
    """
    if sech_time<15:
        sech_time = 15
    return HeartSech(sech_time)
