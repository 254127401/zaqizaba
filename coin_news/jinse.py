import requests,json,time,threading,re
from app import Simplified2Traditional as cx
from lxml import etree
from mongo import *
class Jinse():
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number):
        print("文章：%s"%url)
        titie_xpath='//*[@class="js-article"]/div/h2'
        content_xpath='//*[@class="js-article"]/p'
        req=requests.get(url,verify=False).text
        # print(req)
        content=Jinse.qwbzj(req,'</component-share>'+'\n</div>\n','\n<div class="tags">')
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        title_complex=cx(title)
        author_complex=cx(author)
        content_complex=cx(content)
        country='CN' ##来源国家
        froms='www.jinse.com'
        try:
             # print(Jinse.qwbzj(req,'</component-share>'+'\n</div>','<div class="tags">'))
            if select_id(url[-11:],country) ==None:   ##查询ID是否存在。不存在则插入
                id = insert_simple(title,author,int(times),int(time.time()),content,froms,sort,url,img_url,brief,country,categories,read_number)
                insert_simple1(id) ##新增ID
                if select_id(url[-11:],'complex')==None:
                    cid=insert_complex(title_complex,author_complex,times,int(time.time()),content_complex,froms,sort,url,img_url,brief,country,id,categories,read_number)
                    insert_complex1(cid)
            else:
                return False
        except Exception as e:
            print("errorrrrrrrrrrrrrrr:"+e.getMessage())
            return False
       
    def jishu():##技术板块
        categories='5af58f97839f3369e4d607ea'
        lianjie=[]
        tid=0
        while True:
            url='https://api.jinse.com/v4/information/list/?catelogue_key=tech&information_id='+str(tid)+'&limit=20&flag=down&version=9.9.9'
            print('当前目录页：%s'%tid)
            req=json.loads(requests.get(url,verify=False).text)
            if len(req['list'])==0:
                break
            for link in req['list']:
                if 'topic_url' in link['extra']:
                    # print(link['extra']['topic_url'])
                    lianjie.append(link['extra']['topic_url'])
                    url,title,author,times,sort,img_url,brief,contentid,read_number=link['extra']['topic_url'],link['title'],link['extra']['author'],link['extra']['published_at'],'技术',link['extra']['thumbnail_pic'],link['extra']['summary'],link['id'],link['extra']['read_number']
                    state = Jinse.content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number)
                    if state == False:
                        break
                        # pass
            if state == False:
                break
                # pass
            tid=req['bottom_id']
    def keyan():##科研板块
        categories='5af58f8d839f3369e4d607e8'
        lianjie=[]
        tid=0
        while True:
            url='https://api.jinse.com/v4/information/list/?catelogue_key=capitalmarket&information_id='+str(tid)+'&limit=20&flag=down&version=9.9.9'
            req=json.loads(requests.get(url,verify=False).text)
            if len(req['list'])==0:
                break
            print(len(req['list']))
            for link in req['list']:
                # print(link['extra']['topic_url'])
                lianjie.append(link['extra'].get('topic_url'))
                if link['extra'].get('topic_url')=='':
                    pass
                elif 'topic_url' in link['extra']:
                    print(link['extra']['topic_url'])
                    url,title,author,times,sort,img_url,brief,contentid,read_number=link['extra']['topic_url'],link['title'],link['extra']['author'],link['extra']['published_at'],'技术',link['extra']['thumbnail_pic'],link['extra']['summary'],link['id'],link['extra']['read_number']
                    state = Jinse.content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number)
                    if state == False:
                        break
            if state==False:
                break
            tid=req['bottom_id']
            print(len(lianjie))
        print(lianjie)
    def yingyong():##应用板块
        categories='5af58f8d839f3369e4d607e8'
        lianjie=[]
        tid=0
        while True:
            url='https://api.jinse.com/v4/information/list/?catelogue_key=application&information_id='+str(tid)+'&limit=20&flag=down&version=9.9.9'
            req=json.loads(requests.get(url,verify=False).text)
            print(req)
            if len(req['list'])==0:
                break
            print(len(req['list']))
            for link in req['list']:
                # print(link['extra']['topic_url'])
                if 'topic_url' in link['extra']:
                    lianjie.append(link['extra']['topic_url'])
                    url,title,author,times,sort,img_url,brief,contentid,read_number=link['extra']['topic_url'],link['title'],link['extra']['author'],link['extra']['published_at'],'技术',link['extra']['thumbnail_pic'],link['extra']['summary'],link['id'],link['extra']['read_number']
                    state = Jinse.content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number)
                    if state ==False:
                        break
            if state==False:
                break
            tid=req['bottom_id']
            print(len(lianjie))
        print(lianjie)
    def chanye():##产业板块
        categories='5af58f92839f3369e4d607e9'
        lianjie=[]
        tid=0
        while True:
            url='https://api.jinse.com/v4/information/list/?catelogue_key=industry&information_id='+str(tid)+'&limit=20&flag=down&version=9.9.9'
            req=json.loads(requests.get(url,verify=False).text)
            print(req)
            if len(req['list'])==0:
                break
            print(len(req['list']))
            for link in req['list']:
                # print(link['extra']['topic_url'])
                if 'topic_url' in link['extra']:
                    lianjie.append(link['extra']['topic_url'])
                    url,title,author,times,sort,img_url,brief,contentid,read_number=link['extra']['topic_url'],link['title'],link['extra']['author'],link['extra']['published_at'],'技术',link['extra']['thumbnail_pic'],link['extra']['summary'],link['id'],link['extra']['read_number']
                    state = Jinse.content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number)
                    if state==False:
                        break
            if state==False:
                break
            tid=req['bottom_id']
            print(len(lianjie))
        print(lianjie)
    def renwu():##人物板块
        categories='5af58f8d839f3369e4d607e8'
        lianjie=[]
        tid=0
        while True:
            url='https://api.jinse.com/v4/information/list/?catelogue_key=personage&information_id='+str(tid)+'&limit=20&flag=down&version=9.9.9'
            req=json.loads(requests.get(url,verify=False).text)
            print(req)
            if len(req['list'])==0:
                break
            print(len(req['list']))
            for link in req['list']:
                # print(link['extra']['topic_url'])
                if 'topic_url' in link['extra']:
                    lianjie.append(link['extra']['topic_url'])
                    url,title,author,times,sort,img_url,brief,contentid,read_number=link['extra']['topic_url'],link['title'],link['extra']['author'],link['extra']['published_at'],'技术',link['extra']['thumbnail_pic'],link['extra']['summary'],link['id'],link['extra']['read_number']
                    state = Jinse.content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number)
                    if state==False:
                        break
            if state==False:
                break
            tid=req['bottom_id']
        print(lianjie)
    def duihua():##对话板块
        categories='5af58f8d839f3369e4d607e8'
        lianjie=[]
        tid=0
        while True:
            url='https://api.jinse.com/v4/information/list/?catelogue_key=zhuanfang&information_id='+str(tid)+'&limit=20&flag=down&version=9.9.9'
            req=json.loads(requests.get(url,verify=False).text)
            print(req)
            if len(req['list'])==0:
                break
            print(len(req['list']))
            for link in req['list']:
                # print(link['extra']['topic_url'])
                if 'topic_url' in link['extra']:
                    lianjie.append(link['extra']['topic_url'])
                    url,title,author,times,sort,img_url,brief,contentid,read_number=link['extra']['topic_url'],link['title'],link['extra']['author'],link['extra']['published_at'],'技术',link['extra']['thumbnail_pic'],link['extra']['summary'],link['id'],link['extra']['read_number']
                    state = Jinse.content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number)
                    if state==False:
                        break
            if state==False:
                break
            tid=req['bottom_id']
        print(lianjie)
    def zhuanlan():##专栏板块
        categories='5af58f8d839f3369e4d607e8'
        lianjie=[]
        tid=1
        while True:
            url='https://api.jinse.com/v4/member/columns?page='+str(tid)
            req=json.loads(requests.get(url,verify=False).text)
            print(req)
            if len(req)==0:
                break
            print(len(req))
            for link in req:
                # print(link['extra']['topic_url'])
                if 'topic_url' in link:
                    lianjie.append(link['topic_url'])
                    url,title,author,times,sort,img_url,brief,contentid,read_number=link['topic_url'],link['title'],link['author'],link['published_at'],'专栏',link['thumbnail_pic'],link['summary'],link['id'],link['read_number']
                    times=Jinse.shijian(times)
                    state = Jinse.content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number)
                    if state==False:
                        break
            if state==False:
                break
            tid+=1
        print(lianjie)
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
        elif len(times)==17:
            timeArray = time.strptime(times, "%Y/%m/%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
        elif len(times)==16:
            times=times+':00'
            timeArray = time.strptime(times, "%Y/%m/%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
    def xinwen():##新闻板块
        categories='5af58f86839f3369e4d607e7'   ## 分类
        lianjie=[]
        tid=0
        while True:
            url='https://api.jinse.com/v4/information/list?catelogue_key=news&limit=10&information_id='+str(tid)+'&flag=down&version=9.9.9'
            req=json.loads(requests.get(url,verify=False).text)
            print(req)
            if len(req['list'])==0:
                break
            print(len(req['list']))
            for link in req['list']:
                # print(link['extra']['topic_url'])
                if 'topic_url' in link['extra']:
                    lianjie.append(link['extra']['topic_url'])
                    url,title,author,times,sort,img_url,brief,contentid,read_number=link['extra']['topic_url'],link['title'],link['extra']['author'],link['extra']['published_at'],'技术',link['extra']['thumbnail_pic'],link['extra']['summary'],link['id'],link['extra']['read_number']
                    state = Jinse.content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number)
                    if state==False:
                        break
            if state==False:
                break
            tid=req['bottom_id']
            print(len(lianjie))
        print(lianjie)
    def shendu():##深度板块
        categories='5af58f92839f3369e4d607e9'
        lianjie=[]
        tid=0
        while True:
            url='https://api.jinse.com/v4/information/list/?catelogue_key=shendu&information_id='+str(tid)+'&limit=20&flag=down&version=9.9.9'
            req=json.loads(requests.get(url,verify=False).text)
            print(req)
            if len(req['list'])==0:
                break
            print(len(req['list']))
            for link in req['list']:
                # print(link['extra']['topic_url'])
                if 'topic_url' in link['extra']:
                    lianjie.append(link['extra']['topic_url'])
                    url,title,author,times,sort,img_url,brief,contentid,read_number=link['extra']['topic_url'],link['title'],link['extra']['author'],link['extra']['published_at'],'技术',link['extra']['thumbnail_pic'],link['extra']['summary'],link['id'],link['extra']['read_number']
                    state = Jinse.content(url,title,author,times,sort,img_url,brief,categories,contentid,read_number)
                    if state==False:
                        break
            if state==False:
                break
            tid=req['bottom_id']
            print(len(lianjie))
        print(lianjie)

if __name__=='__main__':
    Jinse.jishu()
    time.sleep(2)
    Jinse.keyan()
    time.sleep(2)
    Jinse.yingyong()
    time.sleep(2)
    Jinse.chanye()
    time.sleep(2)
    Jinse.renwu()
    time.sleep(2)
    Jinse.duihua()
    time.sleep(2)
    Jinse.zhuanlan()
    time.sleep(2)
    Jinse.xinwen()
    time.sleep(2)
    Jinse.shendu()
