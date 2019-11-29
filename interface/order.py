from common.send_method import SendMethod
from common.get_keyword import GetKeyword
from interface.login import Login


# 编写购物车类
class Order(object):
    # 待付款
    @staticmethod
    def order_await_pay(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 待发货
    @staticmethod
    def order_await_ship(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 待收货
    @staticmethod
    def order_shipped(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 已收货（历史订单）
    @staticmethod
    def order_finished(url, data):
        return SendMethod.send_method(url=url, data=data)
    
    # 获取返回数据中某个字段的值
    @staticmethod
    def get_value(response, keyword):
        return GetKeyword.get_keyword(response, keyword)


if __name__ == '__main__':
    order_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/order/list'
    login_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/signin'
    login_data = {"name": "李哈哈_5", "password": "123456"}
    login = Login(login_url)
    session = login.get_session(login_data)
    # print(session)
    await_pay_data = {"session": session, "type": "await_pay", "pagination": {"count": 10, "page": 1}}
    res = Order.order_await_pay(url=order_url, data=await_pay_data)
    print(res)
    