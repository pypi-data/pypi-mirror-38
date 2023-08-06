# -*- coding: utf-8 -*-
# @Time    : 2018/7/13 18:11
# @Author  : play4fun
# @File    : 整个流程1.py
# @Software: PyCharm

"""
整个流程1.py:
"""

from top.api import WirelessShareTpwdQueryRequest, TbkTpwdCreateRequest
from top.api import TbkItemConvertRequest
from top import appinfo
from config import appkey, secret
from urllib.parse import urlparse, parse_qs


def parseTKL(msg):
    req = WirelessShareTpwdQueryRequest()
    req.set_app_info(appinfo(appkey, secret))
    req.password_content = msg

    rt = req.getResponse()
    return rt


if __name__ == '__main__':
    # tkl = '''【2018夏季新款女装薄款白色打底内衣性感漏肩内搭背心吊带短款上衣】http://m.tb.cn/h.3XYA5IW 点击链接，再选择浏览器咑閞；或復·制这段描述€g1IVbaMXxxK€后到👉淘♂寳♀👈'''
    tkl = '''【法国菜特价3】http://m.tb.cn/h.3cCldb1 点击链接，再选择浏览器咑閞；或復·制这段描述€qJC7baMSryl€后到👉淘♂寳♀👈'''

    rt = parseTKL(tkl)
    print(rt)
    '''
    {'wireless_share_tpwd_query_response': {'content': '2018夏季新款女装薄款白色打底内衣性感漏肩内搭背心吊带短款上衣', 'native_url': 'tbopen://m.taobao.com/tbopen/index.html?action=ali.open.nav&module=h5&h5Url=https%3A%2F%2Fitem.taobao.com%2Fitem.htm%3Fut_sk%3D1.WkpqTyOBZbADAJxSRs4G0pnb_21380790_1531476850118.PanelQRCode.1%26id%3D568295190230%26sourceType%3Ditem%26price%3D128%26suid%3DB93FAA0C-781F-4C40-961E-93B3911BED21%26un%3D6a0b666299f236be8bd7bab98ffeb263%26share_crt_v%3D1%26sp_tk%3D4oKsZzFJVmJhTVh4eEvigqw%3D%26spm%3Da211b4.24728341%26visa%3D13a09278fde22a2e%26disablePopup%3Dtrue%26disableSJ%3D1&appkey=24728341&visa=13a09278fde22a2e', 'pic_url': 'http://gw.alicdn.com/bao/uploaded/i2/381329993/TB2xzdWfvuSBuNkHFqDXXXfhVXa_!!381329993.jpg', 'price': '128.00', 'suc': True, 'thumb_pic_url': 'http://gw.alicdn.com/bao/uploaded/i2/381329993/TB2xzdWfvuSBuNkHFqDXXXfhVXa_!!381329993.jpg_170x170.jpg', 'title': '淘口令-宝贝', 'url': 'https://item.taobao.com/item.htm?ut_sk=1.WkpqTyOBZbADAJxSRs4G0pnb_21380790_1531476850118.PanelQRCode.1&id=568295190230&sourceType=item&price=128&suid=B93FAA0C-781F-4C40-961E-93B3911BED21&un=6a0b666299f236be8bd7bab98ffeb263&share_crt_v=1&sp_tk=4oKsZzFJVmJhTVh4eEvigqw=&spm=a211b4.24728341&visa=13a09278fde22a2e&disablePopup=true&disableSJ=1', 'request_id': '92ocdpxbz17j'}}
    '''
    url = rt['wireless_share_tpwd_query_response']['url']
    content = rt['wireless_share_tpwd_query_response']['content']
    price = rt['wireless_share_tpwd_query_response']['price']
    pic_url = rt['wireless_share_tpwd_query_response']['pic_url']
    p1 = urlparse(url)
    qs1 = parse_qs(p1.query)
    gid = qs1.get('id', None)[0]
    print(content, price, gid)
    #
    req = TbkItemConvertRequest()
    req.set_app_info(appinfo(appkey, secret))
    req.fields = "click_url"
    req.num_iids = gid  # ,566807961895"# 商品ID串，用','分割，从taobao.tbk.item.get接口获取num_iid字段，最大40个
    # req.adzone_id=adzone_id
    req.adzone_id = 1814028435  # 成功 #广告位ID，区分效果位置
    resp = req.getResponse()
    # import json
    # ds = json.dumps(resp)
    click_url = resp['tbk_item_convert_response']['results']['n_tbk_item'][0]['click_url']
    print(click_url)
    # 创建淘口令
    req = TbkTpwdCreateRequest()
    req.set_app_info(appinfo(appkey, secret))
    req.text = content
    req.url = click_url
    req.logo = pic_url
    resp = req.getResponse()
    # ds = json.dumps(resp)
    print(resp)
    print(resp['tbk_tpwd_create_response']['data']['model'])  # ￥j8V0baMTi6H￥
    print('成功转链')
