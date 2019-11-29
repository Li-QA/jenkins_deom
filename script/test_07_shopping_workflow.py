from common.op_database import OpDatabase
from common.get_keyword import GetKeyword
from interface.login import Login
from interface.shopping_workflow import Shopping
import unittest


class TestShopping(unittest.TestCase):
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
    def setUpClass(cls) -> None:
        # 清空数据信息
        op_database = OpDatabase()
        op_database.clear_mysql()

    # 编写test case
    def test_shopping_workflow(self):
        # 选择商品
        url1 = 'http://ecshop.itsoso.cn/ECMobile/?url=/goods'
        data1 = {"goods_id": 89, "session": self.session}
        response = Shopping.select_goods(url1, data1)
        goods_id = Shopping.get_value(response, 'id')
        # 添加到购物车
        url2 = 'http://ecshop.itsoso.cn/ECMobile/?url=/cart/create'
        data2 = {"spec": [], "session": self.session, "goods_id": goods_id, "number": 1}
        Shopping.add_trolley(url2, data2)
        # 添加收货地址
        url3 = 'http://ecshop.itsoso.cn/ECMobile/?url=/address/add'
        data3 = {
            "address": {"default_address": 0, "consignee": "tester", "tel": "13512345678",
                        "zipcode": "123456", "country": "1", "city": "271", "id": 0,
                        "email": "tester@qq.com", "address": "天府新谷",
                        "province": "24", "district": "276", "mobile": ""}, "session": self.session
        }
        Shopping.add_address(url3, data3)
        # 确认订单
        url4 = 'http://ecshop.itsoso.cn/ECMobile/?url=/flow/checkOrder'
        data4 = {"session": self.session}
        response = Shopping.check_order(url4, data4)
        # 获取返回值中的shipping_id和pay_id
        shipping_id = Shopping.get_value(response, 'shipping_id')
        pay_id = Shopping.get_value(response, 'pay_id')
        # 提交订单
        url5 = 'http://ecshop.itsoso.cn/ECMobile/?url=/flow/done'
        data5 = {"shipping_id": shipping_id, "session": self.session, "pay_id": pay_id}
        response = Shopping.commit_order(url5, data5)
        # 获取返回数据中succeed, order_id
        succeed = Shopping.get_value(response, 'succeed')  # 实际结果
        order_id = Shopping.get_value(response, 'order_id')
        # 查询订单表中该订单的信息
        sql = f'select * from ecs_order_info where order_id = {order_id}'
        order_info = self.op_database.get_one(sql)
        result = True if order_info != None else False  # 期望结果
        self.assertEqual(result, succeed, msg='断言失败')


if __name__ == '__main__':
    unittest.main()
