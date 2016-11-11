# coding:utf-8
import requests
import lxml
from Queue import Queue
from lxml import etree
from StringIO import StringIO
import re
import sys
import pandas as pd
import numpy as np


df = pd.read_csv(sys.argv[1])
print df.head()

df['price_num'] = df.price.map(lambda x: float(x.replace(u'万'.encode('utf-8'),'')))
print u'房屋总价'
print df.price_num.describe()

df['unitprice_num'] = df.unitprice.map(lambda x: float(re.search(r'\d+', x).group()))
print u'单价'
print df.unitprice_num.describe()

df['xiaoqu'] = df['info'].map(lambda x: x.split('|')[0])
df['fangxin'] = df['info'].map(lambda x: x.split('|')[1])
df['area'] = df['info'].map(lambda x: float(x.split('|')[2].replace('平米','')))
df['chaoxiang'] = df['info'].map(lambda x: x.split('|')[3])
df['zhuangxiu'] = df['info'].map(lambda x: x.split('|')[4])
#df['dianti'] = df['info'].map(lambda x: x.split('|')[5])

print df.xiaoqu.value_counts()[:30]
print df.chaoxiang.value_counts()
print df.area.describe()

def dist_ditie(x):
    #if type(x) is not str:
    #    raise Exception('TypeError: %s' % str(type(x)))
    s = re.search(r'距离.+?(\d+)米', str(x))
    if s is None:
        return np.nan
    else:
        return float(s.groups()[0])
df['ditie_juli'] = df['tag'].map(dist_ditie)
print df.ditie_juli.describe()


df['ceng'] = df.pos.map(lambda x: int(re.search(r'共(\d+)层', x).groups()[0]))
print df.ceng.describe()
df.to_csv(sys.argv[1] + '.processed.csv')
