#!/usr/bin/env python
# encoding: utf-8

# 腾讯智能闲聊需要用模块
import random
import string
import time
import hashlib  #  用户签名需要用到的
import urllib.parse
import urllib.request
import json  # 处理收到的json数据

# 爬取中关村用到的模块
import requests
from urllib.parse import quote   # 处理url中文报错
from lxml import etree  # xpath解析网页取数据


class SpiderZOL(object):
    def __init__(self, param):
        # 根据param拼接搜索地址
        self.search_url = f"http://detail.zol.com.cn/index.php?c=SearchList&kword={quote(param)}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Referer": self.search_url,
            "Cookie": "gr_user_id=acd9bfc4-2645-4d79-a83b-92ea6fb26c6f; z_pro_city=s_provice%3Dhenan%26s_city%3Dzhengzhou; userProvinceId=22; userCityId=260; userCountyId=0; userLocationId=1226; realLocationId=1226; userFidLocationId=1226; ip_ck=4c+B4fv1j7QuNjgwNjEyLjE1NDY2NjMzMTA%3D; listSubcateId=57; visited_subcateId=57; visited_subcateProId=57-0; z_day=ixgo20=1&rdetail=9; visited_serachKw=%u82F9%u679Cx%7C%u82F9%u679C%u624B%u673A%20x; Hm_lvt_ae5edc2bc4fc71370807f6187f0a2dd0=1546665646,1546670449; lv=1546671127; vn=2; Adshow=2; Hm_lpvt_ae5edc2bc4fc71370807f6187f0a2dd0=1546671245; questionnaire_pv=1546646430"
        }
        # 网页源码
        self.html = None
        # 网页源码转etree对象
        self.html_eles = None

    # 获取网页源代码
    def get_html(self, url):
        response = requests.post(url, headers=self.headers)
        print(response.status_code)
        search_result = response.content.decode("GB2312", "ignore")
        # 用类变量接收网页源码
        self.html = search_result
        # 用类变量接收网页源码转etree对象
        self.html_eles = etree.HTML(search_result)

    # 主程序 发根据参数拿到产品信息
    def product_info(self):
        product_list = []
        self.get_html(self.search_url)
        # xpath取出每条产品信息的item
        list_item = self.html_eles.xpath('//div[@class="list-item clearfix"]')
        # 取搜索结果前三条商品
        for item in list_item[0:3]:
            # 商品图片
            image_url = item.xpath('div[@class="pic-box SP"]/a/img/@src')[0]
            # 商品名字
            name = " ".join(item.xpath('div[@class="pro-intro"]/h3//text()'))
            # 商品参数
            param_li = item.xpath('div[@class="pro-intro"]//ul/li')[1:]
            params = [x.xpath("text()")[0] for x in param_li]
            # ['4G网络：移动TD-LTE，联通TD-LTE ', '主屏尺寸：4英寸  1136x640像素 ', 'CPU型号：苹果 A7+M7协处理器  ', 'CPU频率：1.3GHz  双核 ', '电池容量：1560mAh  不可拆卸式电 ', '后置摄像：800万像素  ']
            # 商品价格
            price = ":".join(item.xpath('div[@class="price-box"]/span/b/text()'))
            # 添加到商品list中
            product_list.append((image_url, name, params, price))
        return product_list




class Chart(object):
    def __init__(self):
        # appid
        self.appid = 2110618292
        # 接口app钥匙
        self.appkey = "np77DWqUT6BwtfNV"
        # 接口基础url
        self.base_url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"

    # 生成用户签名
    def get_sign(self, params, appkey):
        # True 降序 False升序默认升序
        keys = sorted(params, reverse=False)
        # print(sorted(params.items(), key=operator.itemgetter(0), reverse=False))
        str_ = ""
        for key in keys:
            str_ += (key + "=" + urllib.parse.quote(str(params.get(key))) + "&")
        # print(str_)
        str_ += ("app_key" + "=" + appkey)
        # 构造MD5
        md = hashlib.md5()
        md.update(str_.encode("utf-8"))
        # print(md.hexdigest())
        sign = md.hexdigest().upper()
        return sign

    #  发请求获得机器人回话
    def do_http_post(self, url, params):
        """

        :param url:
        :param params:
        :return: 返回机器上回答内容
        """
        data = urllib.parse.urlencode(params).encode("utf-8")
        result_obj = urllib.request.urlopen(url, data)
        return json.loads(result_obj.read().decode("utf-8"))["data"]["answer"]

    # 主程序
    def smart_chat(self, question):
        # 需要的参数
        params = {
            "app_id": 2110618292,
            "session": "1000",
            "question": question,
            "time_stamp": time.time(),
            # "time_stamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            "nonce_str": "".join(random.sample(string.ascii_letters + string.digits, 10))
        }
        # 在参数字典中添加用户签名参数
        params["sign"] = self.get_sign(params, self.appkey)
        # 返回闲聊机器人的回复消息
        return self.do_http_post(self.base_url, params)


if __name__ == "__main__":
    # spider_obj = SpiderZOL("华硕电脑")
    # spider_obj.product_info()
    chart_obj = Chart()
    print(chart_obj.smart_chat("郑州天气"))
