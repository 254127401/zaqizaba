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
        elif len(times)==10:
            print(times)
            timeArray = time.strptime(times, "%Y/%m/%d")
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
        content=Coin.qwbzj(req,'<div class="pre_text">','<div class="snsbox">').strip()
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        froms='venturetimes.jp'
        country='JP'
        read_number=0
        try:
            if select_id(url,country) ==None:
                id = jp_insert_simple(title,author,int(times),int(time.time()),content,froms,sort,url,img_url,brief,country,categories,read_number)
                jp_insert_simple1(id)
            else:
                return False
        except Exception as e:
            return False
        
    def news():
        categories='5af58f86839f3369e4d607e7'
        sort='仮想通貨'
        title_xpath='//*[@itemprop="headline"]/text()'
        data_xpath='//*[@class="timedata"]/text()'
        url_xpath='//*[@class="article_list"]/article/a'
        briefs_xpath='//*[@class="article_list"]/article/a/div[3]/p/text()'
        img_xpath='//*[@class="article_list"]/article/a/div[2]/img'
        page=1
        while True:
            url_get='http://venturetimes.jp/category/cryptocurrency/page/%d'%page
            print('当前目录页：%s'%url_get)
            req=requests.get(url_get,verify=False).text
            req=etree.HTML(req)
            title=req.xpath(title_xpath)
            url=req.xpath(url_xpath)
            data=req.xpath(data_xpath)
            briefs=req.xpath(briefs_xpath)
            # author=req.xpath(author_xpath)
            img=req.xpath(img_xpath)
            author='venturetimes'
            if len(title)<2:
                break
            if title != None:
                for num in range(len(title)):
                    try:
                        state=Coin.content(url[num].get('href'),title[num].strip(),author,Coin.shijian(data[num].strip()),sort,img[num].get('src'),briefs[num].strip(),categories)
                        if state == False:
                            break
                    except Exception as e:
                        print(e)
                if state==False:
                    break
            else:
                break
            page+=1
if __name__=='__main__':
    '''http://venturetimes.jp/'''
    Coin.news()
