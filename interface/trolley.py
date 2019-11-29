from common.send_method import SendMethod
from interface.login import Login


# 编写购物车类
class Trolley(object):
    # 添加
    @staticmethod
    def trolley_add(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 查询
    @staticmethod
    def trolley_search(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 删除
    @staticmethod
    def trolley_delete(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 修改
    @staticmethod
    def trolley_modify(url, data):
        return SendMethod.send_method(url=url, data=data)


if __name__ == '__main__':
    add_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/cart/create'
    login_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/signin'
    login_data = {"name": "tester", "password": "123456"}
    login = Login(login_url)
    session = login.get_session(login_data)
    # print(session)
    # 添加
    add_data = {"spec": [], "session": session, "goods_id": 90, "number": 1}
    response = Trolley.trolley_add(url=add_url, data=add_data)
    print(response)
    # 查询

