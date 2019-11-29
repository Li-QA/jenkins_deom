from common.send_method import SendMethod
from common.get_keyword import GetKeyword
from interface.login import Login


class Collection(object):
    # 查看收藏
    @staticmethod
    def collection_check(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 添加收藏
    @staticmethod
    def collection_add(url, data):
        return SendMethod.send_method(url=url, data=data)

    # 移除收藏
    @staticmethod
    def collection_remove(url, data):
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

    check_url = 'http://ecshop.itsoso.cn/ECMobile/?url=/user/collect/list'
    check_data = {"session": session, "pagination": {"count": 10, "page": 1}, "rec_id": 0}
    add_data = {"session": session, "goods_id": 68}
    remove_data = {"session": session, "rec_id": "2674"}
    res = Collection.collection_check(url=check_url, data=check_data)
    print(res)
