from mongo import *
import requests,json,time,random,threading
from lxml import etree
class Coin():
    def shijian(times):
        if times.find('刚刚')!=-1:
            return int(time.time())
        elif times.find('秒')!=-1:
            return int(time.time())
        elif times.find('분전')!=-1:
            sj=int(times[:times.find('분전')])
            sj=int(time.time())-sj*60
            return sj
        elif times.find('시간전')!=-1:
            sj=int(times[:times.find('시간전')])
            sj=int(time.time()-sj*60*60)
            return sj
        elif len(times)==19:
            timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
        elif len(times)==16:
            times=times+':00'
            timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
        elif len(times)==25:
            times=Coin.qwbzj(times,'','+').replace('T',' ')
            timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def content(url,title,times,sort,img_url,brief,categories):
        print('文章：%s'%url)
        req=requests.get(url,verify=False).text
        author=Coin.qwbzj(req,'rel="author">','</a></span></div>')
        content=Coin.qwbzj(req,'<div class="cn-content">','<div class="cn-cta-box">').strip()
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        froms='cryptonews.com'
        country='US'
        read_number=0
        try:
            if select_id(url,country) ==None:
                id = us_insert_simple(title,author,int(times),int(time.time()),content,froms,sort,url,img_url,brief,country,categories,read_number)
                us_insert_simple1(id)
            else:
                return False
        except Exception as e:
            return False
        
    def news():
        categories='5af58f86839f3369e4d607e7'
        sort='News'
        offset=0
        title_xpath='//*[@class="props"]/h4/a/text()'
        date_xpath='//*[@datetime]'
        link_xpath='//*[@class="props"]/h4/a'
        briefs_xpath='//*[@class="entry-snippet"]'
        img_xpath='//*[@class="img"]/img'
        while True:
            req=requests.get('https://cryptonews.com/').text
            event=Coin.qwbzj(req,'"event":"','","where')
            where=Coin.qwbzj(req,'"where":"','","')
            data={
                'event':event,
                'where':where,
                'offset':offset
            }
            req=requests.post('https://cryptonews.com/',data=data).text
            con=json.loads(req)
            offset=con['offset']
            req=req.replace("\\",'')
            txt=etree.HTML(req)
            date=txt.xpath(date_xpath)
            title=txt.xpath(title_xpath)
            link=txt.xpath(link_xpath)

            img=txt.xpath(img_xpath)
            if len(link)<3:
                break
            for num in range(len(link)):
                try:
                    brief=title[num]
                    state=Coin.content('https://cryptonews.com'+link[num].get('href'),title[num],Coin.shijian(date[num].get('datetime')),sort,img[num].get('src'),brief,categories)
                    if state ==False:
                        break
                except Exception as e:
                    print(e)

            if state ==False:
                break


if __name__=='__main__':
    ''' cryptonews.com  '''
    Coin.news()

