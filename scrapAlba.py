import pymysql
import datetime
import requests
from urllib import request
import math
from rich import print as rprint
from bs4 import BeautifulSoup

DB_HOST_NAME = "YOUR_DATABASE_HOST_NAME"
DB_PORT = "YOUR_DATABASE_PORT"
DB_USERNAME = "YOUR_DATABASE_USERNAME"
DB_PASSWORD = "YOUR_DATABASE_PASSWORD"
DB_DATABASE_NAME = "YOUR_DATABASE_NAME"


def getMariaConnection():
    host_name = DB_HOST_NAME
    port = DB_PORT
    username = DB_USERNAME
    password = DB_PASSWORD
    database_name = DB_DATABASE_NAME

    db = pymysql.connect(host=host_name, port=port, user=username, password=password, db=database_name, charset='utf8')

    return db

def insertMaria(data):
    db = getMariaConnection()

    cursor = db.cursor()

    selectSql = '''
        SELECT * FROM albamon_recruit where site_id=%s
    '''

    cursor.execute(selectSql, data.getSiteId())

    result = cursor.fetchall()

    if len(result) < 1:
        rprint('[', data, ']')
        insertSql = '''
        INSERT INTO albamon_recruit
        (
             site_id, area, name, title
             , pay, won, time, biz_type
             , addr, period_date, way, end_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        cursor.execute("set names utf8")
        db.commit()

        cursor.execute(insertSql,
                       (
                           data.getSiteId(), data.getArea(), data.getName(), data.getTitle()
                           , data.getPay(), data.getWon(), data.getTime(), data.getBizType()
                           , data.getAddr(), data.getPeriod(), data.getWay(), data.getEndDate()
                       )
                      )

        db.commit()

    else:
        f = open('C:/opt/albaOverLap.txt', 'a')
        checkId = "id가 [%s] 게시글은 중복되었습니다. \n" % (data.getSiteId())
        f.write(checkId)
        f.close()


class AlbaInfo:
    siteId = 0
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

    def getSiteId(self):
        return self.siteId

    def getArea(self):
        return self.area

    def getName(self):
        return self.name

    def getTitle(self):
        return self.title

    def getPay(self):
        return self.pay

    def getWon(self):
        return self.won

    def getTime(self):
        return self.time

    def getBizType(self):
        return self.bizType

    def getAddr(self):
        return self.addr

    def getPeriod(self):
        return self.period

    def getWay(self):
        return self.way

    def getEndDate(self):
        return self.endDate

    def setData(self, _siteId, _area, _name, _title, _pay, _won, _time, _bizType, _addr, _period, _way, _endDate):
        self.siteId = _siteId
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
        returnVal = self.siteId + ", " + self.area + ", " + self.name +"," + self.title +"," + self.pay +"," + self.won +","+self.time+","+self.bizType+","+self.addr+","+self.period+","+self.way+","+self.endDate
        return returnVal


def main():

    #https://www.albamon.com/list/gi/mon_gi_list.asp?page=1&gubun=2&ps=50&lvtype=2&tc=25290
    response = requests.get('https://www.albamon.com/list/gi/mon_gi_list.asp?gubun=2&ps=50&lvtype=2')
    response.encoding = 'euc-kr'
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    totalCountStr = soup.select('div[class=pageSubTit]')[0].select('em')[0].text.strip()

    pageSize = 20

    totalCount = totalCountStr.replace(',', '')

    totalPage = math.ceil(int(totalCount) / pageSize)

    for i in range(totalPage):
        rprint(i+1152)

        url = 'https://www.albamon.com/list/gi/mon_gi_list.asp?page={0}&gubun=2&ps=50&lvtype=2&tc=25290'.format(i+1152)
        #url = 'https://www.albamon.com/list/gi/mon_gi_list.asp?page=73&gubun=2&ps=50&lvtype=2&tc=25290'

        res = requests.get(url)
        res.encoding = 'euc-kr'
        html = res.text

        soup = BeautifulSoup(html, 'html.parser')

        resultDiv = soup.select('div[class=gListWrap]')[0].select('tbody')[0]

        albaInfoList = []

        j = 0

        for tr in resultDiv.select('tr'):

            albaInfo = AlbaInfo()

            if (j % 2 == 0):        # class가 exp
                area = (tr.select('td.area')[0].text).replace('스크랩', '').strip()
                name = (tr.select('td.subject')[0].select('p.cName')[0].text).strip()
                siteId = (tr.select('td.subject')[0].select('p.cName')[0].find('a')["href"].split('?')[1].split('=')[1].split('&')[0]).strip()
                title = (tr.select('td.subject')[0].select('p.cTit')[0].text).strip()

                if tr.select('td.pay span'):
                    if tr.select('td.pay span.eduTrainee'):
                        pay = (tr.select('td.pay span.eduTrainee')[0].text).strip()
                        won = pay
                    else:
                        pay = ''
                        won = ''
                else:
                    pay = tr.select('td.pay p.money img')[0]['alt']
                    won = (tr.select('td.pay p.won')[0].text).strip()

                time = (tr.select('td')[3].text).strip()

            else:                   # class가 preview
                if tr.select('td dd'):
                    bizType = (tr.select('td dd')[0].text).strip()
                    addr = (tr.select('td dd')[1].text).strip()
                    period = (tr.select('td dd')[3].text).strip()
                    way = (tr.select('td dd.aWay')[0].text).strip()
                    endDate = (tr.select('td dd.end')[0].text).strip()
                else:
                    bizType = ''
                    addr = ''
                    period = ''
                    way = ''
                    endDate = ''
                    j = j + 1

                    f = open('C:/opt/albaDDNone.txt', 'a')
                    checkId = "cName이 [%s] [ %s ]인 게시글은 preview 폼없이 exp만 있습니다.\n" %(siteId, name)
                    f.write(checkId)
                    f.close()

                albaInfo.setData(siteId, area, name, title, pay, won, time, bizType, addr, period, way, endDate)
                albaInfoList.append(albaInfo)

            j = j + 1

        for x in albaInfoList:
           insertMaria(x)




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