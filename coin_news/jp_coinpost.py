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
        elif len(times)==10 or len(times)==9:
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
        content=Coin.qwbzj(req,'<div id="the-content" class="entry-content">','<!-- ページリンク -->').strip()
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        ad=Coin.qwbzj(content,'  <!-- 広告 -->','</script></div>')
        jiaoyi=Coin.qwbzj(content,'<div id="text-35" class="widget-in-article widget_text">','''</table>''')
        content=content.replace(ad,'').replace(jiaoyi,'').replace('<div','<p').replace('</div>','</p>')
        froms='coinpost.jp'
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
        sort_xpath='//*[@class="category"]/a/text()'
        title_xpath='//*[@class="content-rwrap"]/a/h2/text()'
        date_xpath='//*[@class="published"]/text()'
        link_xpath='//*[@class="content-lwrap"]/a'
        briefs_xpath='//*[@class="entry-snippet"]'
        img_xpath='//*[@class="content-lwrap"]/a/img'
        page=1
        while True:
            url='http://coinpost.jp/?paged=%d'%page
            print('当前目录页：%s'%url)
            req=requests.get(url).text
            req=etree.HTML(req)
            img=req.xpath(img_xpath)
            author='coinpost'
            date=req.xpath(date_xpath)
            title=req.xpath(title_xpath)
            link=req.xpath(link_xpath)
            sort=req.xpath(sort_xpath)
            briefs=req.xpath(briefs_xpath)
            if len(title)<2:
                break
            if title != None:
                for num in range(len(title)):
                    try:
                        state=Coin.content(link[num].get('href'),title[num].strip(),author,Coin.shijian(date[num].strip()),sort[num],img[num].get('src'),briefs[num].text.strip(),categories)
                        if state == False:
                            break
                    except Exception as e:
                        print(e)
                if state ==False:
                    break
            else:
                break
            page+=1
Coin.news()
