import collections
import re

# 特殊处理
def re_sub(result1):
    result1 = re.sub('.R2TB-1532-EA', '|R2TB-1532-EA', result1)
    result1 = re.sub('SEATINGCAPACITY.TOTAL', '|SEATINGCAPACITYTOTAL', result1)
    result1 = re.sub(r'制造年月[/1]', '制造年月', result1)
    result1 = re.sub(r'福特多', '福特', result1)
    result1 = re.sub(r'公司.+造[|]', '公司制造|', result1)
    return result1

def re_sub_aa(text, remove):
    # 先把字符串中的float的点号替换成^,再过滤其他点号,最后把^再替换成点号，目的是保留float类型的数字中的点号
    text = re.sub(r'([0-9])[.]([0-9])', r'\g<1>^\g<2>', text)
    text = re.sub(r'[,()（）.。?;，、\"]*', '', text)
    result1 = re.sub(r'([0-9])[\^]([0-9])', r'\g<1>.\g<2>', text)

    # 单引号和冒号不替换为空而是替换成|  避免这种情况："SEATING CAPACITY ' TOTAL： 5 'FRONT :2'REAR:3"
    result1 = re.sub(r'[：:\s\']+', '|', result1)
    result1 = re_sub(result1)
    return not set(list(filter(lambda x: x, result1.split('|')))).isdisjoint(remove)

def re_sub_bb(text, remove):
    # 先把字符串中的float的点号替换成^,再过滤其他点号,最后把^再替换成点号，目的是保留float类型的数字中的点号
    text = re.sub(r'([0-9])[.]([0-9])', r'\g<1>^\g<2>', text)
    text = re.sub(r'[\s,()（）:.。?：;，、\'\"]*', '', text)
    result1 = re.sub(r'([0-9])[\^]([0-9])', r'\g<1>.\g<2>', text)
    # result1 = re.sub(r'[\s,()（）:.。?：;，、\'\"]*', '', text)
    # result1 = re.sub(r'\s+', '|', result1)
    result1 = re_sub(result1)
    return result1 in remove

def text_split(x):
    # print(X)
    # 先把字符串中的float的点号替换成^,再过滤其他点号,最后把^再替换成点号，目的是保留float类型的数字中的点号
    x = re.sub(r'([0-9])[.]([0-9])', r'\g<1>^\g<2>', x)
    x = re.sub(r'[,()（）.。?;，、\"]*', '', x)
    result1 = re.sub(r'([0-9])[\^]([0-9])', r'\g<1>.\g<2>', x)

    # result1 = re.sub(r'[,()（）.。?;，、\"]*', '', x)
    result1 = re.sub(r'[：:\s\']+', '|', result1)
    result1 = '|'+re_sub(result1)+'|'
    result1 = result1.replace('||', '|')
    # print("text1: "+ result1)
    return result1


def collection_counter(a, b):
    result1 = list(map(text_split, list(map(lambda x: x[1][0], a))))
    # 单引号和冒号不替换为空而是替换成|  避免这种情况："SEATING CAPACITY ' TOTAL： 5 'FRONT :2'REAR:3"
    print(result1)

    # 先把字符串中的float的点号替换成^,再过滤其他点号,最后把^再替换成点号，目的是保留float类型的数字中的点号
    b = re.sub(r'([0-9])[.]([0-9])', r'\g<1>^\g<2>', b)
    b = re.sub(r'[,()（）:.。?：;，、\'\"]*', '', b)
    result2 = re.sub(r'([0-9])[\^]([0-9])', r'\g<1>.\g<2>', b)
    # result2 = re.sub(r'[,()（）:.。?：;，、\'\"]*', '', b)
    result2 = '|' + re.sub(r'\s+', '|', result2) + '|'
    print(result2)

    # list1 = list(filter(lambda x: not x in result2, result1))
    list1 = []
    for item in result1:
        print(item)
        if item in result2:
            # list1.append(item)
            result2 = result2.replace(item, '|', 1)
            # print(result2)
        else:
            list1.append(item)
    # print('A|B' in 'A|B|D|B')
    list1 = list(filter(lambda x: x, ('|'.join(list1).split('|'))))
    return collections.Counter(list1)

def texts_pair_algorithm(a, b):
    percentage_a, filter_texts_a, aa_vin = texts_pair_algorithm_aa(a, b)
    percentage_b, filter_texts_b, set_b, remove_b, bb_vin = texts_pair_algorithm_bb(a, b)
    print("remove_b: %s" % remove_b)
    filter_texts = list(filter(lambda x: x[1][0] in list(map(lambda x: x[1][0], filter_texts_a)), filter_texts_b))
    # list1 = list(map(lambda x: re.sub(r'制造年月[/1]', '制造年月', re.sub('SEATINGCAPACITY.TOTAL', '|SEATINGCAPACITYTOTAL', re.sub('.R2TB-1532-EA', '|R2TB-1532-EA', re.sub(r'[\s,()（）:.。?：;，、\'\"]*', '', x[1][0])))), filter_texts))
    # remove_b = collections.Counter(list1) - set_b
    # percentage = sum(remove_b.values())/sum(set_b.values())
    percentage = percentage_a if percentage_a < percentage_b else percentage_b
    if len(filter_texts) == 0:
        percentage = 0
    if aa_vin or bb_vin:
        percentage = 1
    # print("list1: %s" % list1)

    print("percentage: %s" % percentage)
    print("filter_texts_a: %s" % filter_texts_a)
    print("filter_texts_b: %s" % filter_texts_b)
    print("filter_texts: %s" % filter_texts)
    return percentage, filter_texts


def texts_pair_algorithm_aa(a, b):
    a_str = '|'.join(list(map(lambda x: x[1][0], a)))
    # 先把字符串中的float的点号替换成^,再过滤其他点号,最后把^再替换成点号，目的是保留float类型的数字中的点号
    a_str = re.sub(r'([0-9])[.]([0-9])', r'\g<1>^\g<2>', a_str)
    a_str = re.sub(r'[,()（）.。?;，、\"]*', '', a_str)
    result1 = re.sub(r'([0-9])[\^]([0-9])', r'\g<1>.\g<2>', a_str)

    # 单引号和冒号不替换为空而是替换成|  避免这种情况："SEATING CAPACITY ' TOTAL： 5 'FRONT :2'REAR:3"
    result1 = re.sub(r'[：:\s\']+', '|', result1)
    result1 = re_sub(result1)

    # 先把字符串中的float的点号替换成^,再过滤其他点号,最后把^再替换成点号，目的是保留float类型的数字中的点号
    b = re.sub(r'([0-9])[.]([0-9])', r'\g<1>^\g<2>', b)
    b = re.sub(r'[,()（）:.。?：;，、\'\"]*', '', b)
    result2 = re.sub(r'([0-9])[\^]([0-9])', r'\g<1>.\g<2>', b)

    result2 = re.sub(r'\s+', '|', result2)
    list2 = list(map(str, result2.split('|')))
    list1 = list(map(str, result1.split('|')))

    # 去除空值
    # list1 = list(filter(lambda x: x, list1))

    set_a = collections.Counter(list1)
    set_b = collections.Counter(list2)

    print("aa set_a: %s" % set_a)
    print("aa set_b: %s" % set_b)
    # print(set_b)
    # print('-----------\n')
    # print(set_a)
    # remove_a = set_a - set_b
    # 考虑到这种情况：Manufacturer and Vehicle commercial Name 和 Manufacturer Name, 不使用set_a - set_b
    remove_a = collection_counter(a, b)
    print(remove_a)
    remove_b = set_b - set_a
    print(remove_b)
    vin1 = re.compile(".*5LM.*")
    vin2 = re.compile(".*LVS.*")
    list1 = list(filter(vin1.match, list(remove_b)))  # Read Note below
    list2 = list(filter(vin2.match, list(remove_b)))  # Read Note below
    percentage = sum(remove_b.values()) / sum(set_b.values())
    aa_vin = False
    if len(list1) > 0 or len(list2) > 0:
        aa_vin = True
    # percentage = len(remove_b) / len(set_b)
    # filter_texts = list(filter(lambda x: not set(list(filter(lambda x: x, re.sub(r'制造年月[/1]', '制造年月',re.sub('SEATINGCAPACITY.TOTAL', '|SEATINGCAPACITYTOTAL',re.sub('.R2TB-1532-EA', '|R2TB-1532-EA', re.sub(r'\s+', '|',re.sub(r'[,()（）:.。?：;，、\'\"]*','', x[1][0]))))).split('|')))).isdisjoint(remove_a), a))
    filter_texts = list(filter(lambda x: re_sub_aa(x[1][0], remove_a), a))
    print(filter_texts)
    print("aa percentage: %s" % percentage)
    return percentage, filter_texts, aa_vin

def texts_pair_algorithm_bb(a, b):
    a_str = '|'.join(list(map(lambda x: x[1][0], a)))
    # 先把字符串中的float的点号替换成^,再过滤其他点号,最后把^再替换成点号，目的是保留float类型的数字中的点号
    a_str = re.sub(r'([0-9])[.]([0-9])', r'\g<1>^\g<2>', a_str)
    a_str = re.sub(r'[\s,()（）:.。?：;，、\'\"]*', '', a_str)
    result1 = re.sub(r'([0-9])[\^]([0-9])', r'\g<1>.\g<2>', a_str)
    result1 = re_sub(result1)

    # 先把字符串中的float的点号替换成^,再过滤其他点号,最后把^再替换成点号，目的是保留float类型的数字中的点号
    b = re.sub(r'([0-9])[.]([0-9])', r'\g<1>^\g<2>', b)
    b = re.sub(r'[\s,()（）:.。?：;，、\'\"]*', '', b)
    result2 = re.sub(r'([0-9])[\^]([0-9])', r'\g<1>.\g<2>', b)

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
    vin1 = re.compile(".*5LM.*")
    vin2 = re.compile(".*LVS.*")
    list1 = list(filter(vin1.match, list(remove_b)))  # Read Note below
    list2 = list(filter(vin2.match, list(remove_b)))  # Read Note below
    percentage = sum(remove_b.values()) / sum(set_b.values())
    bb_vin = False
    if len(list1) > 0 or len(list2) > 0:
        bb_vin = True
    # filter_texts = list(filter(lambda x: re.sub(r'制造年月[/1]', '制造年月', re.sub('SEATINGCAPACITY.TOTAL', '|SEATINGCAPACITYTOTAL', re.sub('.R2TB-1532-EA', '|R2TB-1532-EA', re.sub(r'[\s,()（）:.。?：;，、\'\"]*', '', x[1][0])))) in remove_a, a))
    filter_texts = list(filter(lambda x: re_sub_bb(x[1][0], remove_a), a))
    # print(filter_texts)
    print("bb percentage: %s" % percentage)
    return percentage, filter_texts, set_b, remove_b, bb_vin

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