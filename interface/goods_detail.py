from common.send_method import SendMethod
from common.get_keyword import GetKeyword


# 商品详情
class GoodsDetail(object):
    # 查看商品详情
    @staticmethod
    def check_detail(url, data):
        return SendMethod.send_method(url=url, data=data)
    # 获取返回数据中某个字段的值
    @staticmethod
    def get_value(response, keyword):
        return GetKeyword.get_keyword(response, keyword)


if __name__ == '__main__':
    pass

