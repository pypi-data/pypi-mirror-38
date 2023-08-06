# _*_ coding: utf-8 _*_
__author__ = 'luoli'
from BaiduCoreRequest import IqiyiOpRequest
import datetime
import const
import ClientCore

'''
query_params = {'statistics[]': 'maximum',  # statistics 统计聚合的类型【average,maximum,minimum,sampleCount,sum】
                'dimensions': 'InstanceId: %s' % instanceid,  # demo InstanceId:i-j6Dxxxxx,
                'startTime': start_time,
                 'endTime': end_time,
                'periodInSecond': 60}
'''


def _get_default_time(step_time=5):
    _end_time = datetime.datetime.utcnow()
    step = datetime.timedelta(minutes=step_time)
    _start_time = _end_time - step
    _end_time = _end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    _start_time = _start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return _start_time, _end_time


class QueryMetricDataRequest(IqiyiOpRequest):

    def __init__(self,
                 endpoint=None):
        IqiyiOpRequest.__init__(self,
                                endpoint)

    def set_query_params_statistics(self, statistics):
        self.add_query_params('statistics[]', statistics)

    def get_query_params_statistics(self):
        return self._query_params.get('statistics[]')

    def set_query_params_dimensions(self, instance_id):
        self.add_query_params('dimensions', 'InstanceId: %s' % instance_id)

    def get_query_params_dimensions(self):
        return self._query_params.get('dimensions')

    def set_query_params_start_time(self, start_time=_get_default_time()[0]):
        self.add_query_params('startTime', start_time)

    def get_query_params_start_time(self):
        return self._query_params.get('startTime')

    def set_query_params_end_time(self, end_time=_get_default_time()[1]):
        self.add_query_params('endTime', end_time)

    def get_query_params_end_time(self):
        return self._query_params.get('endTime')

    def set_query_params_period_second(self, second=60):
        self.add_query_params('periodInSecond', second)

    def get_query_params_period_second(self):
        return self.get_query_params().get('periodInSecond')

    def set_uri_monitor_item(self, item):
        self.add_uri_params('item', item)

    def get_uri_monitor_item(self):
        return self.get_uri_params().get('item')

    def set_uri_uid_item(self, uid):
        self.add_uri_params('uid', uid)

    def get_uri_uid_item(self):
        return self.get_uri_params().get('uid')















