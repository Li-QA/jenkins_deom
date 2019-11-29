from common.send_method import SendMethod
from common.get_keyword import GetKeyword



class Login(object):
    def __init__(self, url):
        self.url = url
    # 登录
    def login_ecshop(self, data):
        return SendMethod.send_method(url=self.url, data=data)

    # 获取session
    def get_session(self, data):
        response = self.login_ecshop(data)
        return GetKeyword.get_keyword(response, 'session')
    
    # 获取succeed
    def get_succeed(self, data):
        response = self.login_ecshop(data)
        return GetKeyword.get_keyword(response, 'succeed')




if __name__ == '__main__':
    url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/signin'
    data = {"name": "tester", "password": "123456"}
    login = Login(url)
    res = login.login_ecshop(data=data)
    print(res)
    session = login.get_session(data)
    print(session)
    user_id = GetKeyword.get_keyword(session, 'uid')
    print(user_id)


