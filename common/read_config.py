import os
import configparser

# 当前执行脚本的绝对路径
cur_path = os.path.dirname(os.path.realpath(__file__))
# 当前配置文件的路径
cf_path = os.path.join(cur_path, "config.ini")


# 读取配置文件信息
class read_config(object):
    # 初始化
    def __init__(self):
        self.cf = configparser.ConfigParser()
        # 读取配置文件
        self.cf.read(filenames=cf_path, encoding='utf-8')

    # 读取配置数据
    def get_value(self, section, params):
        # 获取配置文件中指定section下参数的值
        value = self.cf.get(section, params)
        return value


if __name__ == '__main__':
    config = read_config()
    host = config.get_value("DATABASE", "host")
    print(host)

