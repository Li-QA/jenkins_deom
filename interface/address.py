from common.send_method import SendMethod
from common.get_keyword import GetKeyword
from interface.login import Login


class Address(object):
    # 添加收货地址
    @staticmethod
    def add_address(url, data):
        return SendMethod.send_method(url=url, data=data)
    # 查看收货地址
    @staticmethod
    def check_address(url, data):
        return SendMethod.send_method(url=url, data=data)
    # 修改收货地址
    @staticmethod
    def modify_address(url, data):
        return SendMethod.send_method(url=url, data=data)
    # 删除收货地址
    @staticmethod
    def delete_address(url, data):
        return SendMethod.send_method(url=url, data=data)
    # 获取返回数据中某个字段的值
    @staticmethod
    def get_value(response, keyword):
        return GetKeyword.get_keyword(response, keyword)


if __name__ == '__main__':
    login_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/signin'
    login_data = {"name": "tester", "password": "123456"}
    login = Login(login_url)
    session = login.get_session(login_data)

    add_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/address/add'
    add_data = {"address":{"default_address":0,"consignee":"tester","tel":"13512345678","zipcode":"621000",
                           "country":"4044","city":"","id":0,"email":"tester1@qq.com","address":"天府新谷",
                           "province":"","district":"","mobile":""},"session":session
                }
    res = Address.add_address(add_url, add_data)
    print(res)