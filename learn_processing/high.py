#!/usr/bin/env python3
# -*- coding: utf-8 -*-

L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']

#切片
print(L[0:2])
print(L[:3])

#迭代
d = {'name':'yxrs', 'price':'13.23',}

# 迭代值
for key in d.values():
	print(key)

#迭代键值对
for k, v in d.items():
	print(k, v)

#迭代 数字索引
for i, value in enumerate(['A', 'B', 'C']):
	print(i, value)

print(range(0,10)[2])

#生成器
generator = (x*x for x in range(0, 10))
print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))