import score_checker
import string
import os


# dictionaryの読み込み
def load_dictionary(file_path):
    with open(file_path) as f:
        dict_origin = f.read().splitlines() # 改行\nを無視するためにsplitlines

    # 得点順位並べ替える
    dict_sorted = sorted(dict_origin, key = lambda word: score_checker.calculate_score(word), reverse=True)

    # 辞書の元の単語(chr)とそこで使われているアルファベット数(list)の対応表
    dict_new = {}
    for word in dict_sorted:
        letter_count = [0] * 26 # アルファベット数カウントリストの初期化
        for l in word: # wordの文字数をカウントする
            letter_count[ord(l) - ord('a')] += 1
        dict_new[word] = letter_count
    
    # 新しい辞書
    return dict_new


# letter_count1がletter_count2のサブセットかどうかの判定
def is_subset(letter_count1, letter_count2):
    return all(letter_count1[ord(l) - ord('a')] <= letter_count2[ord(l) - ord('a')] for l in string.ascii_lowercase) 


# 1つの単語とカウント済みの辞書について線形探索
def find_best_anagram(test, dict_new): 
    # 空の文字数カウントリスト
    letter_count_test = [0] * 26 
    for l in test: # wordの文字数をカウントする
        letter_count_test[ord(l) - ord('a')] += 1

    # 部分集合のanagramを見つける
    for word in dict_new.items():
        if is_subset(word[1], letter_count_test) == True: 
            return word[0] # ソートされているので、1番点数が高いもの
    return "Cannot find any answer."


# testファイルの読み込み
def load_test_file(file_path):
    with open(file_path) as f:
        tests = f.read().splitlines() # 改行\nを無視するためにsplitlines
    
    return tests

# testファイルの探索
def find_best_anagrams_in_test_file(test_file_path, dict_new): 
    ans = []
    tests = load_test_file(test_file_path)
    for test in tests:
        ans.append(find_best_anagram(test, dict_new))
    return ans

# print関数
def print_ans(ans):
    for word in ans:
        print(word)

# 書き出し関数
def write_ans(file_name, ans):
    with open(f"{file_name}_answer.txt", mode='w') as f:
        f.write("\n".join(ans))
    print("保存完了")

def main():
    print("Write the File Path to Dictionary")
    dict_file_path = str(input())
    print("Write the File Path to Test File")
    test_file_path = str(input())

    dict_new = load_dictionary(dict_file_path)
    
    ans = find_best_anagrams_in_test_file(test_file_path, dict_new)

    print_ans(ans)

    write_ans(os.path.splitext(test_file_path)[0], ans)

if __name__ == '__main__':
    main()