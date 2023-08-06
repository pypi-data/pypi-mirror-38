# -*- coding: utf-8 -*-
# @Time    : 2018/6/16 07:22
# @Author  : play4fun
# @File    : 获取淘宝联盟选品库列表1.py
# @Software: PyCharm

"""
获取淘宝联盟选品库列表1.py:
没有权限
"""

import traceback

from top.api import TbkItemConvertRequest ,TbkUatmFavoritesGetRequest
from top import appinfo

from test.config import appkey, secret

req = TbkItemConvertRequest()
req.set_app_info(appinfo(appkey, secret))
# req.set_app_info(appinfo("24728514",'847aff038c548e44adeeb7fd634d6cc2'))#也没有权限

req.page_no=1
req.page_size=20
req.fields="favorites_title,favorites_id,type"
req.type=1

try:
    resp = req.getResponse()
    import json

    print(resp)

    ds = json.dumps(resp)
    print(ds)
except Exception as e:
    print(e)
    traceback.print_exc()
