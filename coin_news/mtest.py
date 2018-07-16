#coding=utf-8
from bson import ObjectId
from pymongo import *
import json
client = MongoClient("mongodb://pro:q5ll8Eedel7ZgSM7pe1u@dds-j6cb54ecada822241.mongodb.rds.aliyuncs.com:3717,dds-j6cb54ecada822242.mongodb.rds.aliyuncs.com:3717/giftcms?replicaSet=mgset-6151741")
# client = MongoClient("localhost", 27017)
db = client.giftcms
# content=db.posts_cn.find({"slug":"5b0b88aa151a766a10234f43"})
content=db.posts_cn.find({"slug":"5b0b8882151a766a10234f21"})
for document in content:
    print(document)