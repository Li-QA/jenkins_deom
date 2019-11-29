from interface.goods_detail import GoodsDetail
from interface.login import Login
import unittest


class TestGoodsDetail(unittest.TestCase):
    # 编写test fixture
    def setUp(self) -> None:
        # 登录数据
        login_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/signin'
        login_data = {"name": "tester", "password": "123456"}
        # 实例化登录对象
        login = Login(url=login_url)
        self.session = login.get_session(login_data)

    # 编写测试用例
    def test_goods_detail(self):
        # 商品详情数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/goods'
        data = {"goods_id": 89, "session": self.session}
        # 查看商品详情
        response = GoodsDetail.check_detail(url=url, data=data)
        # 获取返回数据中id的值
        goods_id = GoodsDetail.get_value(response, 'id')

        # 断言
        self.assertEqual(89, int(goods_id), msg='断言失败')


if __name__ == '__main__':
    unittest.main()

