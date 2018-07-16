import requests,json,time,threading,re
from app import Simplified2Traditional as cx
from lxml import etree
from mongo import *
class Coin():
    def shijian(times):
        timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return int(timeStamp)
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def content(url,title,author,times,sort,img_url,brief,categories,read_number):
        print(url,title,author,times,sort,img_url,brief,categories,read_number)
        print("文章：%s"%url)
        req=requests.get(url,verify=False).text
        # print(req)
        content='<div class="con line36 font16">'+Coin.qwbzj(req,'<div class="con line36 font16">','<div class="time gray5 font12 margin-b10">').strip()
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        country='KR' ##来源国家
        froms='kr.cointime.com'
        try:
             # print(Jinse.qwbzj(req,'</component-share>'+'\n</div>','<div class="tags">'))
            if select_id(url,country) ==None:   ##查询ID是否存在。不存在则插入
                id = kr_insert_simple(title,author,int(times),int(time.time()),content,froms,sort,url,img_url,brief,country,categories,read_number)
                kr_insert_simple1(id) ##新增ID
            else:
                return False
        except Exception as e:
            print("errorrrrrrrrrrrrrrr:"+e)
            return False
    def news(): #咨讯
        sort="百科"
        categories='5af58f8d839f3369e4d607e8'
        tid=1
        while True:
            url='http://kr.cointime.com/ajax/topics-list/wiki/%d'%tid
            req=requests.get(url).text
            req=json.loads(req)
            tid=req['data'][0]['child_id']
            if len(req['data'])<=2:
                break
            for text in req['data']:
                times=Coin.shijian(text['created_at'])
                titleid=text['extra']['url']
                viewNum=text['extra']['show_read_number']
                title=text['extra']['title']
                imageUrl=text['extra']['thumbnail']
                articleSummary=text['extra']['summary']
                editor=text['extra']['user']['nickname']
                state=Coin.content(titleid,title,editor,times,sort,imageUrl,articleSummary,categories,viewNum)
                if state==False:
                    break
                print('===========================================================================')
            if state==False:
                break
                # print(titleid,viewNum,title,imageUrl,articleSummary,editor,times)
if __name__=='__main__':
    Coin.news()