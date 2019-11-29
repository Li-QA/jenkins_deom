from common.get_keyword import GetKeyword
from common.operation_Excel import OperationExcel
from common.op_database import OpDatabase
from interface.login import Login
from interface.address import Address
import unittest
import ddt

# 测试数据
op_excel = OperationExcel()
add_file = r'D:\pyCharm\Demo\pycode\Requests\20191109\课堂练习\ECShop_interface\data\add_address.xlsx'
modify_file = r'D:\pyCharm\Demo\pycode\Requests\20191109\课堂练习\ECShop_interface\data\modify_address.xlsx'
test_data1 = op_excel.get_data(add_file)
test_data2 = op_excel.get_data(modify_file)


@ddt.ddt
class TestAddress(unittest.TestCase):
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
    # 添加收货地址
    @ddt.data(*test_data1)
    def test_01_add_address(self, data):
        # SQL语句
        sql = f'select * from ecs_user_address where user_id = {self.user_id}'
        # 获取收货地址表中用户地址数
        before = self.op_database.get_all(sql)
        # 添加收货地址数据
        add_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/address/add'
        add_data = {
            "address": {"default_address": 0, "consignee": f"{data['consignee']}", "tel": f"{data['tel']}",
                        "zipcode": f"{data['postcode']}", "country": "1", "city": "271", "id": 0,
                        "email": f"{data['email']}", "address": f"{data['detail']}",
                        "province": "", "district": "", "mobile": ""}, "session": self.session
        }
        # 添加收货地址
        Address.add_address(url=add_url, data=add_data)
        # 获取收货地址表中用户地址数
        after = self.op_database.get_all(sql)
        result = len(after) - len(before)  # 实际结果
        # 断言
        self.assertEqual(data['expect'], result, msg='断言失败')

    # 查看收货地址
    def test_02_check_address(self):
        # 查看收货地址数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/address/list'
        data = {"session": self.session}
        # 查看收货地址
        response = Address.check_address(url, data)
        # 获取返回数据中data的值
        addr_list = Address.get_value(response, 'data')  # 实际结果
        # SQL语句
        sql = f'select * from ecs_user_address where user_id = {self.user_id}'
        # 获取收货地址表中用户地址数
        sql_addr = self.op_database.get_all(sql)  # 期望结果
        # 断言
        self.assertEqual(len(sql_addr), len(addr_list), msg='断言失败')

    # 修改收货地址
    @ddt.data(*test_data2)
    def test_03_modify_address(self, data):
        # 读取收货地址表中的地址的address_id
        sql = f'select address_id from ecs_user_address where user_id = {self.user_id}'
        id_list = self.op_database.get_all(sql)
        # 修改收货地址数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/address/update'
        modify_data = {
            "address": {"default_address": 0, "consignee": f"{data['consignee']}", "tel": f"{data['tel']}",
                        "zipcode": f"{data['postcode']}", "country": "1", "city": "271", "id": 0, "email": f"{data['email']}",
                        "address": f"{data['detail']}", "province": "0", "district": "0", "mobile": f"{data['mobile']}"},
                        "address_id": id_list[0]['address_id'], "session": self.session
        }
        # 修改收货地址
        response = Address.modify_address(url, modify_data)
        # 获取返回数据中的succeed
        succeed = Address.get_value(response, 'succeed')
        # 断言----缺少数据库验证代码
        self.assertEqual(data['expect'], succeed, msg='断言失败')

    # 删除收货地址
    def test_04_delete_address(self):
        # 读取收货地址表中的地址的address_id
        sql = f'select address_id from ecs_user_address where user_id = {self.user_id}'
        id_list = self.op_database.get_all(sql)
        # 删除收货地址数据
        url = 'http://ecshop.itsoso.cn/ECMobile/?url=/address/delete'
        delete_data = {"address_id": id_list[0]['address_id'], "session": self.session}
        # 删除收货地址
        response = Address.delete_address(url, delete_data)
        # 获取返回数据中succeed
        succeed = Address.get_value(response, 'succeed')    # 实际结果
        # 查询收货地址表中该地址的信息
        sql = f"select * from ecs_user_address where address_id = {id_list[0]['address_id']}"
        info = self.op_database.get_one(sql)
        result = False if info != None else True    # 期望结果
        # 断言
        self.assertEqual(result, succeed, msg='断言失败')


if __name__ == '__main__':
    unittest.main()
