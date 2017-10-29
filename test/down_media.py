#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import sys


def PrintMessage(msg):
    print('>>', sys.stderr, '\r',)
    print('>>', sys.stderr, msg,)


def DownloadFile(url, tofile, CallBackFunction=PrintMessage):
    f = urllib.request.urlopen(url)
    outf = open(tofile, 'wb')
    c = 0
    CallBackFunction('Download %s to %s' % (url, tofile))
    while True:
        s = f.read(1024 * 32)
        if len(s) == 0:
            break
        outf.write(s)
        c += len(s)
        CallBackFunction('Download %d' % (c/(1024*1024)))
    return c

url = 'https://v8.wuso.tv/wp-content/uploads/2017/03/iii817.mp4'
DownloadFile(url, 'xiaochuan.mp4', )
exit(0)


url = 'http://pic.ibaotu.com/00/35/14/27E888piCBfA.mp4'
url = 'https://gss1.bdstatic.com/9vo3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike80%2C5%2C5%2C80%2C26/sign=4c9327e19d0a304e462fa8a8b0a1cce3/4d086e061d950a7bb3841d2100d162d9f3d3c9a6.jpg'
f = urllib.request.urlopen(url)
with open("demo2.jpg", "wb") as code:
  code.write(f.read())

r = requests.get(url_file, stream=True)
f = open("file_path", "wb")
for chunk in r.iter_content(chunk_size=512):
    if chunk:
        f.write(chunk)