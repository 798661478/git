#!usr/bin/env python
#encoding=utf-8
from urllib import request
from bs4 import BeautifulSoup as bs
import re
import jieba
import pandas as pd
import numpy
import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
matplotlib.rcParams['figure.figsize']=(10.0,5.0)
from wordcloud import WordCloud
requrl ='https://movie.douban.com/subject/26363254/comments?start=0&limit=20'
    #'https://movie.douban.com/subject/'+nowplaying_list[0]['id']+'/comments'+'?'+'start=0'+'&limit=20'
resp=request.urlopen(requrl)
html_data=resp.read().decode('utf-8')
soup=bs(html_data,'html.parser')
comment_div_lists=soup.find_all('div',class_='comment')
eachCommentList=[]
for item in comment_div_lists:
    if item.find_all('p')[0].string is not None:
        eachCommentList.append(item.find_all('p')[0].string)
#print(eachCommentList)
comments=''
for k in range(len(eachCommentList)):
    comments=comments+(str(eachCommentList[k])).strip()
#print(commets)
pattern = re.compile(r'[\u4e00-\u9fa5]+')
filterdata = re.findall(pattern, comments)
cleaned_comments = ''.join(filterdata)
#print(cleaned_comments)
segment=jieba.lcut(cleaned_comments)
words_df=pd.DataFrame({'segment':segment})
stopwords=pd.read_csv('stopwords.txt',index_col=False,quoting=3,sep='\t',names=['stopword'],encoding='gb2312')
words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
#print(words_df.head())
words_stat=words_df.groupby(by=['segment'])['segment'].agg({'计数':numpy.size})
words_stat=words_stat.reset_index().sort_values(by=['计数'],ascending=False)
#print(words_stat.head())
wordcloud=WordCloud(font_path='simhei.ttf',background_color='white',max_font_size=80)
word_frequence={x[0]:x[1] for x in words_stat.head(1000).values}
word_frequence_list=[]
for key in word_frequence:
    temp=(key,word_frequence[key])
    word_frequence_list.append(temp)
wordcloud=wordcloud.fit_words(dict(word_frequence_list))
plt.imshow(wordcloud)
plt.show()