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

INPUT_URL = 'http://www.duerrdental.com'
# INPUT_URL = 'http://www.bitshift-dynamics.de/'
# INPUT_URL = 'http://chris-maier.com'

class Crawler:
    """This class crawles the web page."""

    def __init__(self, url):
        """Ctor - Setup the basic variables."""
        self.URL = url
        self.BASE_URL = urlparse.urlparse(url).netloc
        self.mail = set()
        self.httpList = set()
        self.httpExtList = set()

    def parse(self, urllist = None):
        """This function does the heavy lifting.

        Iterates over the `urlList`, check if link was already processed and process it

        Args:
            urllist (:obj:`list` of :obj:`str`): List of URL's to process
        """
        if urllist == None:
            urllist = [self.URL]

        for link in urllist:
            if not (link in self.httpList):
                print link

                dom = self.getHtmlDom(link)

                s = self.getUrlList(dom)
                print s

                # obtain external URL's
                # self.httpList.update(self.getIntUrl(s))

                # obtain Email addresses
                # self.mail.update(self.getEmail(s))
                # print "Obtained links: " + str(l)




                # mark link as visited
                self.httpList.add(link)
                # recursive call with list of links
                self.parse()


                # l = self.getUrl(s)
                # self.parse(l)

    def getHtmlDom(self, url):
        """Send HTML request and process the received HTML DOM.

        Args:
            url (:obj:`str`): string of the URL
        """
        res = requests.get(url)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('Execption: %s' % (exc))

        return bs4.BeautifulSoup(res.text, "lxml")


    def getUrlList(self, dom):
        """Obtain every 'href' HTML tag from the HTML DOM

        Args:
            dom (:obj:`bs4.BeautifulSoup`): HTML DOM
        """
        l = list()

        # retrieve all <a> tags
        for tag in (dom.select('a')):
            a = tag.get('href')

            # skip empty <a>
            if a == None:
                continue

            l.append (urlparse.urlparse(a))
        return l

    def getIntUrl(self, schemeList):
        l = set()
        for scheme in schemeList:
            # print "Scheme: " + str(scheme)
            if (scheme.netloc == self.BASE_URL or scheme.netloc == ''):
                # urlunparse helps to strip the URL
                l.add(urlparse.urlunparse(scheme))
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
        self.httpList = sorted(self.httpList)
        for h in self.httpList:
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
