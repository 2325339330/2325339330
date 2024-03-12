import sys
import os
import jieba
from difflib import SequenceMatcher
import re
import cProfile
class PlagiarismDetector:
    def __init__(self, original_file, copied_files, output_file):
        self.original_file = original_file
        self.copied_files = copied_files
        self.output_file = output_file

    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def chinese_word_cut(self, mytext):
        jieba.initialize()  # 初始化jieba
        # 文本预处理 ：去除一些无用的字符只提取出中文出来
        new_data = re.findall('[\u4e00-\u9fa5]+', mytext, re.S)
        new_data = " ".join(new_data)
        # 文本分词
        seg_list_exact = jieba.lcut(new_data)
        result_list = []
        # 读取停用词库
        stop_words_list = ['这个','那个','我的','你的','他的','她的','它的']
        stop_words = set(stop_words_list)

        for word in seg_list_exact:
            if word not in stop_words and len(word) > 1:
                result_list.append(word)     
        return result_list

    def calculate_similarity(self, original_text, copied_texts):
        similarities_jaccard = []
        similarities_difflib = []

        original_words = set(self.chinese_word_cut(original_text))

        for copied_text in copied_texts:
            copied_words = set(self.chinese_word_cut(copied_text))

            # 计算Jaccard相似度
            jaccard_similarity = len(original_words & copied_words) / len(original_words | copied_words)
            similarities_jaccard.append(jaccard_similarity)

            # 计算difflib相似度
            matcher = SequenceMatcher(None, original_text, copied_text)
            difflib_similarity = matcher.ratio()
            similarities_difflib.append(difflib_similarity)

        return similarities_jaccard, similarities_difflib

    def run(self):
        original_text = self.read_file(self.original_file)
        copied_texts = [self.read_file(file) for file in self.copied_files]

        similarities_jaccard, similarities_difflib = self.calculate_similarity(original_text, copied_texts)

        with open(self.output_file, 'w', encoding='utf-8') as file:
            file.write("Jaccard Similarity:\n")
            for similarity in similarities_jaccard:
                file.write(f"{similarity:.2f}\n")

            file.write("\nDifflib Similarity:\n")
            for similarity in similarities_difflib:
                file.write(f"{similarity:.2f}\n")
            
            sum_similarity = [x + y for x, y in zip(similarities_jaccard, similarities_difflib)]
            file.write("\nsum_similarity:\n")
            for similarity in sum_similarity:
                file.write(f"{similarity/2:.2f}\n")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python main.py <original_file> <copied_files...> <output_file>")
        sys.exit(1)
    
    original_file = sys.argv[1]
    copied_files = sys.argv[2:-1]
    output_file = sys.argv[-1]

    # 检查原文文件是否存在
    if not os.path.exists(original_file):
        print(f"Error: Original file '{original_file}' does not exist.")
        sys.exit(1)

    # 检查抄袭版论文文件是否存在
    for file in copied_files:
        if not os.path.exists(file):
            print(f"Error: Copied file '{file}' does not exist.")
            sys.exit(1)

    detector = PlagiarismDetector(original_file, copied_files, output_file)
    detector.run()
    cProfile.run('detector.run()', sort='cumulative')
