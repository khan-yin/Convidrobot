import time, json, requests
from datetime import datetime


# ------------------------------------------------------------------------------
# 第一步 抓取腾讯疫情实时json数据
# 参考文章：许老师博客 https://blog.csdn.net/xufive/article/details/104093197
# ------------------------------------------------------------------------------
def catch_daily():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts&callback=&_=%d' % int(time.time() * 1000)
    data = json.loads(requests.get(url=url).json()['data'])
    data.sort(key=lambda x: x['date'])

    date_list = list()  # 日期
    confirm_list = list()  # 确诊
    suspect_list = list()  # 疑似
    dead_list = list()  # 死亡
    heal_list = list()  # 治愈
    for item in data:
        month, day = item['date'].split('/')
        date_list.append('%s-%s' % (month, day))
        confirm_list.append(int(item['confirm']))
        suspect_list.append(int(item['suspect']))
        dead_list.append(int(item['dead']))
        heal_list.append(int(item['heal']))
    return date_list, confirm_list, suspect_list, dead_list, heal_list


date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()
data = {
    'date': date_list,
    'confirm': confirm_list,
    'suspect': suspect_list,
    'dead':dead_list,
    'heal': heal_list
}
with open('../data/chart_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
print(data)
