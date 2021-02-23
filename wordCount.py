# coding:utf-8
# author: uckendo.com
import io
import jieba

text = io.open("/Users/kendo/Desktop/all.txt", encoding='utf-8').read()
words = jieba.lcut(text)
counts = {}
for word in words:
    if len(word) == 1:
        continue
    else:
        counts[word] = counts.get(word,0)+1


items = list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
print (len(items))
for i in range(15):
    word,count = items[i]
    print (u"{0:<10}{1:>5}".format(word, count))