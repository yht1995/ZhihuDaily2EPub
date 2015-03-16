# -*- coding: UTF-8 -*-
import urllib2
import json
import re

class ZhihuDaily:
    def DownloadLatest(self,path):
        daily = self.Fetchurl_json('http://news.at.zhihu.com/api/3/news/latest')
        for news in daily.get('stories'):
            print news['title']
            print news['id']
            url = 'http://news.at.zhihu.com/api/3/news/' + '%s' % news['id']
            data = self.Fetchurl_json(url).get('body')

            pattern = re.compile(r'class=".*?" ?')
            data = re.sub(pattern, '', data)
            pattern = re.compile(r'<a[^>]*>([\s\S]*?)</a>')
            data = re.sub(pattern, r'\1', data)
            filePath = path + '%s' %daily.get('date') + '/' + '%s' % news['id'] + '.html'
            htmlFile = open(filePath, 'w')
            htmlFile.writelines('<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
                                '<div class="main-wrap content-wrap"></head><body>')
            htmlFile.writelines("\n" + '<div><h1>' + '%s' % news['title'].encode('utf-8') + '</h1></div>' + "\n")
            htmlFile.writelines(data.encode('utf-8'))
            htmlFile.writelines('</body></html>')
            htmlFile.close()

    def GetLatestDate(self):
        daily = self.Fetchurl_json('http://news.at.zhihu.com/api/3/news/latest')
        return daily.get('date')

    def Fetchurl_json(self,url):
        req = urllib2.Request(url, headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        })
        response = urllib2.urlopen(req)
        data = response.read()
        data_json = json.loads(data)
        return data_json