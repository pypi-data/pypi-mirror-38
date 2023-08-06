#Wikicivi Crawler Client SDK
import os
import time
import datetime
import os,sys
import json
import re

def decode_event(event):
    #下面是一个带上阿里云网关全部系统参量的headers信息：
    """
    {"result":{
            "headers":{
                "CaRequestId":"8BDEAB48-9EAB-44AF-84D2-6E526A6C6993",
                "X-Ca-Api-Gateway":"8BDEAB48-9EAB-44AF-84D2-6E526A6C6993",
                "CaProxy":"AliCloudAPIGateway",
                "CaClientUa":"curl/7.61.0",
                "CaApiName":"echo",
                "CaHttpSchema":"HTTP",
                "X-Forwarded-For":"159.226.43.61",
                "CaRequestHandleTime":"2018-11-15T06:11:33Z",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "CaDomain":"api.hannm.com",
                "CaClientIp":"159.226.43.61",
                "CaAppId":"null"
            },
            "body":"",
            "pathParameters":{"echo_text":"phone"},
            "httpMethod":"GET",
            "path":"/echo/phone",
            "isBase64Encoded":false,
            "queryParameters":{}
        },
        "error":0,
        "reason":"success"
    }
    """
    try:
        event_json = json.loads(event)
        event_headers = event_json["headers"]
        req_headers = [
                "CaRequestId",
                "X-Ca-Api-Gateway",
                "CaProxy",
                "CaClientUa",
                "CaApiName",
                "CaHttpSchema",
                "X-Forwarded-For",
                "CaRequestHandleTime",
                "Content-Type",
                "CaDomain",
                "CaClientIp",
                "CaAppId"
        ]
        for req_header in req_headers:
            if req_header not in event_headers: raise Exception("缺少系统头参数:"+req_header)
        return True,event_json
    except Exception as err:
        return False,str(err)
   

def log(event_json,asmrt_json,**kwargs):
    mongo_uri   = "mongodb://root:hello2DB@dds-2zeabb0862781c64-pub.mongodb.rds.aliyuncs.com:3717";
    mongo_db    = "hannmdb";
    mongo_col   = "apilog" ;
    """
    当以函数计算作为API网关的后端服务时，API网关会把请求参数通过一个固定的Map结构传给函数计算的入参event，
    函数计算通过如下结构去获取需要的参数，然后进行处理，该结构如下：
    {
    "path":"api request path",
    "httpMethod":"request method name",
    "headers":{all headers,including system headers},
    "queryParameters":{query parameters},
    "pathParameters":{path parameters},
    "body":"string of request payload",
    "isBase64Encoded":"true|false, indicate if the body is Base64-encode"
    }
    需要特别说明的是：当isBase64Encoded=true时，
    表明API网关传给函数计算的body内容是经过Base64编码的，
    函数计算需要先对body内容进行Base64解码后再处理。
    反之，isBase64Encoded=false时，表明API网关没有对body内容进行Base64编码。
    下面就是一个典型的evt结构.base64编码的body里就是{'brief': 'what a fuck', 'name': 'test'}
    '{"result":{"headers":{"X-Ca-Api-Gateway":"C66FA93A-5283-4590-9A50-D6FFFFD47B0F",
    "X-Forwarded-For":"159.226.43.36","Content-Type":"application/octet-stream; charset=UTF-8"},
    "body":"eyJicmllZiI6ICJ3aGF0IGEgZnVjayIsICJuYW1lIjogInRlc3QifQ==","pathParameters":{},
    "httpMethod":"POST","path":"/site","isBase64Encoded":true,"queryParameters":{}},"error":1,"reason":"debug"}
    
    下面是一个带上阿里云网关全部系统参量的headers信息：
    {
    "result":{
        "headers":{
            "CaRequestId":"8BDEAB48-9EAB-44AF-84D2-6E526A6C6993",
            "X-Ca-Api-Gateway":"8BDEAB48-9EAB-44AF-84D2-6E526A6C6993",
            "CaProxy":"AliCloudAPIGateway",
            "CaClientUa":"curl/7.61.0",
            "CaApiName":"echo",
            "CaHttpSchema":"HTTP",
            "X-Forwarded-For":"159.226.43.61",
            "CaRequestHandleTime":"2018-11-15T06:11:33Z",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "CaDomain":"api.hannm.com",
            "CaClientIp":"159.226.43.61",
            "CaAppId":"null"
        },
        "body":"",
        "pathParameters":{"echo_text":"phone"},
        "httpMethod":"GET",
        "path":"/echo/phone",
        "isBase64Encoded":false,
        "queryParameters":{}},
        "error":0,"reason":"success"
    }
    """
    mongo_doc = {
        "event":event_json,
        "asmrt":asmrt_json,
        "incr":int(time.time()*1000000)
    }
    try:
        event_headers = event_json["headers"]
        for event_header in event_headers:
            mongo_doc[event_header] = event_headers[event_header]
        mongo_doc["url"]         = event_json["httpMethod"]+" "+event_headers["CaHttpSchema"]+"://"+event_headers["CaDomain"]+event_json["path"]
        mongo_client = MongoClient(mongo_uri)
        mongo_db     = mongo_client[mongo_dbname]
        mongo_col    = mongo_db[mongo_tablename]
        mongo_col.insert_one(site)
        return True
    except Exception as err:
        return False
