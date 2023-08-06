# -*- coding: utf-8 -*-
# @Time    : 2018/4/29 16:52
# @Author  : play4fun
# @File    : 创建淘口令1.py
# @Software: PyCharm

"""
创建淘口令1.py:
http://open.taobao.com/docs/api.htm?apiId=31127

这个能转换【优惠券-长链接】
"""

from top.api import TbkTpwdCreateRequest
from top import appinfo
import config

req=TbkTpwdCreateRequest()
req.set_app_info(appinfo(config.appkey,config.secret))

# req.text='半身裙套装女2018新款时尚潮 港风省心搭配女装上衣短裙两件套夏'
req.text='大众11-17款新帕萨特改装车门防踢垫保护垫专用装饰不锈钢防踢板'
# req.url='https://item.taobao.com/item.htm?id=567873872517'
req.url='https://uland.taobao.com/coupon/edetail?e=JBuZPm5JWqEGQASttHIRqZL3pImL%2FJh1HZ6yD2Py5i%2Fg4lUqifPvH9x2%2FlD7wOdrVxl2CHuUpj1uWNE2q%2FyjycWKxy1EFPIVsSKwS%2F%2FvFcFma4VUO7VGBlZrtTOLgXkcjDppvlX%2Bob%2BBtHA6T8TZnVBPfopb7LXvu8n6e%2B0RLoCEsG9BMdsVqA%3D%3D&traceId=0bb6999515405448411741149e&union_lens=lensId:0b0ad4b4_0bf5_166afa0c5f0_c4b9'
# req.logo=''
# req.tpwd_param

try:
    resp= req.getResponse()
    import json

    ds = json.dumps(resp)
    print(ds)
    print(resp['tbk_tpwd_create_response']['data']['model'])
    #{"tbk_tpwd_create_response": {"data": {"model": "\uffe5cqtQbS9y8gR\uffe5"}, "request_id": "41yh5cdyclhc"}}
    #￥cqtQbS9y8gR￥
except Exception as e:
    print(e)