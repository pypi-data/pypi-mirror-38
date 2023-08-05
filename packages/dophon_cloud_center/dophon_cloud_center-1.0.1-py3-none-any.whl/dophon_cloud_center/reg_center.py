import socket
from flask import Flask, render_template, redirect, request, jsonify, abort
from dophon_cloud_center import kits
import threading
import urllib3
from flask_bootstrap import Bootstrap
import time
from dophon import logger

logger.inject_logger(globals())

config = ['DOPHON_REG_CENTER_CLUSTERS']  # 公共配置

instance_cache = []  # 实例列表

clusters = {}  # 集群信息

req_pool = urllib3.PoolManager()

"""
注册中心
默认端口为8361
"""


class Center(Flask):

    @property
    def reg_info(self):
        return self._reg_info

    @reg_info.setter
    def setter_reg_info(self, value: dict):
        self._reg_info = value

    @reg_info.getter
    def getter_reg_info(self):
        return self._reg_info

    def __init__(
            self,
            config: dict = {},
            *args,
            **kwargs
    ):
        super(Center, self).__init__(*args, **kwargs)
        # 配置编码
        self.config['JSON_AS_ASCII'] = False

        # h5添加bootstrap样式
        Bootstrap(self)

        # 写入配置
        self._center_config = config

        self._heart_cell = kits.get_heart()
        # 类内属性
        self._reg_info = {}
        self.__self_reg_info = {}

        # 绑定首页路由(重定向)
        self.add_url_rule('/', 'hello_world', self.hello_world, methods=['get', 'post'])
        # 绑定注册中心信息路由
        self.add_url_rule('/center', 'center', self.center, methods=['get', 'post'])
        # 绑定查看实例信息路由
        self.add_url_rule('/request/<service_name>/<instance_id>', 'request_instance', self.request_instance)
        # 绑定注册服务路由
        self.add_url_rule('/reg/service/<name>', 'reg_service', self.reg_service, methods=['get'])
        # 绑定查询中心健康状态路由
        self.add_url_rule('/health', 'health', self.health, methods=['get'])
        # 绑定注册实例列表更新接口路由
        self.add_url_rule('/reg/update', 'get_reg_info', self.get_reg_info, methods=['get'])

    def run(self, host=None, port=None, debug=None,
            load_dotenv=True, **options):

        # 保存地址信息
        self._addr_info = {
            'host': get_host_ip(),
            'port': port
        }
        super(Center, self).run(host=host, port=port, debug=debug,
                                load_dotenv=load_dotenv, **options)

    def hello_world(self):
        return redirect('/center', )

    def center(self):
        m = request.method
        view_data = self._reg_info.copy()
        # 消除内部功能参数
        for k in config:
            if k in view_data:
                view_data.pop(k)
        if m == 'GET':
            return render_template('center.html', reg_info=view_data)
        if m == 'POST':
            return jsonify(view_data)
        return abort(400)

    def request_instance(self, service_name, instance_id):
        if service_name in self._reg_info.keys():
            s_instances = self._reg_info[service_name]
            for instance in s_instances:
                if instance_id == instance['id']:
                    res = req_pool.request('POST',
                                           'http://' + str(instance['host'] + ':' + instance['port'] + '/heart'))
                    if 200 == res.status:
                        return jsonify(eval(res.data))
                    else:
                        return abort(404)
        else:
            return abort(404)

    def reg_service(self, name):
        logger.info('ri: %s sri:%s' % (str(id(self.reg_info)),str(id(self.__self_reg_info))))
        logger.info('%s' % (self._center_config['broadcast_heartbeat']))
        reg_info = self._reg_info if self._center_config['broadcast_heartbeat'] else self.__self_reg_info
        reg_info_cache = self._reg_info
        # 处理多实例服务注册
        if name.upper() in reg_info_cache:
            cache = reg_info_cache[name.upper()]
        else:
            cache = []
        h = request.headers
        # 组装服务细胞信息
        if 'prefer_ip' in h:
            ip = h['prefer_ip']
        else:
            ip = str(h['Host']).split(':')[0]
        if 'u_heart_interface' in h:
            heart = h['u_heart_interface']
            s_c = kits.ServiceCell(ip, h['service_port'], heart)
        else:
            s_c = kits.ServiceCell(ip, h['service_port'])
        for item in cache:
            if item == s_c:
                return jsonify(self._reg_info)
        cache.append(s_c.__dict__())
        reg_info_cache[name.upper()] = cache
        self._reg_info = reg_info_cache
        if not self._center_config['broadcast_heartbeat']:
            # 写入自身注册实例
            if name.upper() in reg_info:
                cache = reg_info[name.upper()]
            else:
                cache = []
            cache.append(s_c.__dict__())
            self.__self_reg_info[name.upper()] = cache
        # print(reg_info_cache)
        self._heart_cell.update_reg(reg_info)
        if clusters:
            # 存在集群信息
            self_clusters_info = clusters.copy()
            self_clusters_info.pop(
                str(hash(self._addr_info['host'] + ':' + str(self._addr_info['port'])))
            )
            reg_info_cache['DOPHON_REG_CENTER_CLUSTERS'] = self_clusters_info
            # 广播服务实例信息
            for cluster_instance in instance_cache:
                cluster_instance.sync_reg_info(
                    self._reg_info,
                    str(hash(
                        str(get_host_ip()) + ':' + str(self._addr_info['port'])
                    ))
                )
        return jsonify(reg_info_cache)

    def health(self):
        '''
        检查注册中心健康状态
        :return:
        '''
        return jsonify({})

    def get_reg_info(self):
        return jsonify(self._reg_info)

    def get_addr_info(self):
        """
        返回实例连接信息
        :return:
        """
        return self._addr_info

    # 集群内共享实例信息
    def sync_reg_info(self, _reg_info: dict, access_token: str):
        if access_token in clusters:
            # 验证发起更新实例
            if hash(str(self.reg_info)) == hash(str(_reg_info)):
                return
            self._reg_info = _reg_info

    def active_heart_check(self,round_sec:int=None):
        threading.Thread(
            target=self._heart_cell.start_heart,
            kwargs={
                'round_sec': round_sec
                if round_sec
                else 15
            }
        ).start()


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def run_singleton(properties={}):
    app = Center(
        {
            # 广播式心跳(慎用,会消耗网络资源)  ->  向集群内部所有实例广播心跳
            'broadcast_heartbeat': bool(properties['broadcast_heartbeat']
                                        if 'broadcast_heartbeat' in properties
                                        else False)
        },
        __name__
    )
    if 'heart_check' in properties.keys() and properties['heart_check']:
        # app.active_heart_check(properties['heart_round_second'])
        threading.Thread(
            target=kits.start_heart,
            kwargs={
                'round_sec': properties['heart_round_second']
                         if 'heart_round_second' in properties
                         else 15
            }
        ).start()
    try:
        instance_cache.append(app)
        clusters[
            str(
                hash(
                    str(get_host_ip()) + ':' + str(properties['port'])
                )
            )
        ] = {
            'host': get_host_ip(),
            'port': properties['port']
        }
        app.run(
            host=properties['host']
            if 'host' in properties and properties['host']
            else '0.0.0.0',
            port=properties['port']
            if 'port' in properties and properties['port']
            else 8361
        )
    except Exception as e:
        instance_cache.remove(app)
        raise e


def run_clusters(properties_list: list):
    # 启动注册中心集群
    for properties in properties_list:
        singleton_thread = threading.Thread(target=run_singleton, kwargs={
            'properties': properties
        })
        singleton_thread.start()
    while True:
        if len(instance_cache) == len(properties_list):
            break
        time.sleep(0.5)
    print('集群启动完毕')
