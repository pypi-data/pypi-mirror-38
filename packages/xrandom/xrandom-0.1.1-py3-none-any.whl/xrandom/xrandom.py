# coding:utf-8
import random


def salt(length: int = None):
    length = length or random.randint(8, 12)
    seed = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s = []
    for i in range(length):
        s.append(random.choice(seed))
    return ''.join(s)
