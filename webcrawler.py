#!/usr/bin/python
import requests
import bs4
import urlparse

INPUT_URL = 'http://www.duerrdental.com'
# INPUT_URL = 'http://www.bitshift-dynamics.de/'
# INPUT_URL = 'http://chris-maier.com'

class Page:
    def __init__(self, URL):
        # self.URL = URL
        self.BASE_URL = urlparse.urlparse(URL).netloc
        self.mail = set()
        self.httpList = set()
        self.httpExtList = set()
        self.count = 0

    def parse(self, urlList):
        for link in urlList:
            if not (link in self.httpList):
                s = self.getUrlSchemeList(link)
                l = self.getUrl(s)
                # obtain external URL's
                self.httpExtList.update(self.getExtUrl(s))
                # obtain Email addresses
                self.mail.update(self.getEmail(s))
                # print "Obtained links: " + str(l)
                self.httpList.add(link)
                self.parse(l)


    def getUrlSchemeList(self, URL):
        scheme = list()

        # HTTP request
        res = requests.get(URL)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('Execption: %s' % (exc))

        # parse HTML
        s = bs4.BeautifulSoup(res.text, "lxml")

        # retrieve all <a> tags
        tags = s.select('a')

        for tag in tags:
            a = tag.get('href')

            # skip empty <a>
            if a == None:
                continue

            scheme.append (urlparse.urlparse(a))
        return scheme

    def getEmail(self, schemeList):
        l = set()
        for scheme in schemeList:
            if scheme.scheme == 'mailto':
                l.add(urlparse.urlunparse(scheme))
                # self.mail.add(scheme.path)
        return l

    def getUrl(self, schemeList):
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
    p = Page(INPUT_URL)
    linklist = [INPUT_URL]
    p.parse(linklist)

    p.printVisitedLinks()
    p.printExtLinks()
    p.printEmails()

    # s = p.getUrlSchemeList(INPUT_URL)
    # links = p.getUrl(s)
    # print links

    # p.parse()
    # print p.mail
    # print p.http

if __name__ == "__main__":
    main()
