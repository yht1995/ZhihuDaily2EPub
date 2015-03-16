# coding:utf8
import os
import shutil
import htmlcl
import zipFile
import re


class html2epub:
    def __init__(self, Path, Topath,Name):
        # 得到两个路径
        self.path = Path
        self.toPath = Topath
        self.name = Name

    def start(self):
        name_list = []
        title_list = []

        # 举出html存放路径下所有文件
        all_file = os.listdir(self.path)
        # 新建一个temp文件夹用来组织zip包里的内容
        # 如果已经存在则删除temp文件夹
        if os.path.exists('temp'):
            shutil.rmtree('temp')
        # 复制粘贴
        shutil.copytree('resource', 'temp')

        for each in all_file:
            print each
            if not each.endswith('.html'):
                continue
            # 组合文件名
            name = each.decode('utf-8')
            FilePath = self.path + name
            name_list.append(name.replace('.html', ''))

            # 第二步：处理HTML文件
            HtmlFile = open(FilePath, 'r')
            index = HtmlFile.read()
            HtmlFile.close()

            # 写一个解析类，负责下载html中的图片，并放入特定的路径下，并修改HTML文件中的图片路径
            pattern = re.compile(r'<h1>(.*?)</h1>')
            title_list.append(pattern.search(index).group(1))
            rep = [index]
            Parser = htmlcl.get_img(html=rep, path=r'temp/')
            Parser.feed(index)
            # 把改好的html写入文件
            HtmlFile = open(r'temp/OEBPS/' + name, 'w')
            HtmlFile.write(rep[0])
            HtmlFile.close()

        file = open(r'resource/OEBPS/content.opf', 'r')
        content = file.read()
        file.close()
        manifest = ''
        spine = ''
        for name in name_list:
            manifest += '<item id="' + name + '" href="' + name + '.html" media-type="application/xhtml+xml"/>' + "\n    "
            spine += '<itemref idref="' + name + '"/>' + "\n    "
        content = content.replace('[manifest]', manifest)
        content = content.replace('[spine]', spine)
        content = content.replace('<dc:title>', '<dc:title>'+self.name)
        file = open(r'temp/OEBPS/content.opf', 'w')
        file.write(content)
        file.close()

        file = open(r'resource/OEBPS/toc.ncx', 'r')
        content = file.read()
        file.close()
        navMap = ''
        for index in range(0, len(name_list) - 1):
            navMap += '<navPoint id="navpoint-' + '%d' % (index + 2) + '" playOrder="' + '%d' % (index + 2) + '">' \
                      + '<navLabel><text>' + title_list[index] + '</text></navLabel><content src="' \
                      + name_list[index] + '.html"/></navPoint>' + "\n"
        content = content.replace('[navPoint]', navMap)
        file = open(r'temp/OEBPS/toc.ncx', 'w')
        file.write(content)
        file.close()

        # 第三步：zip压缩修改好的文件，命名为.epub后缀
        zipFile.zip_dir(r'temp', self.toPath + self.name + '.epub')

        # 删除临时的文件夹
        shutil.rmtree('temp')
        print u'所有已完成'