#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyPDF2 import PdfFileReader, PdfFileWriter

readFile = 'src/test.pdf'
writeFile = 'write.pdf'
# erw获取
pdfReader = PdfFileReader(open(readFile, 'rb'))
# 获取 PDF 的页数
pageCount = pdfReader.getNumPages()
print(pageCount)
# 返回一个 PageObject
page = pdfReader.getPage(0)
# 获取一个 PdfFileWriter 对象
pdfWriter = PdfFileWriter()
# 将一个 PageObject 加入到 PdfFileWriter 中
pdfWriter.addPage(page)

# 输出到文件中
pdfWriter.write(open(writeFile, 'wb'))