import jieba
import json
import os
from django.conf import settings


def split(sentence):
    seg_list = jieba.cut_for_search(sentence)  # 搜索引擎模式
    result = list(seg_list)

    return result

def wordVector(text,wordset):
    L = [0] * len(wordset)  # [2,1,0,0,1]
    for i in range(len(text)):
        if text[i] in wordset:
            L[wordset.index(text[i])] += 1

    return L

def cosVector(x,y):
    if(len(x)!=len(y)):
        print('error input,x and y is not in the same space')
        return
    result1=0.0
    result2=0.0
    result3=0.0
    for i in range(len(x)):
        result1+=x[i]*y[i]   #sum(X*Y)
        result2+=x[i]**2     #sum(X*X)
        result3+=y[i]**2     #sum(Y*Y)
    #print(result1)
    #print(result2)
    #print(result3)
    return str(result1/((result2*result3)**0.5))

#匹配句子
#sentence为输入文本，text为语料库
def match(sentence,text):
    score=[]
    sentenceResult = split(sentence)
    for i in range(len(text)):
        textResult = split(text[i])
        #制作共同分词
        result=textResult+sentenceResult
        length = len(result)
        result = list(set(result))
        L_sentence=wordVector(sentenceResult,result)
        L_text=wordVector(textResult,result)
        score.append(cosVector(L_sentence,L_text))
    maxCosIndex = score.index(max(score))
    return maxCosIndex, max(score)

def getAnswer(question, text, answer):
    index, maxScore = match(question, text)
    maxScore = float(maxScore)
    if maxScore<=0.4:
        return '我好像不明白。'
    if 0.7 >= maxScore > 0.4:
        return '我猜您想问的是:\n'+text[index]+'\n'+answer[index]
    if maxScore>0.7:
        #print(text[index])
        return answer[index]


def ReturnAnswer(sentence):
    # 打开文件
    text=[]
    answer=[]
    rumor=[]
    jsonname = 'data/' + 'answer.json'
    filename = os.path.join(settings.STATICFILES_DIRS[0], jsonname)
    f=open(filename, encoding='utf-8')
    f=json.load(f)
    #print(len(f))
    for i in range(len(f)):
        text.append(f[i]['question'])
        answer.append(f[i]['answer'])

    return getAnswer(sentence,text,answer)

#
# text=[]
# answer=[]
# rumor=[]
# # jsonname = 'data/' + 'answer.json'
# # filename = os.path.join(settings.STATICFILES_DIRS[0], jsonname)
# f=open('../../templates/static/data/answer.json', encoding='utf-8')
#
# f=json.load(f)
# print(len(f))
# for i in range(len(f)):
#     text.append(f[i]['question'])
#     answer.append(f[i]['answer'])
#
# print (getAnswer('Thank you',text,answer))
