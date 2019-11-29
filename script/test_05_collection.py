from interface.collection import Collection
from common.get_keyword import GetKeyword
from common.op_database import OpDatabase
from interface.login import Login
import unittest


class TestCollection(unittest.TestCase):
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
    # 添加收藏
    def test_01_collect_add(self):
        # 添加收藏数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/collect/create'
        data = {"session": self.session, "goods_id": 68}
        # 添加收藏
        response = Collection.collection_add(url=url, data=data)
        # 获取返回值中succeed的值
        succeed = Collection.get_value(response, 'succeed')  # 实际结果
        # 读取收藏商品表中该商品的信息
        sql = f'select * from ecs_collect_goods where user_id = {self.user_id} and goods_id = 68'
        collect = self.op_database.get_all(sql)
        # 断言
        result = True if collect else False  # 期望结果
        self.assertEqual(succeed, result, msg='断言失败')

    # 查看收藏
    def test_02_collect_check(self):
        # 查看收藏数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/collect/list'
        data = {"session": self.session, "pagination": {"count": 10, "page": 1}, "rec_id": 0}
        try:
            # 查看收藏
            response = Collection.collection_check(url=url, data=data)
            # 获取返回值中count、rec_id的值
            count = Collection.get_value(response, 'count')  # 实际结果
            # 读取收藏商品表中所有商品的数量
            sql = f'select * from ecs_collect_goods where user_id = {self.user_id}'
            num = self.op_database.get_all(sql)  # 期望结果
            # 断言
            self.assertEqual(count, len(num), msg='断言失败')
        except Exception as e:
            print('错误信息：', e)

    # 移除收藏
    def test_03_collect_remove(self):
        # 获取收藏商品表中的rec_id
        sql = f'select rec_id from ecs_collect_goods where user_id = {self.user_id}'
        recid_dict = self.op_database.get_one(sql)
        # 移除收藏数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/collect/delete'
        data = {"session": self.session, "rec_id": recid_dict["rec_id"]}
        # 移除收藏
        response = Collection.collection_remove(url=url, data=data)
        # 获取返回值中succeed的值
        succeed = Collection.get_value(response, 'succeed')   # 实际结果
        # 获取收藏商品表中该商品的信息
        sql = f'select * from ecs_collect_goods where user_id = {self.user_id} and rec_id = {recid_dict["rec_id"]}'
        collect = self.op_database.get_all(sql)
        # 断言
        result = False if collect else True    # 期望结果
        self.assertEqual(succeed, result, msg='断言失败')


if __name__ == '__main__':
    unittest.main()