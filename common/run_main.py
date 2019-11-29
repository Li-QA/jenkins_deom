import unittest
import HTMLTestRunnerPlugins
import zmail
import os, time


# 定义加载测试用例
def add_cases(case_path="./script", rule="test_*.py"):
    """加载所有的测试用例"""
    # 实例化测试套件对象
    testsuite = unittest.TestSuite()
    # 筛选测试用例
    discover = unittest.defaultTestLoader.discover(case_path, pattern=rule)
    # 将筛选的测试用例加载到测试套件中
    testsuite.addTests(discover)
    return testsuite


# 定义执行测试用例，生成测试报告
def run_cases(all_cases, report_path="./report"):
    """测试所有的测试用例，并生成测试报告"""
    # 确定生成的测试报告名
    now = time.strftime('%Y-%m-%d %H-%M-%S')  # 时间
    report_name = report_path + '/' + now + '-report.html'  # 文件名
    # 打开文件并写入测试结果
    with open(report_name, 'wb') as fp:
        runner = HTMLTestRunnerPlugins.HTMLTestRunner(
            title='自动化测试结果报告',
            description='自动化测试详细数据参考文件',
            stream=fp
        )
        runner.run(all_cases)


# 定义获取最新测试报告
def get_latest_report(report_path="./report"):
    """获取测试报告文件存储路径下最新的测试报告"""
    # 返回指定文件路径下的所有文件（无序）
    lists = os.listdir(report_path)
    # 将文件按照修改时间进行升序排列
    lists.sort(key=lambda fn: os.path.getmtime(report_path + "\\" + fn))
    # 获取最新的测试报告
    report_file = os.path.join(report_path, lists[-1])
    return report_file


# 定义发送邮件
def send_mail(sender, password, recipient, report_file):
    """将测试报告以邮件的形式发送给指定收件人"""
    # 读取测试报告内容
    with open(report_file, 'r', encoding='utf-8') as fp:
        content = fp.read()
    # 邮件内容
    mail_content = {
        "subject": "自动化测试报告",
        "content_html": content,
        "attachments": report_file
    }
    # 发送邮件
    server = zmail.server(username=sender, password=password)
    server.send_mail(recipient, mail_content)
    print('邮件发送成功！')


if __name__ == '__main__':
    sender = 'tester@qq.com'
    password = '123456'
    recipient = 'tester@qq.com'
    # 调用方法
    testsuite = add_cases()
    run_cases(testsuite)
    report_file = get_latest_report()
    send_mail(sender, password, recipient, report_file)
