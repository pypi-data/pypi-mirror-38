# -*- coding: utf-8 -*-
# @Time    : 2018/4/29 15:12
# @Author  : play4fun
# @File    : get_rebate_order.py
# @Software: PyCharm

"""
get_rebate_order.py:
"""

# import top
from top import api as tbk_api

import top.api



url=''
port=''


# req = top.api.TbkRebateOrderGetRequest(url, port)
req = top.api.TbkRebateOrderGetRequest()
req.set_app_info(top.appinfo(appkey, secret))

req.fields = "tb_trade_parent_id,tb_trade_id,num_iid,item_title,item_num,price,pay_price,seller_nick,seller_shop_title,commission,commission_rate,unid,create_time,earning_time"
req.start_time = "2015-03-05 13:52:08"
req.span = 600
req.page_no = 1
req.page_size = 20
try:
    resp = req.getResponse()
    print(resp)
except Exception as e:
    print(e)