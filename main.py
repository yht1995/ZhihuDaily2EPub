# coding:utf8
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
sys.getdefaultencoding()
from ZhihuDaily import ZhihuDaily
from html2epub import html2epub

def MakePath(path):
    import os
    path = Path2Std(path)
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def Path2Std(path):
    path = path.decode('utf-8')
    path = path.replace('\\', '/')
    if path.endswith('/'):
        pass
    else:
        path += '/'
    return path

if __name__ == '__main__':
    path = os.path.abspath('.')
    zhihu = ZhihuDaily()
    path = Path2Std(path)
    date = zhihu.GetLatestDate()
    rawPath = Path2Std(path + date)
    MakePath(rawPath)
    zhihu.DownloadLatest(path)
    epub = html2epub(rawPath, path, date)
    epub.start()
