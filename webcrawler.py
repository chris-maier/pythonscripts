#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Webcrawler for rating web pages

This module visits webpages recursively and is juggeling with the content.

Handling the content:
    * obtain all E-Mail addresses published on the webpage
    * count the words and sort them
    * use an matching algorithm to rate the page

Todo:
    * count the words on every page and store them in a list of tuples
    * find a matching algorithm and run it against the word list
"""

import requests
import bs4
import urlparse
from Queue import Queue
from timeit import default_timer as timer

INPUT_URL = 'http://www.duerrdental.com'
# INPUT_URL = 'http://www.bitshift-dynamics.de/'
# INPUT_URL = 'http://chris-maier.com'

class Crawler:
    """This class crawles the web page."""

    def __init__(self, url):
        """Ctor - Setup the basic variables."""
        self.URL = url.rstrip("//")
        self.BASE_URL = urlparse.urlparse(url).netloc
        self.BASE_SCHEME = urlparse.urlparse(url).scheme
        self.mail = set()
        self.httpVisited = set()
        self.httpExtList = set()

    def parse(self):
        """This function does the heavy lifting.

        Iterates over the `urlList`, check if link was already processed and process it

        Args:
            urllist (:obj:`list` of :obj:`str`): List of URL's to process
        """
        inQueue = set()

        # init Queue
        q = Queue()
        q.put(self.URL)

        while not q.empty():
            link = q.get()
            print "- " + link

            self.httpVisited.add(link)

            dom = self.getHtmlDom(link)
            allUrls = self.getUrlList(dom)
            uniqueUrls = self.getIntUrl(allUrls) - self.httpVisited

            map(q.put, uniqueUrls - inQueue)
            inQueue.update(uniqueUrls)

            print "Queue: " + str(q.qsize())
            print "Visited: " + str(len(self.httpVisited))
            # print "Progress: " +
            # TODO here we are

    def getHtmlDom(self, url):
        """Send HTML request and process the received HTML DOM.

        TODO:
            Needs speed up
        Args:
            url (:obj:`str`): string of the URL
        """
        res = requests.get(url)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('Execption: %s' % (exc))

            # for link in soup.findAll('a', href=True, text='TEXT'):
        return bs4.BeautifulSoup(res.text, "lxml")


    def getUrlList(self, dom):
        """Obtain every 'href' HTML tag from the HTML DOM

        Args:
            dom (:obj:`bs4.BeautifulSoup`): HTML DOM
        """
        l = set()

        # retrieve all <a> tags with a valid href
        for tag in dom.find_all('a', href=True):
            a = tag.get('href')

            l.add(urlparse.urlparse(a))
        return l

    def getIntUrl(self, schemeList):
        """Extract every URL which belongs to the same base domain

        Args:
            dom (:obj:`bs4.BeautifulSoup`): HTML DOM
        """
        l = set()
        for scheme in schemeList:
            if (scheme.netloc == '' and scheme.scheme == ''):
                # prepend the BASE_URL
                link = self.BASE_SCHEME + '://' + self.BASE_URL + '/' + urlparse.urlunparse(scheme)
            elif (scheme.netloc == self.BASE_URL):
                link = urlparse.urlunparse(scheme)
            else:
                # print scheme
                # import pdb; pdb.set_trace()
                continue

            link = link.rstrip("//")
            l.add(link)
        return l

    def getExtUrl(self, schemeList):
        l = set()
        for scheme in schemeList:
            if scheme.netloc != self.BASE_URL and (scheme.scheme == 'http' or scheme.scheme == 'https'):
                l.add(urlparse.urlunparse(scheme))
        return l

    def getEmail(self, schemeList):
        l = set()
        for scheme in schemeList:
            if scheme.scheme == 'mailto':
                l.add(urlparse.urlunparse(scheme))
                # self.mail.add(scheme.path)
        return l

    def printEmails(self):
        print "Mail Addresses:"
        self.mail = sorted(self.mail)
        for h in self.mail:
            print h
        print ""

    def printVisitedLinks(self):
        print "Visited HTTP Links:"
        self.httpVisited = sorted(self.httpVisited)
        for h in self.httpVisited:
            print h
        print ""

    def printExtLinks(self):
        print "External HTTP Links:"
        self.httpExtList = sorted(self.httpExtList)
        for h in self.httpExtList:
            print h
        print ""


def main():
    p = Crawler(INPUT_URL)
    p.parse()

    # p.printVisitedLinks()
    # p.printExtLinks()
    # p.printEmails()

    # s = p.getUrlSchemeList(INPUT_URL)
    # links = p.getUrl(s)
    # print links

    # p.parse()
    # print p.mail
    # print p.http

if __name__ == "__main__":
    main()
