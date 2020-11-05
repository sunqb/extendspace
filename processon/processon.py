#!/usr/bin/env python
# -*- coding: utf-8 -*-

' 文件下载 '

__author__ = 'sunqb'

import sys
import urllib
import urllib2
import logging as log
import json
import threading

# 编码
reload(sys)
sys.setdefaultencoding('utf-8')

# 日志配置
log.basicConfig()
logger = log.getLogger()
logger.setLevel(log.DEBUG)

# cookie 集合，请替换。
cookies = []
cookies.append(
    '_ga=GA1.2xxxxx')
cookies.append(
    '_ga=GA1.2xxxxx')
cookies.append(
    '_ga=GA1.2xxxxx')
cookies.append(
    '_ga=GA1.2xxxxx')
cookies.append(
    '_ga=GA1.2xxxxx')

# copyUrl
copyUrl = 'https://www.processon.com/folder/copy'
# startUrl
startUrl = 'https://www.processon.com/view/dolike'
# deleteUrl
deleteUrl = 'https://www.processon.com/folder/to_trash'
# flushUrl
flushUrl = 'https://www.processon.com/folder/remove_from_trash'

# 扩展多少个
extendSize = 1000

# 发送一个请求并返回字典
def sendHttp(url,values, cookie):
    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        req.add_header('cookie', cookie)
        res = urllib2.urlopen(req)
        resMap = json.load(res)
        return resMap
    except Exception as e:
        logger.error(e)
        return e


class Processon:
    def __init__(self):
        pass

    # 清空回收站file
    def flushFile(self):
        try:
            values = {'fileType': 'all'}
            resMap = sendHttp(flushUrl, values, cookies[0])
            if resMap.get('result') == 'success':
                return 1
            else:
                return 0
        except Exception as e:
            logger.error(e)
            return e

    # 删除file
    def deleteFile(self, fileId):
        try:
            values = {'fileType': 'chart', 'fileId': fileId, 'resource': ''}
            resMap = sendHttp(deleteUrl, values, cookies[0])
            if resMap.get('result') == 'success':
                return 1
            else:
                return 0
        except Exception as e:
            logger.error(e)
            return e

    # 复制返回新的fileId
    def copyFile(self, fileId):
        try:
            values = {'fileType': 'chart', 'fileId': fileId, 'target': 'root', 'teamId': '', 'orgId': ''}
            resMap = sendHttp(copyUrl, values, cookies[0])
            if resMap.get('result') == 'success':
                return resMap.get('chart').get('chartId')
            else:
                return 'error'
        except Exception as e:
            logger.error(e)
            return e

    # 点赞
    def starFile(self, fileId):
        try:
            values = {'chartId': fileId}
            for cookie in cookies:
                resMap = sendHttp(startUrl, values, cookie)
                if resMap.get('count') >= 5:
                    print 'star success:'+fileId
                    return 1
        except Exception as e:
            logger.error(e)
            return e

    # 开始
    def start(self, fileId):
        if fileId == '':
            return 'error...'
        result = self.starFile(fileId)
        newFileId = ''
        if result == 1:
            while True:
                newFileId = self.copyFile(fileId)
                if newFileId != 'error':
                    break
            print 'newFileId:'+newFileId
            self.deleteFile(fileId)
            self.flushFile()
        if extendSize < 1:
            return "over..."
        else:
            return self.start(newFileId)

def run(fileId):
    processon = Processon()
    processon.start(fileId)

if __name__ == '__main__':
    # 请替换文件id。通常只需要3个就够了。我用3个文件，跑了400个没有问题。
    t1 = threading.Thread(target=run, args=('文件id1',))
    t1.start()
    t2 = threading.Thread(target=run, args=('文件id2',))
    t2.start()
    t3 = threading.Thread(target=run, args=('文件id3',))
    t3.start()
