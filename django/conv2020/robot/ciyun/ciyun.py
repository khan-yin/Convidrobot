#coding:utf-8
import os
import jieba
import wordcloud
import chardet
import imageio
mask = imageio.imread("1.jpeg")

w=wordcloud.WordCloud(width=1000,height=700,background_color='gray',font_path='msyh.ttc',
                      mask=mask,scale=15)

#
# cut_words = ""
# wordlist = ""
# f = open('fenci.txt', 'w')
# for line in open('C-class.txt', encoding='utf-8'):
#     line.strip('\n')
#     signalline = jieba.cut(line,cut_all=False)
#     # print(signalline)
#     # print(" ".join(seg_list))
#     signalword = (" ".join(signalline))
#     # print(signalword)
#     f.write(signalword)
#     wordlist += signalword
# else:
#     f.close()
# 输出结果
# wordlist = wordlist.split()

# print(wordlist)

f = open('C-class.txt', encoding='utf-8')
wordlist=f.read()
# txt="同济大学（Tongji University）简称“同济”，是中华人民共和国教育部直属并由教育部、国家海洋局和上海市共建的全国重点大学，历史悠久、享有盛誉的中国著名高等学府，中央直管高校，国家“世界一流大学建设高校”，国家“211工程”和“985工程”建设高校；入选国家“珠峰计划”、“2011计划”、“111计划”、卓越工程师教育培养计划、卓越法律人才教育培养计划、卓越医生教育培养计划、国家大学生创新性实验计划、国家建设高水平大学公派研究生项目、中国政府奖学金来华留学生接收院校、国家级大学生创新创业训练计划、国家创新人才培养示范基地、新工科研究与实践项目、全国深化创新创业教育改革示范高校、中美“10+10”计划、学位授权自主审核单位，联合国环境规划署全球环境与可持续发展大学合作联盟主席单位，国际设计艺术院校联盟、21世纪学术联盟、卓越大学联盟、中俄工科大学联盟、中欧工程教育平台、国际绿色校园联盟、同济—伯克利工程联盟成员。"
txtlist=jieba.lcut(wordlist)
string="".join(txtlist)


w.generate(string)
w.to_file('wuhanjiayou.png')


