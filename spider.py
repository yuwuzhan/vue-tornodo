import requests
import xlsxwriter
import time
from random import choice
# import time
# print(time.time())
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
# url = 'http://www.tba.org.tw/lawyer_web/api?API_ID=lawyer_query&page=2&v=1526260050330&forMember=N'
# q = requests.get(url, headers={
#                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
#                  'Host': 'www.tba.org.tw',
#                  'Referer': 'http://www.tba.org.tw/278fecb914.html',
#                  }).json()
# print(q['datas'])


if __name__ == '__main__':
    workbook = xlsxwriter.Workbook('ok.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, '姓名')
    worksheet.write(0, 1, '联系电话')
    worksheet.write(0, 2, '邮箱')
    worksheet.write(0, 3, '传真')
    worksheet.write(0, 4, '公司名称')
    worksheet.write(0, 5, '地址')
    i = 1
    for pagenum in range(1, 829):
        print(pagenum)
        alls = requests.get('http://www.tba.org.tw/lawyer_web/api?API_ID=lawyer_query&page={0}&v={1}&forMember=N'.format(pagenum, int(time.time()*1000)),
                            headers={
            'User-Agent': choice(user_agent_list),
            'Host': 'www.tba.org.tw',
            'Referer': 'http://www.tba.org.tw/278fecb914.html', }).json()
        for each in alls['datas']:
            name = each['name']
            coname = each['CONAME']
            address = each['ADDRESS']
            email = each['EMAIL']
            cophone = each['COPHONE1']
            fax = each['COFAX1']
            worksheet.write(i, 0, name)
            worksheet.write(i, 1, cophone)
            worksheet.write(i, 2, email)
            worksheet.write(i, 3, fax)
            worksheet.write(i, 4, coname)
            worksheet.write(i, 5, address)
            i += 1
    workbook.close()
    print('已抓取结束！ヽ(ˋ▽ˊ)ノ')
