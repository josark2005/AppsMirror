#!usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import ssl
import urllib3
import requests
from contextlib import closing


def main():
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
    # 获取下载页面
    download_page = 'https://github.com/jokin1999/SMMS_Uploader/releases/latest'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WallpaperBackuper/1.0.0'
    http = urllib3.PoolManager()
    try:
        print('Get: download_page')
        r = http.request(
            'get',
            download_page,
            headers={'user-agent': ua})
    except Exception:
        sys.exit('Failed to get download page.')
    data = r.data.decode('utf-8')
    match = re.search('/jokin1999.+gui\.exe', data)
    if (match is None):
        sys.exit('Failed to search download link')
    download_link = 'https://github.com' + match.group(0)
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
                with open('./public/' + os.path.basename(download_link), "wb") as file:
                    for data in res.iter_content(chunk_size=chunk_size):
                        downloaded_size += chunk_size
                        # print('Progress: ' + str(round(downloaded_size/content_size*100, 2)) + r'%', end='\r')
                        file.write(data)
            except Exception:
                sys.exit('Failed to write file.')
    except Exception as e:
        sys.exit('Failed to download file.\n' + str(e))
    file_gui = '/gui.exe'
    # 上传CDN
    # post_url = 'https://transfer.sh/'
    # file = './gui.exe'
    # print('Reading file.')
    # try:
    #     with open(file, 'rb') as f:
    #         fileData = f.read()
    # except Exception:
    #     sys.exit('Failed to read file.')
    # file = {file: fileData}
    # print('Posting file.')
    # r = requests.post(post_url, headers={'Max-Days': '2'}, files=file)
    # file_gui = r.text
    # print(file_gui)
    # 修改HTML内容
    # 读取模板
    try:
        with open('./assets/index.html', 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception:
        sys.exit('Failed to read asset file.')
    html = html.replace('__gui.exe__', file_gui)
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


if __name__ == '__main__':
    main()
