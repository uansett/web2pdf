#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: set fileencoding=ut8 :
# author: Stian Johansen,  otherwise noted
import config
import urllib
import xml.dom.minidom
import string
from BeautifulSoup import BeautifulSoup

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

# http://stackoverflow.com/questions/2097921/easy-way-to-get-data-between-tags-of-xml-or-html-files-in-python
def getHeadlineFromArticle(urlObject, headlineTag, headlineAttr):
    soup = BeautifulSoup(urlObject)
    if headlineAttr  !=  "":
        print soup.findAll(headlineTag, headlineAttr)[0].contents[0]
    else:
        print soup.findAll(headlineTag)[0].contents[0]
    
    return 0

def getArticle(urlObject, articleTag, articleAttr):
    soup = BeautifulSoup(urlObject)
    if articleAttr  !=  "":
        print soup.findAll(articleTag,articleAttr)[0].contents[0]
    else:
        print soup.findAll(articleTag)[0].contents[0]
    return 0


if __name__  ==  "__main__":
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
        getHeadlineFromArticle(thisURL, headlineTag, headlineAttr)
        getArticle(thisURL, articleTag, articleAttr)

    dom.unlink()



