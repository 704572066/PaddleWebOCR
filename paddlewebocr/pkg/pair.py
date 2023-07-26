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
    result1 = re.sub(r'[\s,]*', '', '|'.join(list(map(lambda x: x[1][0], a))))

    result2 = re.sub(r'[\s,]*', '', b)
    list2 = list(map(str, result2.split('|')))
    list1 = list(map(str, result1.split('|')))

    set_a = set(list1)
    set_b = set(list2)
    remove_a = set_a - set_b
    print(remove_a)
    remove_b = set_b - set_a
    print(remove_b)
    percentage = len(remove_b) / len(set_b)
    filter_texts = list(filter(lambda x: re.sub(r'[\s,]*', '', x[1][0]) in remove_a, a))
    print(filter_texts)
    return percentage, filter_texts
# for item in remove_b:
#     b.remove(item)
# x = list(zip(a,b))
# for item in x:
#     print(item)