# coding:utf-8
import random


def salt(length: int = None, hint: bool = False):
    length = length or random.randint(8, 12)
    seed = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s = []
    for i in range(length):
        s.append(random.choice(seed))
    salt = ''.join(s)

    if hint:
        return salt, shrink_to_hint(salt)
    else:
        return salt


def shrink_to_hint(s: str):
    length = len(s)
    if (length < 4): return '*' * length
    return s[0] + '*' * (length - 2) + s[length - 1]


def fake_name(gender='male', nation='us'):
    import requests

    # https://randomuser.me/
    r = requests.get('https://randomuser.me/api/?gender={gender}&nat={nation}'.format(
        gender=gender, nation=nation
    ))

    name = r.json()['results'][0]['name']
    # picture = r.json()['results'][0]['picture']['large'].strip()
    first_name = name['first'].strip().capitalize()
    last_name = name['last'].strip().capitalize()
    return first_name, last_name
