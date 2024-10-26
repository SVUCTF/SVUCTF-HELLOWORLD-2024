import random

flag = "flag{po_xiao_yyds}"

print("|原字符|目标字符|原二进制|目标二进制|差值|")
print("|-|-|-|-|-|")

for flag_char in flag:
    flag_ascii = ord(flag_char)
    random_ascii = random.randint(32, flag_ascii)
    ascii_diff = flag_ascii - random_ascii

    orig_binary = random.randint(0, 255 - ascii_diff)
    target_binary = orig_binary + ascii_diff

    random_char = chr(random_ascii)
    orig_bin_str = format(orig_binary, "08b")
    target_bin_str = format(target_binary, "08b")

    print(f"|{random_char}||{orig_bin_str}|{target_bin_str}||")
