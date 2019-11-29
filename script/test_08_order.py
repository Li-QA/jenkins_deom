from interface.order import Order
from interface.login import Login
from common.op_database import OpDatabase
from common.get_keyword import GetKeyword
import unittest


class TestOrder(unittest.TestCase):
    # 编写test fixture
    def setUp(self) -> None:
        # 登录数据
        login_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/signin'
        login_data = {"name": "tester", "password": "123456"}
        # 实例化登录对象
        login = Login(url=login_url)
        self.session = login.get_session(login_data)
        self.user_id = int(GetKeyword.get_keyword(self.session, 'uid'))
        # 实例化数据操作对象
        self.op_database = OpDatabase()

    @classmethod
    def tearDownClass(cls) -> None:
        # 清空数据信息
        op_database = OpDatabase()
        op_database.clear_mysql()

    # 编写 test case
    # 查询待付款订单
    def test_01_order_await_pay(self):
        # -----需要手动添加未付款订单记录
        # 读取订单信息表中未付款的订单数
        sql = f'select * from ecs_order_info where user_id = {self.user_id} and order_status = 0 and pay_status = 0'
        order_list = self.op_database.get_all(sql)
        # 待付款订单数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/order/list'
        data = {"session": self.session, "type": "await_pay", "pagination": {"count": 10, "page": 1}}
        response = Order.order_await_pay(url=url, data=data)
        # 获取返回值中succeed的值
        succeed = Order.get_value(response, 'succeed')  # 实际结果
        # 获取返回值中count的值
        count = Order.get_value(response, 'count')
        # 判断数据库中未付款订单数是否定于返回值中的数
        result = True if len(order_list) == count else False  # 期望结果
        print(result)
        # 断言
        self.assertEqual(succeed, result, msg='断言失败')

    # 查询待发货订单
    def test_02_order_await_ship(self):
        # 修改订单信息表中订单为待发货状态
        sql1 = f'update ecs_order_info set order_status = 0, shipping_status = 0, pay_status = 2 where user_id = {self.user_id}'
        self.op_database.write(sql1)
        # 读取订单信息表中未发货的订单数
        sql2 = f'select * from ecs_order_info where user_id = {self.user_id} and shipping_status = 0 and pay_status = 2'
        order_list = self.op_database.get_all(sql2)
        # 待发货订单数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/order/list'
        data = {"session": self.session, "type": "await_ship", "pagination": {"count": 10, "page": 1}}
        response = Order.order_await_ship(url=url, data=data)
        # 获取返回值中succeed的值
        succeed = Order.get_value(response, 'succeed')  # 实际结果
        # 获取返回值中count的值
        count = Order.get_value(response, 'count')
        # 判断数据库中未发货订单数是否定于返回值中的数
        result = True if len(order_list) == count else False  # 期望结果
        # 断言
        self.assertEqual(succeed, result, msg='断言失败')

    # 查询待收货订单
    def test_03_order_shipped(self):
        # 修改订单信息表中订单为待收货状态
        sql1 = f'update ecs_order_info set order_status = 0, shipping_status = 1, pay_status = 2 where user_id = {self.user_id}'
        self.op_database.write(sql1)
        # 读取订单信息表中待收货的订单数
        sql2 = f'select * from ecs_order_info where user_id = {self.user_id} and order_status = 0 and shipping_status = 1'
        order_list = self.op_database.get_all(sql2)
        # 待发货订单数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/order/list'
        data = {"session": self.session, "type": "shipped", "pagination": {"count": 10, "page": 1}}
        response = Order.order_shipped(url=url, data=data)
        # 获取返回值中succeed的值
        succeed = Order.get_value(response, 'succeed')  # 实际结果
        # 获取返回值中count的值
        count = Order.get_value(response, 'count')
        # 判断数据库中待收货订单数是否定于返回值中的数
        result = True if len(order_list) == count else False  # 期望结果
        # 断言
        self.assertEqual(succeed, result, msg='断言失败')

    # 查询已收货订单
    def test_04_order_finished(self):
        # 修改订单信息表中订单为已收货状态
        sql1 = f'update ecs_order_info set order_status = 1, shipping_status = 2, pay_status = 2 where user_id = {self.user_id}'
        self.op_database.write(sql1)
        # 读取订单信息表中已收货的订单数
        sql2 = f'select * from ecs_order_info where user_id = {self.user_id} and order_status = 1 and shipping_status = 2'
        order_list = self.op_database.get_all(sql2)
        # 已发货订单数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/order/list'
        data = {"session": self.session, "type": "finished", "pagination": {"count": 10, "page": 1}}
        response = Order.order_finished(url=url, data=data)
        # 获取返回值中succeed的值
        succeed = Order.get_value(response, 'succeed')  # 实际结果
        # 获取返回值中count的值
        count = Order.get_value(response, 'count')
        # 判断数据库中已收货订单数是否定于返回值中的数
        result = True if len(order_list) == count else False  # 期望结果
        # 断言
        self.assertEqual(succeed, result, msg='断言失败')


if __name__ == '__main__':
    unittest.main()
