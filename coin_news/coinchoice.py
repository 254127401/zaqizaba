import requests,json,time,re
from lxml import etree
from mongo import *
class Coin():
    def qwbzj(req,x,y):
        a=req.find(x)
        b=req.find(y,int(a+1))
        return req[a+len(x):b]
    def content(url,title,times,sort,img_url,brief,categories):
        print('文章：%s'%url)
        author_xpath='//*[@id="post-9861"]/div[1]/header/div/div[1]/a'
        read_xpath='//*[@class="td-post-views"]/span'
        req=requests.get(url).text
        author_txt=etree.HTML(req)
        author_txt=author_txt.xpath('//*[@class="td-post-author-name"]/a')
        author=author_txt[0].text
        read=etree.HTML(req)
        read=read.xpath(read_xpath)
        content=Coin.qwbzj(req,'<div class="td-post-content">','<div class="td-post-source-tags">').replace('src="/wp-content','src="https://coinchoice.net/wp-content/').replace('\n','').replace('\r','').replace('\t','')
        cc=re.findall(r'href=\'[^\s]*\'',content)
        dd=cc+re.findall(r'href="[^\s]*"',content)
        print(dd)
        for link in dd:
            content=content.replace(link,'')
        country = 'JP'
        froms='coinchoice.net'
        read_number=read[0].text
        try:
            if select_id(url,country) ==None:
                id = jp_insert_simple(title,author,int(times),int(time.time()),content,froms,sort,url,img_url,brief,country,categories,read_number)
                jp_insert_simple1(id)
            else:
                return False
        except Exception as e:
            return False
        
    def shijian(date):
        st=time.strptime(date.replace('年','-').replace('月','-').replace('日',''),'%Y-%m-%d')
        return int(time.mktime(st))
    def news():
        categories='5af58f86839f3369e4d607e7'
        page=1
        title_xpath='//*[@id="td-outer-wrap"]/div[3]/div/div/div[1]/div[2]/div/div/h3/a'
        brief_xpath='//*[@id="td-outer-wrap"]/div[3]/div/div/div[1]/div[2]/div/div/div[2]'
        img_xpath='//*[@id="td-outer-wrap"]/div[3]/div/div/div[1]/div[2]/div/div[1]/a/img'
        time_xpath='//*[@class="td-post-date"]/time'
        while True:
            url='https://coinchoice.net/news/page/%d/'%page
            print('当前目录页：%s'%url)
            req=requests.get(url).text
            req=etree.HTML(req)
            title=req.xpath(title_xpath)
            brief=req.xpath(brief_xpath)
            img=req.xpath(img_xpath)
            time=req.xpath(time_xpath)
            if len(title)==0:
                break
            for x in range(len(title)):
                try:
                    urls,titles,times,sort,img_url,briefs=title[x].get('href'),title[x].get('title'),Coin.shijian(time[x].text),'仮想通貨ニュース',img[x].get('src'),brief[x].text
                    state=Coin.content(urls,titles,times,sort,img_url,briefs,categories)
                    if state ==False:
                        break
                except Exception as e:
                    print(e)
            if state==False:
                break
            page+=1
if __name__=='__main__':
    ''' https://coinchoice.net   '''
    Coin.news()

