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
def texts_pair(a, b):
    result1 = re.sub(r',+', '', '|'.join(list(map(lambda x: x[1][0], a))))
    result1 = re.sub(r'\s+', '|', result1)

    result2 = re.sub(r',+', '', b)
    result2 = re.sub(r'\s+', '|', result2)
    list2 = list(map(str, result2.split('|')))
    list1 = list(map(str, result1.split('|')))

    set_a = set(list1)
    set_b = set(list2)
    print(set_b)
    print('-----------\n')
    print(set_a)
    remove_a = set_a - set_b
    print(remove_a)
    remove_b = set_b - set_a
    print(remove_b)
    percentage = len(remove_b) / len(set_b)
    filter_texts = list(filter(lambda x: not set(re.sub(r'\s+', '|', re.sub(r',+', '', x[1][0])).split('|')).isdisjoint(remove_a), a))
    print(filter_texts)
    return percentage, filter_texts
# for item in remove_b:
#     b.remove(item)
# x = list(zip(a,b))
# for item in x:
#     print(item)
# b = "aa    bb  cc d,:d   77"
# a =  re.sub(r'\s+', '|', b)
# a =  re.sub(r',', '', a)
# t = re.sub(r',+', '', "99 ii    p,,,ppp")
# print(t)
# m = re.sub(r'\s+', '|', t)
# print(m)
# c = re.sub(r'\s+', '|', re.sub(r',+', '', "99 ii    p,,,ppp")).split('|')
# result1 = set(re.sub(r'\s+', '|', re.sub(r',+', '', x[1][0])).split('|')).isdisjoint(remove_a)
# print(c)
# print(result1)
# p = {'ppp'}
# print(result1.isdisjoint(p))