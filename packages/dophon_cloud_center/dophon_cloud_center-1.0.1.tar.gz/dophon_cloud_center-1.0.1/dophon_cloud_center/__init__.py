from dophon_cloud_center import reg_center
from dophon import logger

logger.inject_logger(globals())


def active_center(prop_obj: dict, singleton: bool = True, clusters: int = 0):
    def inj_method(f):
        def inj_args(*args, **kwargs):
            # 前期设置
            f(*args, **kwargs)
            if singleton:
                reg_center.run_singleton(properties=prop_obj)
            else:
                if clusters < 2:
                    raise Exception('集群数异常: %s' % clusters)
                else:
                    c_props = []
                    for next_port in range(clusters):
                        clusters_prop = prop_obj.copy()
                        clusters_prop['port'] = int(prop_obj['port']) + next_port
                        c_props.append(clusters_prop)
                    reg_center.run_clusters(properties_list=c_props)

        return inj_args

    return inj_method
