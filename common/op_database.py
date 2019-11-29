from interface.login import Login
from common.get_keyword import GetKeyword
import pymysql


class OpDatabase(object):
    # 定义 __init__
    def __init__(self, host='ecshop.itsoso.cn', user='ecshop', password='ecshop', db='ecshop', port=3306, charset='utf8'):
        # 绑定初始属性
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.charset = charset
        # 初始化连接对象
        self.cn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            port=self.port,
            charset=self.charset
        )
        # 初始化游标对象
        self.cursor = self.cn.cursor(cursor=pymysql.cursors.SSDictCursor)

    # 定义读取一条数据
    def get_one(self, sql, args=None):
        # 执行SQL语句
        self.cursor.execute(sql, args)
        # 读取数据
        return self.cursor.fetchone()

    # 定义读取所有数据
    def get_all(self, sql, args=None):
        # 执行SQL语句
        self.cursor.execute(sql, args)
        # 读取数据
        return self.cursor.fetchall()

    # 定义写入数据
    def write(self, sql, args=None):
        # 开启事务
        self.cn.begin()
        try:
            # 执行SQL语句，写入数据
            num = self.cursor.execute(sql, args)
            if num == 0:
                # 抛出异常
                raise Exception('受影响行数为0，写入失败')
            # 提交事务
            self.cn.commit()
            return True
        except Exception as e:
            # 回滚事务
            self.cn.rollback()
            # 打印错误信息
            print('错误信息：', e)
            return False

    # 重置用户信息
    def clear_mysql(self):
        # 重置账号信息.
        url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/signin"
        login = Login(url)
        data = {"name": "tester", "password": "123456"}
        session = login.get_session(data)
        user_id = GetKeyword.get_keyword(session,"uid")
        # 删除注册的数据
        sql = "delete from ecs_users where user_name = 'tester2'"
        self.cursor.execute(sql)
        # 清空收藏夹
        sql1 = f"delete from ecs_collect_goods where user_id={user_id}"
        self.cursor.execute(sql1)
        # 清空收货地址
        sql2 = f"delete from ecs_user_address where user_id={user_id}"
        self.cursor.execute(sql2)
        # 清空所有订单状态
        sql3 = f"delete from ecs_order_info where user_id={user_id}"
        self.cursor.execute(sql3)
        # 清除购物车记录
        sql4 = f'delete from ecs_cart where user_id = {user_id}'
        self.cursor.execute(sql4)

    def delete_user(self, uid):
        sql = f"delete from ecs_users where user_id = {uid}"
        self.cursor.execute(sql)


if __name__ == '__main__':
    op_database = OpDatabase()
    # # 读取数据
    # sql = 'select * from ecs_order_info where user_id = 9655 and pay_status = 0 and order_status=0'
    # data = op_database.get_one(sql)
    # print(data)
    # # 清空
    # login = OpDatabase()
    # login.clear_mysql()



    
