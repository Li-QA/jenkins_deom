from common.operation_Excel import OperationExcel
from common.get_keyword import GetKeyword
from interface.login import Login
import unittest, ddt

# 测试数据
file = r'D:\pyCharm\Demo\pycode\Requests\20191109\课堂练习\ECShop_interface\data\login_data.xlsx'
op_excel = OperationExcel()
test_data = op_excel.get_data(file)


@ddt.ddt
class TestLogin(unittest.TestCase):
    # 编写test case
    @ddt.data(*test_data)
    def test_login(self, data):
        # 登录数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/signin'
        login_data = {"name": f"{data['name']}", "password": f"{data['password']}"}
        # 登录
        succeed = Login(url).get_succeed(login_data)
        # 断言
        self.assertEqual(data['expect'], succeed, msg='断言失败')


if __name__ == '__main__':
    unittest.main()