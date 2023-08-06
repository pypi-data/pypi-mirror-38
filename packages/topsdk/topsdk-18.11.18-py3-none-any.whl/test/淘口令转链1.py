# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 15:50
# @Author  : play4fun
# @File    : 淘口令转链1.py
# @Software: PyCharm

"""
淘口令转链1.py:
"""

from top.api import TbkTpwdConvertRequest
from top import appinfo

from config import appkey, secret

req = TbkTpwdConvertRequest()
req.set_app_info(appinfo(appkey, secret))

req.password_content = "￥dAEYbi4KO4D￥"#原链接
# req.password_content = "￥TvFnbi4rS28￥"#转链之后的，优惠券
req.adzone_id = 26807050116
req.dx = "1"

try:
    resp = req.getResponse()

    # it=resp['tbk_item_info_get_response']['results']['n_tbk_item'][0]
    # print(it)

    import json

    ds = json.dumps(resp)
    print(ds)
except Exception as e:
    print(e)
    '''
{
    "tbk_tpwd_convert_response": {
        "data": {
            "click_url": "https://s.click.taobao.com/t?e=m%3D2%26s%3DlPB%2BIFlTXXYcQipKwQzePOeEDrYVVa64XoO8tOebS%2BdRAdhuF14FMQPx4A86vneat4hWD5k2kjOUZR70%2BlK9qVurOGJDe30Mi4iGkEp3vhY1bHXFwOOwIlnifR7TequSVbyFvQb68TVhzIPRUbx8%2FC%2FoxewA8MDczd4sm6IVoF5BvG9Dt0tL1PUA8sxeHPJeLm7IGu8cWyae94Djkt%2FJYSGFCzYOOqAQ&union_lens=lensId:0b177a9d_0c35_166ce44e330_566b",
            
            "num_iid": "576016341093"
        },
        "request_id": "81f43dtpbscl"
    }
}


把别人的淘口令转成自己的淘口令
{
    "tbk_tpwd_convert_response": {
        "data": {
            "click_url": "https://s.click.taobao.com/t?e=m%3D2%26s%3Dsnn8QvJbTiwcQipKwQzePOeEDrYVVa64XoO8tOebS%2BdRAdhuF14FMZ6IEgctIxHz1aH1Hk3GeOiUZR70%2BlK9qVurOGJDe30Mi4iGkEp3vhY1bHXFwOOwIlnifR7TequSVbyFvQb68TVhzIPRUbx8%2FC%2FoxewA8MDczd4sm6IVoF5BvG9Dt0tL1PUA8sxeHPJeLm7IGu8cWyae94Djkt%2FJYSGFCzYOOqAQ&union_lens=lensId:0b01eedb_0d43_166ce482533_5605",
            "num_iid": "576016341093"
        },
        "request_id": "64ifmu0jz018"
    }
}

    '''
