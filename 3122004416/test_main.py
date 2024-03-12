import unittest
from main import PlagiarismDetector
import os
class TestPlagiarismDetector(unittest.TestCase):
    def create_test_files(self):
        with open("original.txt", "w", encoding="utf-8") as f:
            f.write("这是一个测试文件")

        with open("copied1.txt", "w", encoding="utf-8") as f:
            f.write("这是一个复制的文件")

        with open("copied2.txt", "w", encoding="utf-8") as f:
            f.write("这是另一个复制的文件")

    def setUp(self):
        # 创建测试文件
        self.create_test_files()
        # 创建测试实例
        self.detector = PlagiarismDetector("original.txt", ["copied1.txt", "copied2.txt"], "output.txt")

    def test_read_file(self):
        # 测试 read_file 方法是否能正确读取文件内容
        expected_content = "这是一个测试文件"
        self.assertEqual(self.detector.read_file("original.txt"), expected_content)

    def test_chinese_word_cut(self):
        # 测试 chinese_word_cut 方法是否能正确进行中文分词
        text = "你好，我的世界！"
        expected_result = ["你好", "世界"]
        self.assertEqual(self.detector.chinese_word_cut(text), expected_result)

    def test_calculate_similarity(self):
        # 测试 calculate_similarity 方法是否能正确计算相似度
        with open("orig.txt", "r", encoding='utf-8') as file:
            original_text = file.read()
        with open("orig_0.8_del.txt", "r", encoding='utf-8') as file:
            copied_text1 = file.read()
        with open("orig_0.8_dis_1.txt", "r", encoding='utf-8') as file:
            copied_text2 = file.read()
        copied_texts = [copied_text1,copied_text2]
        expected_jaccard_similarity = [0.5715093273035613, 0.8256315465187923]
        expected_difflib_similarity = [0.8303112313937754, 0.926829268292683]

        jaccard_similarity, difflib_similarity = self.detector.calculate_similarity(original_text, copied_texts)
        self.assertEqual(jaccard_similarity, expected_jaccard_similarity)
        self.assertEqual(difflib_similarity, expected_difflib_similarity)

    def test_run(self):
        # 执行run()方法
        self.detector.run()
        # 检查输出文件是否存在
        self.assertTrue(os.path.exists("output.txt"), "output.txt 文件未生成")

        # 检查输出文件内容是否符合预期
        with open("output.txt", "r", encoding="utf-8") as f:
            output_content = f.read()

        expected_output = """Jaccard Similarity:
0.60
0.40

Difflib Similarity:
0.71
0.67

sum_similarity:
0.65
0.53
"""
        self.assertEqual(output_content, expected_output)

    def tearDown(self):
        # 删除测试文件
        import os
        os.remove("original.txt")
        os.remove("copied1.txt")
        os.remove("copied2.txt")
        if os.path.exists("output.txt"):
            os.remove("output.txt")

if __name__ == "__main__":
    unittest.main()