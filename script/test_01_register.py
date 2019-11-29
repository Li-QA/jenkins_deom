from interface.register import Register
from common.op_database import OpDatabase
from common.operation_Excel import OperationExcel
import unittest, ddt

# 测试数据
file = r'D:\pyCharm\Demo\pycode\Requests\20191109\课堂练习\ECShop_interface\data\register_data.xlsx'
op_excel = OperationExcel()
test_data = op_excel.get_data(file)


@ddt.ddt
class TestRegister(unittest.TestCase):
    # 编写test fixture
    def setUp(self) -> None:
        self.op_database = OpDatabase()
        self.op_database.clear_mysql()

    def tearDown(self) -> None:
        if self.succeed:
            self.op_database.delete_user(self.uid)

    # 编写test case
    @ddt.data(*test_data)
    def test_register(self, data):
        # 注册数据
        reg_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/signup'
        reg_data = {"field": [{"id": 5, "value": f"{data['tel']}"}], "email": f"{data['email']}", "name": f"{data['name']}",
                    "password": f"{data['password']}"}
        # 注册用户
        response = Register.register_account(url=reg_url, data=reg_data)
        # 获取返回值中succeed, uid的值
        self.succeed = Register.get_value(response, 'succeed')   # 实际结果
        self.uid = Register.get_value(response, 'uid')
        # 断言
        self.assertEqual(data['expect'], self.succeed, msg='断言失败')


if __name__ == '__main__':
    unittest.main()