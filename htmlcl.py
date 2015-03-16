# coding:utf8
import HTMLParser
import hashlib
import re
import urllib

# 继承于Python自带的HTMLParser解析类
import urllib2


class get_img(HTMLParser.HTMLParser):
    def __init__(self, html, path):
        self.html = html
        self.path = path
        HTMLParser.HTMLParser.__init__(self)

    # 当标签开始的时候
    def handle_starttag(self, tag, attrs):
        # 如果标签是img标签
        if tag == 'img':
            for key, value in attrs:
                # 取<img>标签的src属性
                if key == "src":
                    # 哈希url，得到一会儿要保存的唯一的图片名
                    hash = hashlib.md5(value).hexdigest().upper()[0:16]
                    pattern = re.compile(r'\.[^\.]+$')
                    extname = pattern.search(value)
                    new_url = "OEBPS/image/" + hash + extname.group()
                    try:
                        i_headers = {
                            'Connection': 'Keep-Alive',
                            'Accept': 'text/html, application/xhtml+xml, */*',
                            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
                        req = urllib2.Request(value, headers=i_headers)
                        res = urllib2.urlopen(req)
                        f = open(self.path + new_url, "wb")
                        f.write(res.read())
                        # urllib.urlretrieve(value, self.path + new_url)
                    except Exception:
                        print Exception
                    print key, value, hash
                    # 替换HTML中的图片路径为本地图片路径
                    self.html[0] = self.html[0].replace(value, new_url.replace('OEBPS/',''))