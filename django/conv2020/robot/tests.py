from django.test import TestCase

# Create your tests here.
import jieba
import re
import time
from collections import Counter

cut_words = ""
wordlist = ""
f = open('ciyun/fenci.txt', 'w')
for line in open('ciyun/C-class.txt', encoding='utf-8'):
    line.strip('\n')
    signalline = jieba.cut(line,cut_all=False)
    # print(signalline)
    # print(" ".join(seg_list))
    signalword = (" ".join(signalline))
    # print(signalword)
    f.write(signalword)
    wordlist += signalword
else:
    f.close()
# 输出结果
wordlist = wordlist.split()
# print(wordlist)

c=Counter()
# 词频统计
c = Counter()
for x in wordlist:
    if len(x)>1 and x != '\r\n':
        c[x] += 1


# 存储数据
name = "fenci.csv"
fp = open(name, 'w', encoding='utf-8')
i = 1
for (k,v) in c.most_common(len(c)):
    fp.write(str(i)+','+str(k)+','+str(v)+'\n')
    i = i + 1
else:
    print("Over write file!")
    fp.close()

