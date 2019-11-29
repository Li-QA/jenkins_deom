from interface.login import Login
from interface.trolley import Trolley
from common.get_keyword import GetKeyword
from common.op_database import OpDatabase
import unittest


class TestTrolley(unittest.TestCase):
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

    @classmethod
    def tearDownClass(cls) -> None:
        # 清空数据信息
        op_database = OpDatabase()
        op_database.clear_mysql()

    # 编写test case
    # 购物车添加商品
    def test_01_trolley_add(self):
        self.op_database.clear_mysql()
        # SQL语句
        sql = f'select * from ecs_cart where user_id = {self.user_id}'
        # 获取购物车表中用户所有的商品类数
        before_kinds = self.op_database.get_all(sql)
        # 添加购物车数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/cart/create'  # 请求地址
        data = {"spec": [], "session": self.session, "goods_id": 89, "number": 1}  # 请求参数
        # 添加购物车
        response = Trolley.trolley_add(url=url, data=data)
        # 获取返回值succeed字段的值
        succeed = GetKeyword.get_keyword(response, 'succeed')  # 实际结果
        # 获取商品添加后购物车表中用户所有的商品类数
        after_kinds = self.op_database.get_all(sql)
        result = len(after_kinds) - len(before_kinds)   # 期望结果
        # 断言
        self.assertEqual(succeed, result, msg='断言失败')

    # 购物车查询
    def test_02_trolley_search(self):
        # 查询购物车数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/cart/list'  # 请求地址
        data = {"session": self.session}  # 请求参数
        # 查询购物车
        response = Trolley.trolley_search(url=url, data=data)
        # 获取返回值中goods_list的值
        value = GetKeyword.get_keyword(response, 'goods_list')  # 实际结果
        # SQL语句
        sql = f'select * from ecs_cart where user_id = {self.user_id}'
        # 获取购物车表中用户所有的商品类数
        kinds = self.op_database.get_all(sql)  # 期望结果
        # 断言
        self.assertEqual(len(value), len(kinds), msg='断言失败')

    # 购物车修改
    def test_03_trolley_modify(self):
        # 读取购物车商品表中商品的rec_id
        sql = f'select rec_id from ecs_cart where user_id = {self.user_id}'
        recid_dict = self.op_database.get_one(sql)
        # 修改购物车数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/cart/update'
        data = {"new_number": 3, "session": self.session, "rec_id": recid_dict['rec_id']}
        # 修改购物车
        Trolley.trolley_modify(url=url, data=data)
        # 获取修改后购物车商品表中该商品数量
        sql = f'select * from ecs_cart where user_id = {self.user_id} and rec_id = {recid_dict["rec_id"]}'
        goods = self.op_database.get_one(sql)
        num = goods['goods_number']
        # 断言
        self.assertEqual(3, num, msg='断言失败')

    # 购物车删除
    def test_04_trolley_delete(self):
        # 读取购物车商品表中商品的rec_id
        sql = f'select rec_id from ecs_cart where user_id = {self.user_id}'
        recid_dict = self.op_database.get_one(sql)
        # 获取删除前购物车表商品的信息
        goods = self.op_database.get_one(sql)
        # 判断是否存在该商品
        if goods:
            # 删除购物车数据
            url = 'http://ecshop.itsoso.cn/ECMobile/?url=/cart/delete'
            data = {"session": self.session, "rec_id": recid_dict['rec_id']}
            # 删除购物车
            response = Trolley.trolley_delete(url=url, data=data)
            # 获取返回值中succeed的值
            value = GetKeyword.get_keyword(response, 'succeed')  # 实际结果
            # 获取该商品的信息
            after = self.op_database.get_one(sql)
            # 判断是否能获取该商品的信息
            result = False if after != None else True  # 期望结果
            # 断言
            self.assertEqual(value, result, msg='断言失败')


if __name__ == '__main__':
    unittest.main()
