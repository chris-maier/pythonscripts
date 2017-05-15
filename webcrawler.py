#!/usr/bin/python
import requests
import bs4
import urlparse

# INPUT_URL = 'http://www.duerrdental.com'
INPUT_URL = 'http://www.bitshift-dynamics.de/'

class Page:
    def __init__(self, URL):
        # self.URL = URL
        # self.BASE_URL = urlparse.urlparse(URL).netloc
        self.mail = set()
        # self.http = set()
        # self.http_ext = set()

    def parseURL(self, URL):
        http_result = set()
        BASE_URL = urlparse.urlparse(URL).netloc

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

            pr = urlparse.urlparse(a)

            if pr.scheme == 'mailto':
                self.mail.add(pr.path)
            elif (pr.netloc == BASE_URL or pr.netloc == '') and \
                (pr.scheme == 'http' or pr.scheme == 'https'):
                http_result.add(pr.path)
            # elif pr.netloc != BASE_URL and (pr.scheme == 'http' or pr.scheme == 'https'):
                # self.http_ext.add(pr.netloc + pr.path)
            # # else
                # # skip


    def parse_rec(self, URL):


def main():
    p = Page(INPUT_URL)
    p.parse()
    print p.mail
    print p.http


if __name__ == "__main__":
    main()


