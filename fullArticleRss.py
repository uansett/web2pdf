#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: set fileencoding=ut8 :
# author: Stian Johansen,  otherwise noted
import config
import urllib
import xml.dom.minidom
import string
import re
from BeautifulSoup import BeautifulSoup


'''You might want to edit this function,  depending on what you'd want for output'''
def convertImageTags(text):
    # Does NOT what I want,  it finds all occurences instead of replacing them in-line.
    #http://www.daniweb.com/software-development/python/threads/278313
    #x = re.compile('<img src="(.*?)".*/>', re.DOTALL).findall(text)
    #print x
    return text


def saveArticles(headlines, articles):
    for i in range(0, len(headlines)):
        print headlines[i]+"\n"+articles[i]+"\n"

def loadURL(source):
    try:
        url=urllib.urlopen(source)
        urlContents=url.read()
        url.close()
        return urlContents
    except:
        return none

# author getText: Børre Stenseth
def getText(nodelist):
    rc = ''
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            t=node.data.encode('UTF-8') # ISO-8859-1
            rc += t
    return rc

def removeHTMLTags(text):
    #http://love-python.blogspot.com/2008/07/strip-html-tags-using-python.html?showComment=1236583680000#c2934091903053895837
    x = re.compile(r'<[^<]*?/?>')
    return x.sub('', text)
    return text


# http://stackoverflow.com/questions/2097921/easy-way-to-get-data-between-tags-of-xml-or-html-files-in-python
def getHeadlineFromArticle(urlObject, headlineTag, headlineAttr):
    soup = BeautifulSoup(urlObject)
    if headlineAttr  !=  "":
        try:
            return str(soup.findAll(headlineTag, headlineAttr)[0].contents[0])
        except:
            return 1
    else:
        try:
            return str(soup.findAll(headlineTag)[0].contents[0])
        except:
            return 1
    

def getArticle(urlObject, articleTag, articleAttr):
    soup = BeautifulSoup(urlObject)
    if articleAttr  !=  "":
        try:
            return str(soup.findAll(articleTag,articleAttr)[0].contents[0])
        except:
            return 1
    else:
        try:
            return str(soup.findAll(articleTag)[0].contents[0])
        except:
            return 1


if __name__  ==  "__main__":

    allArticles = []
    allHeadlines = []
    feedContents = loadURL(config.rssSource)
    headlineTag = string.replace(config.headlineTag, ">", "")
    headlineTag = string.replace(headlineTag, "<", "")
    headlineAttr = config.headlineAttr
    articleTag = string.replace(config.articleTag, ">", "")
    articleTag = string.replace(articleTag, ">", "")
    articleAttr = config.articleAttr

    dom = xml.dom.minidom.parseString(feedContents)
    
    articles = dom.getElementsByTagName("item")
    for article in articles:
        thisURL = loadURL(getText(article.getElementsByTagName("link")[0].childNodes))
        headline = getHeadlineFromArticle(thisURL, headlineTag, headlineAttr)
        articleContent = getArticle(thisURL, articleTag, articleAttr)
        if headline == 1 or article == 1:
            print 'Error with source.'
        else:
            allArticles.append(removeHTMLTags(convertImageTags(articleContent)))
            allHeadlines.append(removeHTMLTags(headline))
    dom.unlink()
    saveArticles(allHeadlines,  allArticles)
    print 'Successfully saved articles' 



