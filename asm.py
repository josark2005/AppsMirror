#!usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import ssl
import urllib3
import requests
from contextlib import closing


# 从GitHub获取下载链接
def getDownloadLink(author, project, filename, retry=0):
    # 获取下载页面
    download_page = 'https://github.com/{}/{}/releases/latest'.format(author, project)
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WallpaperBackuper/1.0.0'
    http = urllib3.PoolManager()
    try:
        print('Get: %s/%s' % (author, project))
        r = http.request(
            'get',
            download_page,
            headers={'user-agent': ua})
    except Exception:
        if (retry <= 3):
            print('Failed to get download page, but retry(%d)' % retry+1)
            getDownloadLink(author, project, filename, retry+1)
        else:
            sys.exit('Failed to get download page.')
    data = r.data.decode('utf-8')
    pattern = '/' + author + '.+' + filename.replace('.', '\\.')
    print('search: ' + pattern)
    match = re.search(pattern, data)
    if (match is None):
        sys.exit('Failed to search download link')
    download_link = 'https://github.com' + match.group(0)
    return download_link


def download_file(download_link, target='./public/', retry=0):
    filename = os.path.basename(download_link)
    print('Downloading: ' + filename)
    try:
        print('Get: file @ ' + download_link)
        # headers = {'user-agent': ua}
        with closing(requests.get(download_link, stream=True, verify=False)) as res:
            downloaded_size = 0
            chunk_size = 4096
            # print(res.headers)
            content_size = int(res.headers['Content-Length'])
            print('File size: ' + str(content_size))
            try:
                with open(target + filename, "wb") as file:
                    for data in res.iter_content(chunk_size=chunk_size):
                        downloaded_size += chunk_size
                        print('Progress: ' + str(round(downloaded_size/content_size*100, 2)) + r'%', end='\r')
                        file.write(data)
            except Exception:
                sys.exit('Failed to write file.')
    except Exception as e:
        if (retry <= 3):
            print('Failed to download file, but retry(%d)' % retry+1)
            download_file(download_link, target, retry+1)
        else:
            sys.exit('Failed to download file.\n' + str(e))
    return filename


def allinone(author, project, filename, target='./public/'):
    global filelist
    download_link = getDownloadLink(author, project, filename)
    filename = download_file(download_link, target)
    tpl = '<a href="/__href__" target="_blank">__project__</a><img src="https://img.shields.io/github/release/__author__/__project__.svg?style=flat-square" alt="badge">'
    filelist.append(tpl.replace('__href__', filename).replace('__author__', author).replace('__project__', project))


def main():
    # 下载列表
    download_list = [
        ('jokin1999', 'SMMS_Uploader', 'gui.exe'),
        ('jokin1999', 'PacDownloader', 'updatepac.exe'),
    ]
    # 检查目录情况
    if not (os.path.isdir('./public')):
        try:
            os.mkdir('./public')
        except Exception:
            sys.exit('Failed to make public directory.')
    # 关闭证书验证
    ssl._create_default_https_context = ssl._create_unverified_context
    # 取消关闭验证安全提醒
    urllib3.disable_warnings()
    for fileinfo in download_list:
        if (3 in fileinfo):
            allinone(fileinfo[0], fileinfo[1], fileinfo[2], fileinfo[3])
        else:
            allinone(fileinfo[0], fileinfo[1], fileinfo[2])
    # 读取模板
    try:
        with open('./assets/index.html', 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception:
        sys.exit('Failed to read asset file.')
    html = html.replace('__list__', '<br />'.join(filelist))
    time_link = 'http://nodetime.gearhostpreview.com/'
    try:
        time_prc = requests.get(time_link, verify=False)
        time_prc = time_prc.text
    except Exception:
        sys.exit('Failed to get time.')
    html = html.replace('__time__', time_prc)
    # 写入模板
    try:
        with open('./public/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception:
        sys.exit('Failed to write index.html.')
    # Wechat
    try:
        with open('./public/tencent18116010769473363677.txt', 'w', encoding='utf-8') as f:
            f.write('16389480770053209008')
    except Exception:
        sys.exit('Failed to write tencent18116010769473363677.txt.')


if __name__ == '__main__':
    # 定义全局变量
    filelist = []
    main()
