import requests
import json

class nCovData():

    def __init__(self):

        # 获取原始全国疫情数据的网址
        self.start_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'

    def get_html_text(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'}
        res = requests.get(self.start_url, headers=headers, timeout=30)
        res.encoding = 'utf-8'
        # 将获取到的json格式的字符串类型数据转换为python支持的字典类型数据
        data = json.loads(res.text)
        # 所有的疫情数据,data['data']数据还是str的json格式需要转换为字典格式，包括：中国累积数据、各国数据(中国里面包含各省及地级市详细数据)、中国每日累积数据(1月13日开始)
        all_data = json.loads(data['data'])
        # print(all_data)
        return all_data


class ProvinceData():

    def __init__(self):
        # 获取所有的疫情数据，字典格式
        self.ncovdata = nCovData()
        self.all_data = self.ncovdata.get_html_text()

    def province_total_data(self):
        '''获取各省的累积数据'''
        # areaTree对应的第一个数据就是中国，下面的children对应的就是每个省份的数据，是一个列表
        areaTree = self.all_data['areaTree'][0]['children']
        province_name = list()
        province_total_confirm = list()
        virus_data = []
        heal_data=[]
        dead_data=[]
        for province in areaTree:
            virus_temp= {'name': province['name'], 'value': province['total']['confirm']}
            heal_temp={'name': province['name'], 'value':round(province['total']['heal']/province['total']['confirm']*100,2)}
            dead_temp={'name':province['name'],'value':province['total']['dead']}
            virus_data.append(virus_temp)
            heal_data.append(heal_temp)
            dead_data.append(dead_temp)

        print(dead_data)
        with open('../data/china-data.json', 'w', encoding='utf-8') as f:
            json.dump(areaTree, f, ensure_ascii=False)
        with open('../data/data.json', 'w', encoding='utf-8') as f:
            json.dump(virus_data, f, ensure_ascii=False)
        with open('../data/heal_data.json', 'w', encoding='utf-8') as f:
            json.dump(heal_data, f, ensure_ascii=False)
        with open('../data/dead_data.json', 'w', encoding='utf-8') as f:
            json.dump(dead_data, f, ensure_ascii=False)
        return province_name, province_total_confirm

    def province_today_data(self):
        '''获取各省今日数据'''
        areaTree = self.all_data['areaTree'][0]['children']
        province_name = list()
        province_today_confirm = list()
        province_today_suspect = list()
        province_today_dead = list()
        province_today_heal = list()
        for province in areaTree:
            province_name.append(province['name'])
            province_today_confirm.append(province['today']['confirm'])
            province_today_heal.append(province['total']['heal'])
        # print(province_today_confirm)

    def main(self):
        self.province_total_data()
        self.province_today_data()

if __name__ == '__main__':
    province_data= ProvinceData()
    province_data.main()
