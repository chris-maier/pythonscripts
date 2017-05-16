#!/usr/bin/python
import requests
import bs4
import urlparse

# INPUT_URL = 'http://www.duerrdental.com'
INPUT_URL = 'http://www.bitshift-dynamics.de/'

class Page:
    def __init__(self, URL):
        self.URL = URL
        self.BASE_URL = urlparse.urlparse(URL).netloc
        self.mail = set()
        self.httpList = set()
        self.httpExtList = set()

    def parse(self, urlList):
        for link in urlList:
            if link is not in self.httpList:
                print link
                self.httpList.add(link)


    def getUrlSchemeList(self, URL):
        scheme = list()

        # HTTP request
        res = requests.get(URL)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('%s' % (exc))

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
        for scheme in schemeList:
            if scheme.scheme == 'mailto':
                self.mail.add(scheme.path)

    def getUrl(self, schemeList):
        for scheme in schemeList:
            if (scheme.netloc == BASE_URL or scheme.netloc == '') and \
               (scheme.scheme == 'http' or scheme.scheme == 'https'):
                self.httpList.add(scheme.path)

    def getExtUrl(self, schemeList):
        for scheme in schemeList:
            if scheme.netloc != BASE_URL and (scheme.scheme == 'http' or scheme.scheme == 'https'):
                self.httpExtList.add(scheme.netloc + scheme.path)

def main():
    p = Page(INPUT_URL)
    p.parseURL()
    print p.mail
    print p.http

if __name__ == "__main__":
    main()
