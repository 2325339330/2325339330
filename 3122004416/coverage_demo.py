import coverage
import unittest

# 实例化一个对象
cov = coverage.coverage()
cov.start()

# 测试套件
suite = unittest.defaultTestLoader.discover("./", "test_main.py")
unittest.TextTestRunner().run(suite)


# 结束分析
cov.stop()

# 结果保存
cov.save()

# 命令行模式展示结果
cov.report()

# 生成HTML覆盖率报告
cov.html_report(directory='result_html')