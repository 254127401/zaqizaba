from mongo import *
import requests,json,time,random,threading,re
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
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def content(url,title,author,sort,img_url,brief,categories):
        date_xpath='//*[@class="vc_top"]/p'
        print("文章：%s"%url)
        req=requests.get(url,verify=False).text
        content=Coin.qwbzj(req,'<div class="vc_con">','</div><!-- //vc_con -->').strip()
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        req=etree.HTML(req)
        date=req.xpath(date_xpath)
        froms='www.webdaily.co.kr'
        country='KR'
        read_number=0
        times=Coin.shijian(date[0].text.split('|')[0].strip())
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
        sort='정치·사회'
        title_xpath='//*[@class="w1"]/h4/a/text()'
        link_xpath='//*[@class="w1"]/h4/a'
        img_xpath='//*[@class="ldv2"]/ul/li/a/img'
        brief_xpath='//*[@class="ldv2"]/ul/li/div/p/a/text()'
        date_xpath='//*[@class="articleListDate marginB8"]/text()'
        page=1
        while True:
            url='http://www.webdaily.co.kr/list.php?ct=g0600&ssk=&sds=&nmd=1&pg=%d'%page
            print('当前目录页：%s'%url)
            req=requests.get(url,verify=False).text
            req=etree.HTML(req)
            date=req.xpath(date_xpath)
            title=req.xpath(title_xpath)
            link=req.xpath(link_xpath)
            img=req.xpath(img_xpath)
            author='웹데일리'
            brief=req.xpath(brief_xpath)
            if len(link)<2:
                break
            if len(link)!= 0:
                for num in range(len(link)):
                    try:
                        state=Coin.content(link[num].get('href'),title[num].strip(),author,sort,img[num].get('src'),brief[num].strip(),categories)
                        if state == False:
                            exit()
                    except Exception as e:
                        print(e)
            elif len(link)<2:
                break
            page+=1
if __name__=='__main__':
    ''' http://www.webdaily.co.kr/list.php?ct=g0600'''
    Coin.news()
