#coding=utf-8
from mongo import *
import requests,json,time,random,re
from lxml import etree
class Coin():
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def shijian(times):
        if times.find('分間')!=-1:
            sj=int(times[:times.find('分間')])
            sj=int(time.time())-sj*60
            return sj
        elif times.find('時間')!=-1:
            sj=int(times[:times.find('時間')])
            sj=int(time.time()-sj*60*60)
            return sj
        elif len(times)==17:
            print(times)
            timeArray = time.strptime(times, "%Y-%m-%d %H:%M")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
        elif len(times)==16:
            times=times+':00'
            timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
        else:
            return int(time.time())
    def content(url,title,author,times,sort,img_url,brief,categories):
        print('文章：%s'%url)
        req=requests.get(url,verify=False).text
        content=Coin.qwbzj(req,'<div class="viewcon" itemprop="articleBody">','<div class="viewcon">').strip()
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        froms='www.blockmedia.co.kr'
        country='KR'
        read_number=0
        try:
            if select_id(url,country) ==None:
                id = kr_insert_simple(title,author,int(times),int(time.time()),content,froms,sort,url,img_url,brief,country,categories,read_number)
                kr_insert_simple1(id)
            else:
                return False
        except Exception as e:
            return False
        

    def news():
        categories='5af58f86839f3369e4d607e7'
        sort='뉴스'
        title_xpath='//*[@class="list_blog"]/li/dl/dt/a'
        data_xpath='//*[@id="content"]/div/ul/li/dl/dd[1]/text()'
        author_xpath='//*[@id="content"]/div/ul/li/dl/dd[1]/text()[2]'
        briefs_xpath='//*[@id="content"]/div/ul/li/dl/dd[2]/a'
        img_xpath='//*[@class="listimg"]/a/img'
        page=1
        while True:
            url_get='https://www.blockmedia.co.kr/?page=%d'%page
            print('当前目录页：%s'%url_get)
            req=requests.get(url_get,verify=False).text
            req=etree.HTML(req)
            title=req.xpath(title_xpath)
            url=req.xpath(title_xpath)
            data=req.xpath(data_xpath)
            briefs=req.xpath(briefs_xpath)
            author=req.xpath(author_xpath)
            img=req.xpath(img_xpath)
            if len(title)<3:
                break
            if title != None:
                for num in range(len(title)):
                    try:
                        state=Coin.content('https://www.blockmedia.co.kr'+url[num].get('href'),title[num].text,author[num],Coin.shijian(data[num].strip()),sort,img[num].get('src'),briefs[num].text,categories)
                        if state == False:
                            exit()
                    except Exception as e:
                        print(e)

            else:
                break
            page+=1
if __name__=='__main__':
    ''' www.blockmedia.co.kr '''
    Coin.news()
