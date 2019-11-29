import jsonpath


class GetKeyword(object):
    @staticmethod
    def get_keyword(response: dict, keyword, index=0):
        """
        获取单个返回值,多个返回值就返回根据自己数据的,或默认的第一个
        :param response: 数据源  传入字典格式
        :param keyword: 要获取的字段
        :return:  返回需要查询的值
        """
        try:
            return jsonpath.jsonpath(response, f"$..{keyword}")[index]
        except:
            print("关键字不存在")
            return False

    @staticmethod
    def get_keywords(response: dict, keyword):
        """
        获取单个返回值,多个返回值就返回根据自己数据的,或默认的第一个
        :param response: 数据源  传入字典格式
        :param keyword: 要获取的字段
        :return:  返回需要查询的值
        """
        try:
            return jsonpath.jsonpath(response, f"$..{keyword}")
        except:
            print("关键字不存在")
            return False


if __name__ == '__main__':
    response = {
        "count": 6,
        "next": "下一页",
        "previous": None,
        "results": [
            {
                "dep_id": "14",
                "dep_name": "duan_14",
                "master_name": "man_14",
                "slogan": "随便"
            },
            {
                "dep_id": "15",
                "dep_name": "duan_15",
                "master_name": "man_15",
                "slogan": "随便"
            },
            {
                "dep_id": "16",
                "dep_name": "duan_16",
                "master_name": "man_16",
                "slogan": "随便"
            },
            {
                "dep_id": "17",
                "dep_name": "duan_17",
                "master_name": "man_17",
                "slogan": "随便"
            },
            {
                "dep_id": "18",
                "dep_name": "duan_18",
                "master_name": "man_18",
                "slogan": "随便"
            },
            {
                "dep_id": "19",
                "dep_name": "duan_19",
                "master_name": "man_19",
                "slogan": "随便"
            }
        ]
    }
    keyword = "master_name"
    keyword1 = "next"
    print(GetKeyword.get_keyword(response, keyword1))
    print(GetKeyword.get_keyword(response, keyword))
    print(GetKeyword.get_keywords(response, keyword))
