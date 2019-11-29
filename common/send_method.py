import requests
import json

class SendMethod:
    @staticmethod
    def send_method(url, data):
        """选择请求方式"""
        method_data = {"json": json.dumps(data)}
        res = requests.post(url=url, data=method_data)
        return res.json()
        

    @staticmethod
    def dict_2_json(res):
        """将结果进行json格式化输出"""
        return json.dumps(res, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/signin "
    data = {"name": "grj123456", "password": "grj123456"}
    res = SendMethod.send_method(url, data)
    print(SendMethod.dict_2_json(res))
