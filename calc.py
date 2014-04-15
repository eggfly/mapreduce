#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import re
def u2g(u):
    return u.decode('utf8').encode('gb18030')
def g2u(g):
	return g.decode('gb18030').encode('utf8')
filename = u2g('北分.csv')
filepath = os.path.join(os.path.dirname(__file__), filename)
out_filepath = os.path.join(os.path.dirname(__file__), "output_" + filename)
f = open(filepath, 'rb')
of = open(out_filepath, 'wb')

shou_re = re.compile(r'.*收(.+?)(标书服务费|项目服务费|标书款),0,(\d+),.*')
zhuan_re = re.compile(r'.*转(.+?)(标书服务费|项目服务费|标书款),(\d+),.*')
company_dict = {}
def ensure_key(company_dict, new_key):
    exist = False
    key_contains_old = True
    old_key = ""
    for key in company_dict.iterkeys():
        if key in new_key:
            exist = True
            key_contains_old = True
            old_key = key
            break
        elif new_key in key:
            exist = True
            key_contains_old = False
            old_key = key
            break
        # else continue
    result = {}
    if not exist:
        company_dict[new_key] = {'in': [], 'out': [], 'sum': 0.0}
        result = company_dict[new_key]
    else:
        if not key_contains_old:
            # new key is shorter so it's more useful
            company_dict[new_key] = company_dict[old_key]
            del company_dict[old_key]
            result = company_dict[new_key]
        else:
            result = company_dict[old_key]
    return result
for line in f.readlines():
    line = g2u(line)
    shou_match = shou_re.match(line)
    zhuan_match = zhuan_re.match(line)
    if shou_match:
        company_key = shou_match.groups()[0]
        value = float(shou_match.groups()[2])
        v = ensure_key(company_dict, company_key)
        v['in'].append(line)
        v['sum'] += value
    elif zhuan_match:
        company_key = zhuan_match.groups()[0]
        value = float(zhuan_match.groups()[2])
        v = ensure_key(company_dict, company_key)
        v['in'].append(line)
        v['sum'] -= value
f.close()
for k, v in company_dict.iteritems():
    if v['sum'] != 0:
        for i in v['in']:
            of.write(u2g(i))
        for o in v['out']:
            of.write(u2g(o))
of.close()
