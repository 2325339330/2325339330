# 论文查重算法项目
| 这个作业属于哪个课程 |[软件工程2024 (广东工业大学)](https://edu.cnblogs.com/campus/gdgy/SoftwareEngineering2024) |
| ----------------- | --------------- |
| 这个作业要求在哪里 |[个人项目](https://edu.cnblogs.com/campus/gdgy/SoftwareEngineering2024/homework/13136) |
| 这个作业的目标 |写一个程序实现论文查重功能 |

## 一、[作业GitHub链接](https://github.com/2325339330/2325339330)

## 二、需求

### 题目：论文查重

&emsp;&emsp;设计一个论文查重算法，给出一个原文文件和一个经过增删改的抄袭版论文文件，在答案文件中输出其重复率。

### 输入输出规范

&emsp;&emsp;从命令行参数给出原文文件的绝对路径、抄袭版论文的绝对路径、输出的答案文件的绝对路径。

### 示例

- 原文示例：今天是星期天，天气晴，今天晚上我要去看电影。
- 抄袭版示例：今天是周天，天气晴朗，我晚上要去看电影。


## 三、需求设计
- **功能拆分：** 将功能分解为多个模块，如文件读取、文本处理、相似度计算、结果输出等。
- **语言选择：** 考虑使用现有的工具和库来简化开发过程，提高稳定性，所以用了python。
- **编码测试：** 编码过程中，按照拆分的模块逐步实现功能，并进行测试验证每个模块的正确性。

## 四、模块实现
### 初始化函数(__init__)：

- 接收原文文件路径、抄袭版论文文件路径列表和输出文件路径作为参数。
- 将这些参数保存为对象属性，以备后续使用。

### 读取文件函数(read_file)：

- 接收文件路径作为参数，使用utf-8编码方式读取文件内容。
- 返回文件内容。

### 中文分词函数(chinese_word_cut)：

- 使用jieba库对中文文本进行分词。
- 预处理文本，去除无用字符，只保留中文字符。
- 过滤停用词，保留长度大于1的词语。
- 返回分词结果列表。

### 计算相似度函数(calculate_similarity)：

- 对原文和抄袭版论文进行中文分词。
- 使用[Jaccard相似度](https://baike.baidu.com/item/Jaccard%E7%B3%BB%E6%95%B0/6784913)和[difflib库](https://docs.python.org/zh-cn/3/library/difflib.html)计算文本相似度。
- 返回Jaccard相似度和difflib相似度列表。

### 运行函数(run)：

- 读取原文和抄袭版论文的内容。
- 调用计算相似度函数计算相似度。
- 将相似度求平均值写入输出文件。

### 主程序入口：

- 通过sys.argv获取命令行参数，sys.argv[1]是原文文件路径，sys.argv[2:-1]是抄袭版论文文件路径列表，sys.argv[-1]是输出文件路径实现一篇文章对多篇文章的比较。
- 实例化PlagiarismDetector对象，并调用运行函数。
## 五、使用方法
- 输入: `python main.py <original_file> <copied_files...> <output_file>`
> python main.py "D:\python code\orig.txt" "D:\python code\orig_0.8_add.txt" "D:\python code\orig_0.8_del.txt" "D:\python code\orig_0.8_dis_1.txt" "D:\python code\orig_0.8_dis_10.txt" "D:\python code\orig_0.8_dis_15.txt" "D:\python code\output.txt"

![](https://img2024.cnblogs.com/blog/3399042/202403/3399042-20240312012519836-1378968658.png)

- 打开output.txt,查看结果


![](https://img2024.cnblogs.com/blog/3399042/202403/3399042-20240312013127366-554797193.png)


## 六、性能改进
如图所示，这个程序中性能消耗集中在以下几个方面：
- **difflib.SequenceMatcher的使用：** difflib.SequenceMatcher在计算文本相似度时消耗了大量时间，特别是在调用ratio()方法时。这可能是因为它在内部执行了比较复杂的字符串匹配算法，导致性能较低。

- **中文分词的性能消耗：** 使用jieba进行中文分词时，消耗了一定的时间。尤其是在调用jieba.lcut()方法和相关的分词操作时，性能较低。

计划改进方法：
- 优化文本相似度计算算法：替换difflib库中的相似度计算方法，可以使用一些更高效的文本相似度计算算法来提高性能。
- 使用其他更高效的中文分词工具

![](https://img2024.cnblogs.com/blog/3399042/202403/3399042-20240312013029453-1831934239.png)

## 七、测试单元
测试单元利用了unittest框架，通过运行coverage_demo.py调用test_main.py再调用main.py测试覆盖率，主要测试了以下内容：
- 测试 read_file 方法是否能正确读取文件内容。`def test_read_file(self):`
- 测试 chinese_word_cut 方法是否能正确进行中文分词。`def test_chinese_word_cut(self)`
- 测试 calculate_similarity 方法是否能正确计算相似度。`def test_calculate_similarity(self)`
- 检查输出文件内容是否符合预期。`test_run(self)`

测试截图：

![](https://img2024.cnblogs.com/blog/3399042/202403/3399042-20240312175202981-111319509.png)

![](https://img2024.cnblogs.com/blog/3399042/202403/3399042-20240312175122345-1450980668.png)

### 测试指导

&emsp;&emsp;在进行代码测试时，按照指定的方式输入多个文件的位置，并向指定的文件输出答案。所以主程序未覆盖部分也经过测试

## 八、异常处理
当输入文件不存在时，系统会提示并退出
`PS D:\python code> python main.py "D:\python code\or.txt" "D:\python code\orc.txt" "D:\python code\output.txt" `
`Error: Original file 'D:\python code\or.txt' does not exist.                    #or.txt不存在`
![](https://img2024.cnblogs.com/blog/3399042/202403/3399042-20240312021427487-1986836598.png)

## 附录：PSP表格
| Personal Software Process Stages | 预估耗时（分钟） | 实际耗时（分钟） |
|---------------------------------|-------------------|-------------------|
| **Planning**                        |     20              |     15              |
| - Estimate                      |         20          |         15          |
| **Development**                     |      410             |     555              |
| - Analysis                      |           120       |          160         |
| - Design Spec                  |            40       |           30        |
| - Design Review                |            10       |            5       |
| - Coding Standard             |           5        |              5     |
| - Design                        |          30         |            15       |
| - Coding                         |         150          |          240         |
| - Code Review                 |            15       |              10     |
| - Test                           |        40           |           90        |
| **Reporting**                      |        30           |         35          |
| - Test Report                  |        10           |        15           |
| - Size Measurement          |            10       |           10        |
| - Postmortem & Process Improvement Plan |   10      |          10         |
| **合计**                               |     460              |          605         |
