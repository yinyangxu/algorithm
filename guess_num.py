#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
有一个猜数字游戏，庄家预先写下一个四位数字（每位数字各不相同），玩家每次随机猜4个数字，
庄家告知玩家猜对了几A几B（A代表数字和位置都相同，B代表包含该数字但位置不同，
比如如果庄家写的是3514，玩家猜的是3165，庄家会回答1A2B），玩家继续猜，直到猜中为止。
如果超过5轮没猜中，则玩家输，否则玩家赢。请为玩家设计一个猜数字的算法，确保玩家能够大概率胜。
例如：庄家写下9876，玩家第一次猜0123，庄家回复0A0B；玩家继续猜4567，庄家回复0A2B；
依次下去，直到玩家猜中9876为止。
"""


MAX_GUESS_COUNT = 5


def generate_all_nums():
    """初始化生成所有可能的10*9*8*7=5040种数字结果字符串"""

    num_list = []
    
    # 定义数字范围为0~9
    digit_range = range(10)
    
    for d1 in digit_range:
        for d2 in digit_range:
            if d2 == d1:
                continue
            for d3 in digit_range:
                if (d3 == d2) or (d3 == d1):
                    continue
                for d4 in digit_range:
                    if (d4 == d3) or (d4 == d2) or (d4 == d1):
                        continue

                    num_list.append(str(d1) + str(d2) + str(d3) + str(d4))

    return num_list


def get_best_guess_num(guess_list):
    """
    这里牺牲一点性能来对结果集进行统计，统计数字出现频率高的，
    这样若猜错了可以多过滤掉一些数字，这里只统计千位数
    """

    best_guess_num = guess_list[0]

    if len(guess_list) <= 2:
        # 少于两个元素的话统计也没啥意义，直接取第一个返回
        return best_guess_num

    # 初始化千位数上0~9出现的次数
    freq = [0] * 10

    for num in guess_list:
        thousand_digit = int(num[0])
        freq[thousand_digit] += 1
        
    most_freq_digit_str = str(freq.index(max(freq)))
    for num in guess_list:
        if num[0] == most_freq_digit_str:
            best_guess_num = num
            break

    return best_guess_num
    
    
def judge(guess_num, secret_num):
    """猜测后庄家给出猜测结果"""

    # 初始化A和B的个数为0
    total_a = 0
    total_b = 0

    for i in range(4):
        if guess_num[i] == secret_num[i]:
            total_a += 1
        elif guess_num[i] in secret_num:
            total_b += 1

    return "%dA%dB" % (total_a, total_b)
                

def cut_guess_list(guess_list, guess_num, reply):
    """
    根据猜测结果过滤出具有相同结果（比如都为1A1B）的元素
    """
    
    new_guess_list = []
    
    # 先排除掉猜错的数
    guess_list.remove(guess_num)


    # 过滤掉不符合猜测结果的元素
    i = 0
    while (i < len(guess_list)):
        target = guess_list[i]
        result = judge(target, guess_num)
        if result == reply:
            new_guess_list.append(target)
            
        i += 1

    return new_guess_list
    

def main():
    
    secret_num = raw_input('-> 请输入庄家的四位数字：')
    
    guess_list = generate_all_nums()

    guess_count = 1
    while (guess_count <= MAX_GUESS_COUNT):
        if (1 == guess_count):
            # 第一次猜"0123"，第一次猜每个数字的概率相同，这里取第一个
            guess_num = guess_list[0]
        else:
            # 从第二次开始对结果集进行统计，选数字出现次数多的猜，这里暂且统计千位数
            guess_num = get_best_guess_num(guess_list)

        win_rate = round(float(1) / len(guess_list), 4)
        print "第%d次算法猜的数字：%s，剩余未猜个数：%d，胜率：%.2f%%" % (guess_count, guess_num,
                                                   len(guess_list), win_rate*100)
                         
        reply = judge(guess_num, secret_num)
        
        if reply == '4A0B':
            print "庄家回答：%s 猜对了！！！" % reply
            break
        else:
            print "庄家回答：%s" % reply
            guess_list = cut_guess_list(guess_list, guess_num, reply)

        guess_count += 1
    

if __name__ == '__main__':
    main()


