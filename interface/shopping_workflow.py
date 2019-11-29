from common.send_method import SendMethod
from common.get_keyword import GetKeyword



class Shopping(object):
    # 选择商品
    @staticmethod
    def select_goods(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 添加购物车
    @staticmethod
    def add_trolley(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 添加收货地址
    @staticmethod
    def add_address(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 确认订单
    @staticmethod
    def check_order(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 提交订单
    @staticmethod
    def commit_order(url, data):
        return SendMethod.send_method(url=url, data=data)
    
    # 获取返回数据中某个字段的值
    @staticmethod
    def get_value(response, keyword):
        return GetKeyword.get_keyword(response, keyword)


if __name__ == '__main__':
    pass