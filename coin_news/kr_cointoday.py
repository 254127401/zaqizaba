from mongo import *
import requests,json,time,random,threading,re
from lxml import etree
class Coin():
    def shijian(times):
        times=times.replace(' ','').replace('년','-').replace('월','-').replace('일',' ')
        timeArray = time.strptime(times, "%Y-%m-%d %H:%M")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def content(url,title,author,date,sort,img_url,brief,categories):
        print("文章：%s"%url)
        req=requests.get(url,verify=False).text
        content=Coin.qwbzj(req,'<div class="td-post-content td-pb-padding-side">','<a href="http://creativecommons.org/licenses/by-nc-nd/2.0/kr/"').strip().replace('<p>&lt; ©코인투데이(cointoday.co.kr), 무단전재 및 재배포 금지 &gt;</p>','')
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        froms='cointoday.co.kr'
        country='KR'
        read_number=0
        times=date
        try:
            if select_id(url,country) ==None:
                id = kr_insert_simple(title,author,int(times),int(time.time()),content,froms,sort,url,img_url,brief,country,categories,read_number)
                kr_insert_simple1(id)
            else:
                return False
        except Exception as e:
            return False
        
    def news():
        categories='5af58f92839f3369e4d607e9'
        sort='항목'
        title_xpath='//*[@class="td-block-row"]/div/div/h3/a/text()'
        link_xpath='//*[@class="td-block-row"]/div/div/h3/a'
        img_xpath='//*[@class="td-block-row"]/div/div/div/div/a/img'
        brief_xpath='//*[@class="td-block-row"]/div/div/div[3]/text()'
        date_xpath='//*[@class="td-block-row"]/div/div/div[2]/span/time/text()'
        page=1
        while True:
            url='http://cointoday.co.kr/category/coins/page/%d/'%page
            print('当前目录页：%s'%url)
            req=requests.get(url,verify=False).text
            req=etree.HTML(req)
            date=req.xpath(date_xpath)
            title=req.xpath(title_xpath)
            link=req.xpath(link_xpath)
            img=req.xpath(img_xpath)
            author='웹데일리'
            brief=req.xpath(brief_xpath)

            #print(link[0].get('href'),title[0].strip(),author,Coin.shijian(date[num])sort,img[0].get('src'),brief[0].strip(),categories,date[0])
            if len(link)<2:
                break
            if len(link)!= 0:
                for num in range(len(link)):
                    try:
                        state=Coin.content(link[num].get('href'),title[num].strip(),author,Coin.shijian(date[num]),sort,img[num].get('src'),brief[num].strip(),categories)
                        if state == False:
                            exit()
                    except Exception as e:
                        print(e)
            elif len(link)<2:
                break
            page+=1
if __name__=='__main__':
    ''' http://cointoday.co.kr'''
    Coin.news()
