#!usr/bin/env python
#encoding=utf-8
import jieba
from wordcloud import WordCloud
filename='bigdata.txt'
with open(filename) as f:
    mytext=f.read()
mytext =' '.join(jieba.cut(mytext))
#print (mytext)
worldcloud =WordCloud(font_path='simhei.ttf').generate(mytext)
#%pylab inline
import matplotlib.pyplot as plt
plt.imshow(worldcloud,interpolation='bilinear')
plt.axis('off')
plt.show()
