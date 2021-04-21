import datetime
import requests
from urllib import request

from bs4 import BeautifulSoup






class AlbaInfo:
    area = ''
    name = ''
    title = ''
    pay = ''
    won = ''
    time = ''
    bizType = ''
    addr = ''
    period = ''
    way = ''
    endDate = ''


    def setData(self, _area, _name, _title, _pay, _won, _time, _bizType, _addr, _period, _way, _endDate):
        self.area = _area
        self.name = _name
        self.title = _title
        self.pay = _pay
        self.won = _won
        self.time = _time
        self.bizType = _bizType
        self.addr = _addr
        self.period = _period
        self.way = _way
        self.endDate = _endDate

    def __str__(self):
        returnVal = self.area + ", " + self.name +"," + self.title +"," + self.pay +"," + self.won +","+self.time+","+self.bizType+","+self.addr+","+self.period+","+self.way+","+self.endDate
        return returnVal


def main():

    response = requests.get('https://www.albamon.com/list/gi/mon_gi_list.asp?gubun=2&ps=50&lvtype=2')
    response.encoding = 'euc-kr'
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    resultDiv = soup.select('div[class=gListWrap]')[0].select('tbody')[0]

    albaInfoList = []

    i = 0
    for tr in resultDiv.select('tr'):

        print (i)

        albaInfo = AlbaInfo()


        if (i % 2 == 0):
            area = (tr.select('td.area')[0].text).replace('스크랩', '').strip()
            name = (tr.select('td.subject')[0].select('p.cName')[0].text).strip()
            title = (tr.select('td.subject')[0].select('p.cTit')[0].text).strip()
            pay = tr.select('td.pay p.money img')[0]['alt']
            won = (tr.select('td.pay p.won')[0].text).strip()
            time = (tr.select('td')[3].text).strip()

            print (area)
            print(name)
            print(title)
            print(pay)
            print(won)
            print(time)

        else:
            bizType = (tr.select('td dd')[0].text).strip()
            addr = (tr.select('td dd')[1].text).strip()
            period = (tr.select('td dd')[3].text).strip()
            way = (tr.select('td dd.aWay')[0].text).strip()
            endDate = (tr.select('td dd.end')[0].text).strip()

            albaInfo.setData(area, name, title, pay, won, time, bizType, addr, period, way, endDate)

            print(bizType)
            print(addr)
            print(period)
            print(way)
            print(endDate)
            print('')


            albaInfoList.append(albaInfo)

        i = i + 1



    for x in albaInfoList:
        print(x)








################################################################################
################################################################################
################################################################################
################################################################################
if __name__ == '__main__':
    main()
################################################################################
################################################################################
################################################################################
################################################################################
