# 导入run_main
import common.run_main as run
import common.read_config as read_cf

cf = read_cf.read_config()

# 发送者与接受者信息
sender = cf.get_value("MAIL", "sender")
password = cf.get_value("MAIL", "password")
recipients = cf.get_value("MAIL", "recipient")
recipient = recipients.split(',')


# 添加测试用例到测试套件中
testsuite = run.add_cases()
# # # 执行所有测试用例
run.run_cases(testsuite)
# 获取最新测试报告
report_file = run.get_latest_report()
# 发送邮件
run.send_mail(sender, password, recipient, report_file)