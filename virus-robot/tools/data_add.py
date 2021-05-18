import requests, json
from matplotlib import pyplot as plt
from matplotlib import font_manager
import time

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)


def chinaDayList():
    """中国每日数据"""
    data=[]
    jsondata = json.loads(requests.get(url).json()['data'])
    total = jsondata['chinaTotal']
    add = jsondata['chinaAdd']
    print(jsondata)

    for key in total:
        if not key=='nowConfirm':
            temp = {'value': total[key], 'add': add[key]}
            data.append(temp)
    print(data)
    with open('../data/add_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


    return


chinaDayList()
