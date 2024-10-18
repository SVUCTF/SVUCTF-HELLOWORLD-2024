import os
import sys
import random
import time
from faker import Faker

LEET_DICT = {"a": "4", "e": "3", "g": "6", "i": "1", "o": "0", "s": "5", "t": "7"}
FLAG = os.environ.get("GZCTF_FLAG", "flag{test_flag}")

fake = Faker()

ASCII_ART = """
  .---------.
  |.-------.|
  ||>1337# ||
  ||       ||
  |"-------'|
.-^---------^-.
| ---~   ---~ |
"-------------'
"""


def generate_random_sentence():
    return fake.sentence(nb_words=random.randint(3, 10), variable_nb_words=True)


def convert_to_leet(sentence):
    return "".join(LEET_DICT.get(char, char) for char in sentence.lower())


def display_rules():
    print("系统日志: 检测到转换模块配置如下")
    for key, value in LEET_DICT.items():
        print(f"{key} -> {value}")
    print()


def play_round():
    sentence = generate_random_sentence()
    correct_leet = convert_to_leet(sentence)

    print(f"输入文本: {sentence}")
    start_time = time.time()
    user_input = input("输出 LEET 文本 > ")
    end_time = time.time()

    if end_time - start_time > 3:
        print("系统警告: 响应超时")
        return False

    if user_input == correct_leet:
        print("转换成功: 系统稳定性 +1")
        return True
    else:
        print(f"转换失败: 系统不稳定性增加")
        return False


def main():
    print(ASCII_ART)
    print("=" * 50)
    print("1337 Machine 唤醒中...")
    print("=" * 50)
    time.sleep(1)
    print("系统日志: 检测到核心不稳定")
    print("系统日志: 启动紧急修复程序")
    print("系统日志: 需要执行 100 次成功的 LEET 转换以重新校准系统")
    time.sleep(1)
    display_rules()

    input("按下回车键开始系统修复...")

    successful_conversions = 0
    for i in range(1, 101):
        print(f"\n系统日志: 开始第 {i} 次转换")
        if play_round():
            successful_conversions += 1
            print(f"系统状态: {successful_conversions}/100")
        else:
            print(f"\n系统日志: 修复失败")
            print(f"系统日志: 仅完成 {successful_conversions}/100 次成功转换")
            print("系统日志: 进入紧急休眠模式")
            return

    print("\n系统日志: 修复成功，Flag 核心已稳定")
    print(f"Flag: {FLAG}")


if __name__ == "__main__":
    main()
