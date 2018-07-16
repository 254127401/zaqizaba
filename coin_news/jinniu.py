import requests,json,time,threading,re
from app import Simplified2Traditional as cx
from lxml import etree
from mongo import *
class Jinniu():
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def content(url,title,author,times,sort,img_url,brief,categories,read_number):
        url='http://www.jinniu.cn/news/%s'%url
        # print(url,title,author,times,sort,img_url,brief,categories,read_number)
        print("文章：%s"%url)
        req=requests.get(url,verify=False).text
        # print(req)
        content=Jinniu.qwbzj(req,'window.__NUXT__=',';</script>')
        content=json.loads(content)
        content=content['data'][0]['news']['articleContent']
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        title_complex=cx(title)  ##翻译繁体
        author_complex=cx(author)
        content_complex=cx(content)
        country='CN' ##来源国家
        froms='www.jinniu.cn'
        try:
             # print(Jinse.qwbzj(req,'</component-share>'+'\n</div>','<div class="tags">'))
            if select_id(url,country) ==None:   ##查询ID是否存在。不存在则插入
                id = insert_simple(title,author,int(times),int(time.time()),content,froms,sort,url,img_url,brief,country,categories,read_number)
                insert_simple1(id) ##新增ID
                if select_id(url,'complex')==None:
                    cid=insert_complex(title_complex,author_complex,times,int(time.time()),content_complex,froms,sort,url,img_url,brief,country,id,categories,read_number)
                    insert_complex1(cid)
            else:
                return False
        except Exception as e:
            print("errorrrrrrrrrrrrrrr:"+e)
            return False
    def news(): #咨讯
        sort="资讯"
        categories='5af58f86839f3369e4d607e7'
        page=1
        while True:
            url='http://www.jinniu.cn/prefix/info/medias?id=2&page=%d&maxTime=%d'%(page,time.time())
            req=requests.get(url).text
            req=json.loads(req)
            if len(req['data']['medias']['list'])==0:
                break
            for text in req['data']['medias']['list']:
                times=str(text['createdAt'])[:10]
                titleid=text['id']
                viewNum=text['viewNum']
                title=text['title']
                imageUrl=text['imageUrl']
                articleSummary=text['articleSummary']
                editor=text['editor']
                state=Jinniu.content(titleid,title,editor,times,sort,imageUrl,articleSummary,categories,viewNum)
                if state==False:
                    break
                print('===========================================================================')
            if state==False:
                break
                # print(titleid,viewNum,title,imageUrl,articleSummary,editor,times)
            page+=1
    def renwu(): #renwu
        sort="人物"
        categories='5af58f8d839f3369e4d607e8'
        page=1
        while True:
            url='http://www.jinniu.cn/prefix/info/medias?id=3&page=%d&maxTime=%d'%(page,time.time())
            req=requests.get(url).text
            req=json.loads(req)
            if len(req['data']['medias']['list'])==0:
                break
            for text in req['data']['medias']['list']:
                times=str(text['createdAt'])[:10]
                titleid=text['id']
                viewNum=text['viewNum']
                title=text['title']
                imageUrl=text['imageUrl']
                articleSummary=text['articleSummary']
                editor=text['editor']
                state=Jinniu.content(titleid,title,editor,times,sort,imageUrl,articleSummary,categories,viewNum)
                if state==False:
                    break
                print('===========================================================================')
            if state==False:
                break
                # print(titleid,viewNum,title,imageUrl,articleSummary,editor,times)
            page+=1
    def zhengce(): #renwu
        sort="政策"
        categories='5af58f92839f3369e4d607e9'
        page=1
        while True:
            url='http://www.jinniu.cn/prefix/info/medias?id=5&page=%d&maxTime=%d'%(page,time.time())
            print(url)
            req=requests.get(url).text
            req=json.loads(req)
            if len(req['data']['medias']['list'])==0:
                break
            for text in req['data']['medias']['list']:
                times=str(text['createdAt'])[:10]
                titleid=text['id']
                viewNum=text['viewNum']
                title=text['title']
                imageUrl=text['imageUrl']
                articleSummary=text['articleSummary']
                editor=text['editor']
                state=Jinniu.content(titleid,title,editor,times,sort,imageUrl,articleSummary,categories,viewNum)
                if state==False:
                    break
                print('===========================================================================')
            if state==False:
                break
                # print(titleid,viewNum,title,imageUrl,articleSummary,editor,times)
            page+=1
    def shendu(): #深度
        sort="深度"
        categories='5af58f97839f3369e4d607ea'
        page=1
        while True:
            url='http://www.jinniu.cn/prefix/info/medias?id=7&page=%d&maxTime=%d'%(page,time.time())
            print(url)
            req=requests.get(url).text
            req=json.loads(req)
            if len(req['data']['medias']['list'])==0:
                break
            for text in req['data']['medias']['list']:
                times=str(text['createdAt'])[:10]
                titleid=text['id']
                viewNum=text['viewNum']
                title=text['title']
                imageUrl=text['imageUrl']
                articleSummary=text['articleSummary']
                editor=text['editor']
                state=Jinniu.content(titleid,title,editor,times,sort,imageUrl,articleSummary,categories,viewNum)
                if state==False:
                    break
                print('===========================================================================')
            if state==False:
                break
                # print(titleid,viewNum,title,imageUrl,articleSummary,editor,times)
            page+=1
    def xiangmu(): #项目
        sort="项目"
        categories='5af58f92839f3369e4d607e9'
        page=70
        while True:
            url='http://www.jinniu.cn/prefix/info/medias?id=9&page=%d&maxTime=%d'%(page,time.time())
            print(url)
            req=requests.get(url).text
            req=json.loads(req)
            if len(req['data']['medias']['list'])==0:
                break
            for text in req['data']['medias']['list']:
                times=str(text['createdAt'])[:10]
                titleid=text['id']
                viewNum=text['viewNum']
                title=text['title']
                imageUrl=text['imageUrl']
                articleSummary=text['articleSummary']
                editor=text['editor']
                state=Jinniu.content(titleid,title,editor,times,sort,imageUrl,articleSummary,categories,viewNum)
                if state==False:
                    break
                print('===========================================================================')
            if state==False:
                break
                # print(titleid,viewNum,title,imageUrl,articleSummary,editor,times)
            page+=1
if __name__=='__main__':
    Jinniu.news()
    time.sleep(2)
    Jinniu.renwu()
    time.sleep(2)
    Jinniu.zhengce()
    time.sleep(2)
    Jinniu.shendu()
    time.sleep(2)
    Jinniu.xiangmu()
