# -*- coding: utf-8 -*-
# @Time    : 2018/4/29 17:22
# @Author  : play4fun
# @File    : 淘宝客新用户订单API_导购1.py
# @Software: PyCharm

"""
淘宝客新用户订单API_导购1.py:
"""

from top.api import TbkDgNewuserOrderGetRequest
from top import appinfo
import config

req=TbkDgNewuserOrderGetRequest()
req.set_app_info(appinfo(config.appkey,config.secret))

req.page_size=20
req.adzone_id=154150379#mm_128160800_41488987_177810904
# mm_128160800_40192372_154150379
# mm_18989874_43894087_376356913
req.page_no=1
req.start_register_time="2018-07-24 00:00:00"
req.end_register_time="2018-07-27 00:00:00"


try:
    resp= req.getResponse()
    import json

    ds = json.dumps(resp)
    print(ds)
except Exception as e:
    print(e)