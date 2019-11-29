import pandas as pd


class OperationExcel:
    # 读取数据
    def get_data(self, read_filename):
        # 读取数据
        self.table = pd.read_excel(read_filename)
        data = []
        for i in self.table.index.values:  # 获取行号的索引，遍历行数
            row_data = self.table.loc[i].to_dict()  # 将遍历的每行的数据转化为字典类型
            data.append(row_data)  # 追加到空列表中
        return data  # 返回列表

    # 写入数据
    def write_data(self, write_filename, userinfo):
        data = pd.read_excel(write_filename)  # 读取数据
        index = len(data) + 1  # 获取插入数据的行数值
        data.loc[index] = userinfo  # 将userinfo插入到index行
        data.to_excel(write_filename, sheet_name='Sheet1', header=True, index=False)  # 将数据写入Excel中


# 测试代码
if __name__ == '__main__':
    # 文件路径
    filename = '../data/login_data.xlsx'
    # 实例化
    op_excel = OperationExcel()
    # 读取数据
    data = op_excel.get_data(filename)
    print(data)
    filename = r'D:\pyCharm\Demo\pycode\ECShop\data\register_successed_data.xlsx'
    userinfo = ['11111', '11111', '1111', '1111', '1111']
    data1 = op_excel.write_data(filename, userinfo)
