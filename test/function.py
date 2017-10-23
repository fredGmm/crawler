#!/usr/bin/env python3
# -*- coding: utf-8 -*-

values = abs(-100000000000000000)
#print(values)

#函数的参数

#位置参数
def add(a, b):
	return a + b

#默认参数
def picture(src, type = '.jpg'):
	return src + type
print(picture('cvvv'))
print(picture('asdfasg', type='.png'))

#可变参数

def add2(*nums):
	return nums

print(add2(1, 2, 2,2 , 2,34))

list = [2,3,4,5,6]
print(add2(*list))

def key(param, parma2, **kw):
	return print(kw)

print(key(1,2,num =435252515))

#限制关键词名字
def person(name, age, *, city, job):
    print(name, age, city, job)