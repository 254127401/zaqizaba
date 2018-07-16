from mongo import *
import requests,json,time,random,re
from lxml import etree
class Btcn():
    def shijian(times):
        times=times[:times.find(' (')].replace('.','/')+' %d:%d:%d'%(random.randint(0,23),random.randint(0,59),random.randint(0,59))
        timeArray = time.strptime(times, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    def getimg(content):
        l=content.find('url(')
        f=content.find(');')
        return content[l+4:f]
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def content(url,title,author,times,sort,img_url,categories):
        print('文章：%s'%url)
        req=requests.get(url,verify=False).text
        content=Btcn.qwbzj(req,'<div class="article-details-body">','<div class="article-details-tag">').strip()
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        brief=etree.HTML(content)
        brief=brief.xpath('/html/body/p')
        read_number=0
        if len(brief)==1:
            brief=brief[0].text
        elif len(brief)==0:
            brief=''
        else:
            brief=brief[1].text

        country='JP'            ##语种
        froms='btcnews.jp'      ##来源网址
        categories=categories  ##新闻栏目
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
        page=1
        img_xpath='//*[@id="js-wrapper"]/div/div/article/div/ul/li/article/div[1]'
        label_xpath='//*[@id="js-wrapper"]/div/div/article/div/ul/li/article/div[2]/h4'
        author_xpath='//*[@id="js-wrapper"]/div/div/article/div/ul/li/article/div[2]/div/a'
        link_xpath='//*[@id="js-wrapper"]/div/div/article/div/ul/li/article/a'
        time_xpath='//*[@id="js-wrapper"]/div/div/article/div/ul/li/article/div[2]/div/div'
        while True:
            url='https://btcnews.jp/category/news/page/%d/'%page
            print('当前目录页：%s'%url)
            req=requests.get(url).text
            req=etree.HTML(req)
            img=req.xpath(img_xpath)
            label=req.xpath(label_xpath)
            author=req.xpath(author_xpath)
            link=req.xpath(link_xpath)
            time=req.xpath(time_xpath)
            if len(link) <= 1:             ###没有文章则退出
                break
            sort='ニュース NE'
            for num in range(len(link)):
                if time[num].text!='Promotion':
                    try:
                        state=Btcn.content(link[num].get('href'),label[num].text,author[num].text,Btcn.shijian(time[num].text),sort,Btcn.getimg(img[num].get('style')),categories)
                        if state == False:
                            break
                    except Exception as e:
                        print(e)
            if state ==False:
                break
            page+=1

if __name__=='__main__':
    '''  https://btcnews.jp/   '''
    Btcn.news()
