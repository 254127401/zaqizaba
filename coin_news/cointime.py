from mongo import *
import requests,json,time,random,re
from lxml import etree
class Bointime():
    def shijian(times):
        if times.find('刚刚')!=-1:
            return int(time.time())
        elif times.find('秒')!=-1:
            return int(time.time())
        elif times.find('分钟前')!=-1:
            sj=int(times[:times.find('分钟前')])
            sj=int(time.time())-sj*60
            return sj
        elif times.find('小时前')!=-1:
            sj=int(times[:times.find('小时前')])
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
    def content(url,title,author,times,sort,img_url,brief,categories,read_number):
        print('文章：%s'%url)
        req=requests.get(url,verify=False).text
        content=Bointime.qwbzj(req,'<div class="con line36 font16">','</div>\n<div class="time gray5 font12 margin-b10">').replace('\n','').replace('\r','').replace('\t','')
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        country='JP'
        froms='jp.cointime.com'
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
        tid=0
        while True:
            url='http://jp.cointime.com/ajax/topics-list/www/%d'%tid
            print('当前目录页：%s'%url)
            req=json.loads(requests.get(url,verify=False).text)
            if len(req)==0:
                break
            tid=req['data'][0]['child_id']
            for num in req['data']:
                try:
                    url,title,author,times,sort,img_url,brief,read_number=num['extra']['url'],num['title'],num['extra']['user']['nickname'],num['extra']['created_on'],num['extra']['tag_names'],num['extra']['thumbnail'],num['extra']['summary'],num['extra']['show_read_number']
                    times=Bointime.shijian(times)
                    state=Bointime.content(url,title,author,times,sort,img_url,brief,categories,read_number)
                    if state==False:
                        break
                except Exception as e:
                    print(e)
            if state==False:
                break
if __name__=='__main__':
    ''' http://jp.cointime.com '''
    Bointime.news()
