import requests,json,time,re
from lxml import etree
from mongo import *
class Coin():
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def shijian1(date):
        st=time.strptime(date.replace('年','-').replace('月','-').replace('日',''),'%Y-%m-%d')
        return int(time.mktime(st))
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
            timeArray = time.strptime(times, "%Y/%m/%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
        elif len(times)==16:
            times=times+':00'
            timeArray = time.strptime(times, "%Y/%m/%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
        else:
            return int(time.time())
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def content(url,title,author,times,sort,img_url,brief,categories):
        print('文章：%s'%url)
        read_xpath='//*[@class="referral_stats total-views"]/span[2]'
        req=requests.get(url).text
        read=etree.HTML(req).xpath(read_xpath)
        content=Coin.qwbzj(req,'<div class="post-content">','<div class="b-post-subscription">').strip()
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        froms='jp.cointelegraph.com'
        country='JP'
        read_number=read[0].text.strip()
        try:
            if select_id(url,country) ==None:   ##查询ID是否存在。不存在则插入
                id = jp_insert_simple(title,author,int(times),int(time.time()),content,froms,sort,url,img_url,brief,country,categories,read_number)
                jp_insert_simple1(id) ##新增ID
            else:
                return False
        except Exception as e:
            return False
        
    def news():
        categories='5af58f86839f3369e4d607e7'
        page=2
        sort='ニュース'
        token=requests.get('https://jp.cointelegraph.com/').text
        link_xpath='//*[@class="post boxed"]/a'
        title_xpath='//*[@class="image"]/a/img'
        author_xpath='//*[@class="info clearfix"]/span/a'
        date_xpath='//*[@class="info clearfix"]/span[2]'
        req=etree.HTML(token)
        img=req.xpath(title_xpath)
        author=req.xpath(author_xpath)
        date=req.xpath(date_xpath)
        title=req.xpath(title_xpath)
        link=req.xpath(link_xpath)
        print('当前目录页：%s'%1)
        for num in range(len(link)):
            if link[num].get('href')==None:
                break
            state =Coin.content(link[num].get('href'),title[num].get('alt'),author[num].text,Coin.shijian(date[num].text),sort,img[num].get('src'),title[num].get('alt'),categories)
            if state==False:
                break
        token=Coin.qwbzj(token,'meta name="csrf-token" content="','">')
        post_url='https://jp.cointelegraph.com/api/v1/content/json/_mp'
        while True:
            print('当前目录页：%s'%page)
            data={
                'lang':"en",
                'page':page,
                '_token':token
            }
            req=requests.post(post_url,data=data).text
            req=json.loads(req)
            if 'posts' in req:
                for num in req['posts']:
                    try:
                        state=Coin.content(num['url'],num['title'],num['author_title'],Coin.shijian1(num['date']),sort,num['img'],num['lead'],categories)
                        if state==False:
                            break
                    except Exception as e:
                        print(e)
            else:
                break
            if state==False:
                break
            page+=1
            # print(json.loads(req))
if __name__ == '__main__':
    ''' https://jp.cointelegraph.com '''
    Coin.news()
