# _*_ coding: utf-8 _*_
__author__ = 'luoli'
import const
import QueryBccMetric
import ClientCore

request = QueryBccMetric.QueryMetricDataRequest(const.ENDPOINT)
request.set_query_params_statistics('maximum')
request.set_query_params_dimensions('i-N22Hwk1P')
request.set_query_params_start_time()
request.set_query_params_end_time()
request.set_query_params_period_second()
request.set_uri_monitor_item('CpuLoadAvg1')
request.set_uri_uid_item(const.BAIDU_USER_ID)


client = ClientCore.AcsClient(
    request=request,
    ak=const.ACCESS_KEY_ID,
    sk=const.SECRET_KEY,
    uid=const.BAIDU_USER_ID,
    endpoint=const.ENDPOINT)


resp = client.do_action()
print resp
