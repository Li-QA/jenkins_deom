from common.send_method import SendMethod
from common.get_keyword import GetKeyword


class Register(object):
    # 注册
    @staticmethod
    def register_account(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 获取返回值中某个字段的值
    @staticmethod
    def get_value(response, keyword):
        return GetKeyword.get_keyword(response, keyword)


if __name__ == '__main__':
    reg_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/signup'
    reg_data = {"field": [{"id": 5, "value": "11011011011"}], "email": "tester2@123.com", "name": "tester2",
                "password": "123456"}
    reg = Register()
    res = reg.register_account(url=reg_url, data=reg_data)
    print(res)
