import collections
import re

a = [
 'And',
 "you're",
 'going',
 'to',
 'use',
 'some',
 'handouts.',
 'Okay.',
 'So',
 'I',
 'needed',
 'to',
 'know',
 'and',
 'for,'
]

b = [
 'And',
 "you're",
 'going',
 'to',
 'use',
 'some',
 'handouts.',
 'Okay.',
 'I',
 'needed',
 'to',
 'know',
 'and',
 'for,',
 'it'
]
def texts_pair_algorithm_a(a, b):
    result1 = re.sub(r'[,()（）:.：\']*', '', '|'.join(list(map(lambda x: x[1][0], a))))
    result1 = re.sub(r'\s+', '|', result1)

    result2 = re.sub(r'[,()（）:.\']*', '', b)
    result2 = re.sub(r'\s+', '|', result2)
    list2 = list(map(str, result2.split('|')))
    list1 = list(map(str, result1.split('|')))

    set_a = set(list1)
    set_b = set(list2)
    # print(set_b)
    # print('-----------\n')
    # print(set_a)
    remove_a = set_a - set_b
    # print(remove_a)
    remove_b = set_b - set_a
    # print(remove_b)
    vin1 = re.compile(".*5LMP.*")
    vin2 = re.compile(".*LVSP.*")
    list1 = list(filter(vin1.match, list(remove_b)))  # Read Note below
    list2 = list(filter(vin2.match, list(remove_b)))  # Read Note below
    percentage = len(remove_b) / len(set_b)
    if len(list1) > 0 or len(list2) > 0:
        percentage = 1
    # percentage = len(remove_b) / len(set_b)
    filter_texts = list(filter(lambda x: not set(re.sub(r'\s+', '|', re.sub(r'[,()（）:.\']*', '', x[1][0])).split('|')).isdisjoint(remove_a), a))
    # print(filter_texts)
    return percentage, filter_texts

def texts_pair_algorithm_aa(a, b):
    result1 = re.sub(r'[,()（）:.。?：;\'\"]*', '', '|'.join(list(map(lambda x: x[1][0], a))))
    result1 = re.sub(r'\s+', '|', result1)
    result1 = re.sub('.R2TB-1532-EA', '|R2TB-1532-EA', result1)
    result1 = re.sub('SEATINGCAPACITY.TOTAL', '|SEATINGCAPACITYTOTAL', result1)

    result2 = re.sub(r'[,()（）:.。?：;\'\"]*', '', b)
    result2 = re.sub(r'\s+', '|', result2)
    list2 = list(map(str, result2.split('|')))
    list1 = list(map(str, result1.split('|')))

    set_a = collections.Counter(list1)
    set_b = collections.Counter(list2)

    print("aa set_a: %s" % set_a)
    print("aa set_b: %s" % set_b)
    # print(set_b)
    # print('-----------\n')
    # print(set_a)
    remove_a = set_a - set_b
    print(remove_a)
    remove_b = set_b - set_a
    print(remove_b)
    vin1 = re.compile(".*5LMP.*")
    vin2 = re.compile(".*LVSP.*")
    list1 = list(filter(vin1.match, list(remove_b)))  # Read Note below
    list2 = list(filter(vin2.match, list(remove_b)))  # Read Note below
    percentage = sum(remove_b.values()) / sum(set_b.values())
    if len(list1) > 0 or len(list2) > 0:
        percentage = 1
    # percentage = len(remove_b) / len(set_b)
    filter_texts = list(filter(lambda x: not set(re.sub(r'\s+', '|', re.sub(r'[,()（）:.。?：;\'\"]*', '', x[1][0])).split('|')).isdisjoint(remove_a), a))
    print(filter_texts)
    print("aa percentage: %s" % percentage)
    return percentage, filter_texts

def texts_pair_algorithm_b(a, b):
    result1 = re.sub(r'[\s,()（）:.。\']*', '', '|'.join(list(map(lambda x: x[1][0], a))))
    result1 = re.sub('.*R2TB-1532-EA', '|R2TB-1532-EA', result1)
    result1 = re.sub('SEATINGCAPACITY.*TOTAL', '|SEATINGCAPACITYTOTAL', result1)

    result2 = re.sub(r'[\s,()（）:.。\']*', '', b)
    list2 = list(map(str, result2.split('|')))
    list1 = list(map(str, result1.split('|')))

    set_a = set(list1)
    print("set_a: %s" % set_a)
    set_b = set(list2)
    print("set_b: %s" % set_b)
    remove_a = set_a - set_b
    print(remove_a)
    remove_b = set_b - set_a
    print(remove_b)
    vin1 = re.compile(".*5LMP.*")
    vin2 = re.compile(".*LVSP.*")
    list1 = list(filter(vin1.match, list(remove_b)))  # Read Note below
    list2 = list(filter(vin2.match, list(remove_b)))  # Read Note below
    percentage = len(remove_b) / len(set_b)
    if len(list1) > 0 or len(list2) > 0:
        percentage = 1
    filter_texts = list(filter(lambda x: re.sub(r'[\s,()（）:.\']*', '', x[1][0]) in remove_a, a))
    # print(filter_texts)
    print("bb percentage: %s" % percentage)
    return percentage, filter_texts

def texts_pair_algorithm_bb(a, b):
    result1 = re.sub(r'[\s,()（）:.。?：;\'\"]*', '', '|'.join(list(map(lambda x: x[1][0], a))))
    result1 = re.sub('.R2TB-1532-EA', '|R2TB-1532-EA', result1)
    result1 = re.sub('SEATINGCAPACITY.TOTAL', '|SEATINGCAPACITYTOTAL', result1)

    result2 = re.sub(r'[\s,()（）:.。?：;\'\"]*', '', b)
    list2 = list(map(str, result2.split('|')))
    list1 = list(map(str, result1.split('|')))

    set_a = collections.Counter(list1)
    print("bb set_a: %s" % set_a)
    set_b = collections.Counter(list2)
    print("bb set_b: %s" % set_b)
    remove_a = set_a - set_b
    print(remove_a)
    remove_b = set_b - set_a
    print(remove_b)
    vin1 = re.compile(".*5LMP.*")
    vin2 = re.compile(".*LVSP.*")
    list1 = list(filter(vin1.match, list(remove_b)))  # Read Note below
    list2 = list(filter(vin2.match, list(remove_b)))  # Read Note below
    percentage = sum(remove_b.values()) / sum(set_b.values())
    if len(list1) > 0 or len(list2) > 0:
        percentage = 1
    filter_texts = list(filter(lambda x: re.sub(r'[\s,()（）:.。?：;\'\"]*', '', x[1][0]) in remove_a, a))
    # print(filter_texts)
    print("bb percentage: %s" % percentage)
    return percentage, filter_texts

def split_chinese(strings):
    _char = None
    for _char in strings:
        if ('\u0030' <= _char <= '\u0039') or (u'\u0041' <= _char <= u'\u005a') or (u'\u0061' <= _char <= u'\u007a'):
            return _char
def split_shu(strings):
    _char = None
    for _char in strings:
        if _char == '\u007c':
            return _char
def split_texts(texts):
    i = 0
    split_texts = []
    while i < len(texts):
        str = texts[i][1][0]
        _char = split_shu(str)
        if _char is not None:
            index = str.find(_char)
            if 0 < index < len(str):
                split_texts.append([texts[i][0], (re.sub('[|]', '', str[: index]), texts[i][1][1])])
                split_texts.append([texts[i][0], (re.sub('[|]', '', str[index:]), texts[i][1][1])])
                i += 1
                continue
        split_texts.append([texts[i][0], (texts[i][1][0], texts[i][1][1])])
        i += 1
    return split_texts

# for item in remove_b:
#     b.remove(item)
# x = list(zip(a,b))
# for item in x:
#     print(item)
# b = "aa    bb  cc d,:d   77"
# a =  re.sub(r'\s+', '|', b)
# a =  re.sub(r',', '', a)
# t = re.sub(r',:+', '', "99 ii    p,,,p:pp")
# print(t)
# m = re.sub(r'\s+', '|', t)
# print(m)
# c = re.sub(r'\s+', '|', re.sub(r',+', '', "99 ii    p,,,ppp")).split('|')
# result1 = set(re.sub(r'\s+', '|', re.sub(r',+', '', x[1][0])).split('|')).isdisjoint(remove_a)
# print(c)
# print(result1)
# p = {'ppp'}
# print(result1.isdisjoint(p))
#
# result1 = re.sub(r'[\s,()（）\']*', '', "LES OBJETS DANS LE RETROVISEUR|SONTPLUS PRESQU'ILS|NE LE SEMBLENT|YHU5A-214A96-AA")
# print(result1)

# mylist = ["dog", "rcat", "wildcatr", "thundercat", "cow", "hooo"]
# vin1 = re.compile(".*5LMP.*")
# vin2 = re.compile(".*LVSP.*")
# newlist = list(filter(vin1.match, mylist)) # Read Note below
# newlist = list(filter(vin2.match, mylist)) # Read Note below
# print("pp:%s"%(newlist))