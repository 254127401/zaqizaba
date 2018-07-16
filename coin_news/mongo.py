# coding=utf-8
from bson import ObjectId
from pymongo import *
import json,re

client = MongoClient("mongodb://")

db = client.giftcms
# collection = db.test
collection = db.posts_cn
collection_complex = db.posts_tw
jp_collection = db.posts_jp
kr_collection = db.posts_kr
us_collection = db.posts_us


# collection = db.posts_en
# 中文 插入#
def insert_simple(title, author, time, create_time, content, froms, sort, url, img_url, brief, country, categories,
                  readnum):
    contents = {
        "brief": str(brief),
        "extended": str(content)
    }
    imgs = {
        "url": str(img_url),
    }
    origins = {
        'country': str(country),
        "from": str(froms),
        "cate": str(sort),
        "url": str(url)
    }
    mydict = {
        'title': str(title),
        'state': "published",
        '__v': 1,
        'author': str(author),
        'content': contents,
        'image': imgs,
        'categories': [ObjectId(str(categories))],
        'origin': origins,
        "publishedDate": int(time),
        "createTime": create_time,
        'readnum': readnum
    }
    print(mydict)
    content = collection.insert(mydict)
    return content


# 中文简体，确认ID  #
def insert_simple1(test):
    content = collection.update_one({"_id": ObjectId(test)}, {"$set": {"slug": str(test)}})
    print(content)
    return content


########################################################################################################################
#  中文繁体翻译 ，多一个参数。    #
def insert_complex(title, author, time, create_time, content, froms, sort, url, img_url, brief, country, id, categories,
                   readnum):
    translate = {
        'id': ObjectId(str(id)),
        "lang": "CN"
    }
    contents = {
        "brief": str(brief),
        "extended": str(content)
    }
    imgs = {
        "url": str(img_url),
    }
    origins = {
        'country': country,
        "from": str(froms),
        "cate": str(sort),
        "url": str(url)
    }
    mydict = {
        'title': str(title),
        'state': "published",
        '__v': 1,
        'author': str(author),
        'content': contents,
        'image': imgs,
        'categories': [ObjectId(str(categories))],  ##分类ID
        "translate": translate,  ## 翻译ID  从哪篇文章翻译过来的。
        'origin': origins,
        "publishedDate": time,
        "createTime": create_time,
        'readnum': readnum
    }
    content = collection_complex.insert(mydict)
    return content


#  中文繁体 确认#
def insert_complex1(test):
    content = collection_complex.update_one({"_id": ObjectId(test)}, {"$set": {"slug": str(test)}})
    print(content)
    return content


########################################################################################################################
# 查询是否存在文章 #
def select_id(url, lable):  ##第一个是查询url  第二个是查询的表
    if lable == 'CN':
        content = collection.find({'origin.url': re.compile(url)})
        for document in content:
            return document['origin'].get('url')  ##None
    elif lable == 'complex':
        content = collection_complex.find({'origin.url': re.compile(url)})
        for document in content:
            return document['origin'].get('url')  ##None
    elif lable == 'JP':
        content = jp_collection.find({'origin.url': url})
        for document in content:
            return document['origin'].get('url')  ##None
    elif lable == 'KR':
        content = kr_collection.find({'origin.url': url})
        for document in content:
            return document['origin'].get('url')  ##None
    elif lable == 'US':
        content = us_collection.find({'origin.url': url})
        for document in content:
            return document['origin'].get('url')  ##None


########################################################################################################################

#  日本  插入 #
def jp_insert_simple(title, author, time, create_time, content, froms, sort, url, img_url, brief, country, categories,
                     readnum):
    contents = {
        "brief": str(brief),
        "extended": str(content)
    }
    imgs = {
        "url": str(img_url),
    }
    origins = {
        'country': str(country),
        "from": str(froms),
        "cate": str(sort),
        "url": str(url)
    }
    mydict = {
        'title': str(title),
        'state': "published",
        '__v': 1,
        'author': str(author),
        'content': contents,
        'image': imgs,
        'categories': [ObjectId(str(categories))],
        'origin': origins,
        "publishedDate": time,
        "createTime": create_time,
        'readnum': readnum
    }
    content = jp_collection.insert(mydict)
    return content


# 日本 第二次  确认#
def jp_insert_simple1(test):
    content = jp_collection.update_one({"_id": ObjectId(test)}, {"$set": {"slug": str(test)}})
    print(content)
    return content


########################################################################################################################
#  韩国 第一次插入#
def kr_insert_simple(title, author, time, create_time, content, froms, sort, url, img_url, brief, country, categories,
                     readnum):
    contents = {
        "brief": str(brief),
        "extended": str(content)
    }
    imgs = {
        "url": str(img_url),
    }
    origins = {
        'country': str(country),
        "from": str(froms),
        "cate": str(sort),
        "url": str(url)
    }
    mydict = {
        'title': str(title),
        'state': "published",
        '__v': 1,
        'author': str(author),
        'content': contents,
        'image': imgs,
        'categories': [ObjectId(str(categories))],
        'origin': origins,
        "publishedDate": time,
        "createTime": create_time,
        'readnum': readnum
    }
    content = kr_collection.insert(mydict)
    return content


#  韩国ID 确认#
def kr_insert_simple1(test):
    content = kr_collection.update_one({"_id": ObjectId(test)}, {"$set": {"slug": str(test)}})
    print(content)
    return content


########################################################################################################################


##############################英文插入#################################################################################

def us_insert_simple(title, author, time, create_time, content, froms, sort, url, img_url, brief, country, categories,
                     readnum):
    contents = {
        "brief": str(brief),
        "extended": str(content)
    }
    imgs = {
        "url": str(img_url),
    }
    origins = {
        'country': str(country),
        "from": str(froms),
        "cate": str(sort),
        "url": str(url)
    }
    mydict = {
        'title': str(title),
        'state': "published",
        '__v': 1,
        'author': str(author),
        'content': contents,
        'image': imgs,
        'categories': [ObjectId(str(categories))],
        'origin': origins,
        "publishedDate": time,
        "createTime": create_time,
        'readnum': readnum
    }
    content = us_collection.insert(mydict)
    return content


#  US  ID 确认#
def us_insert_simple1(test):
    content = us_collection.update_one({"_id": ObjectId(test)}, {"$set": {"slug": str(test)}})
    print(content)
    return content


#######################################################################################################


if __name__ == '__main__':
    pass