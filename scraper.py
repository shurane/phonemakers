import bs4
import requests
import tld
import errno
import itertools
import os
import re
import urlparse
from collections import defaultdict

import logging
logging.basicConfig(filename="cache/error.log")

"""
This grabs the phone data from GSMArena. It goes through a list of makers,
then goes through the list of phones by each maker, and then pulls out
whatever specs GSMArena lists for said phones.

The goal of this project is to make more informed data about which phones to
buy. You can filter by what operating system it has, when it was released,
whether it supports and SD card, the diagonal size of the screen, and more.
This relies entirely on the data from GSMArena and similar websites

Now we have all the details on a per-phone basis. Wonderful.

TODO:
YhG1s and cdunklau from #python suggest me using Scrapy instead of
BeautifulSoup + requests
"""

# http://stackoverflow.com/a/600612/198348
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

URL = "http://www.gsmarena.com/makers.php3"
TLD_URL = tld.get_tld(URL)
USER_AGENT = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.49 Safari/537.36"

HEADERS = { "User-Agent" : USER_AGENT
           , "Accept" : "text/html" }
CACHE = "./cache"
# I wonder if there's a more clever way than using 'directory'
CACHE_MAKERS = "{0}/makers".format(CACHE)
CACHE_PHONES = "{0}/phones".format(CACHE)
mkdir_p(CACHE)
mkdir_p(CACHE_MAKERS)
mkdir_p(CACHE_PHONES)

def rget(url, directory=CACHE, **kwargs):
    # if cached, open cached file instead of using requests
    urlpath = urlparse.urlparse(url).path.strip("/")
    urlpath = os.path.join(directory, urlpath)
    try:
        return open(urlpath).read()
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise

        r = requests.get(url,headers=HEADERS,**kwargs)
        with open(urlpath,"w") as f:
            # I'm confused! YEAARGH isn't utf-8 automatic in requests?
            # http://stackoverflow.com/a/9942822/198348
            f.write(r.text.encode("utf-8").strip())
        return r.text


def cleanse(string):
    string = re.sub("\xa0","",string)
    string = re.sub("\r\n","\n",string)
    string = string.strip()
    return string

class Maker(object):
    def __init__(self,name,url):
        self.name = name
        self.url = url
    def __str__(self):
        return "<Maker({0},{1})>".format(self.name,self.url)
    def __repr__(self):
        return str(self)

    def get_phones(self):
        rtext = rget(self.url, directory=CACHE_MAKERS)
        soup = bs4.BeautifulSoup(rtext)
        phones = soup.select("#main .makers > ul > li > a")
        results = []
        for phone in phones:
            name = phone.strong.text
            href = "http://{0}/{1}".format(TLD_URL,phone.attrs["href"])
            results.append(Phone(name,href))

        return results

class Phone(object):
    def __init__(self,name,url):
        self.name = name
        self.url = url
        self.fields = {}
        self.description = ""
    def __str__(self):
        return "<Phone({0},{1})>".format(self.name,self.url)
    def __repr__(self):
        return str(self)
    def get_page(self):
        rtext = rget(self.url,directory=CACHE_PHONES)
        soup = bs4.BeautifulSoup(rtext)
        description = soup.select("#specs-list > p")
        self.description = description[0].text if description else None

        tables = soup.select("table")
        for table in tables:
            title = table.th.text
            subvalues = itertools.izip(table.select(".ttl"),
                                       table.select(".nfo"))
            subdict = {}
            sections_with_emptykey = defaultdict(int)
            for key, value in subvalues:
                clean_key = cleanse(key.text)
                clean_value = cleanse(value.text)
                subdict[clean_key] = clean_value

                if not clean_key:
                    sections_with_emptykey[title] += 1

            if sections_with_emptykey:
                logging.warn("{0}: Sections with empty keys\n{1}"
                             .format(self,sections_with_emptykey))

            self.fields[title] = subdict

        pass

def get_makers(url):
    rtext = rget(url)
    root_soup = bs4.BeautifulSoup(rtext)
    makers = root_soup.select("#main tr > td > a")
    results = []
    # every other element is a duplicate
    for maker in makers[::2]:
        href = "http://{0}/{1}".format(TLD_URL,maker.attrs["href"])
        name = maker.img.attrs["alt"]
        m = Maker(name,href)
        results.append(m)

    return results


if __name__ == "__main__":

    makers = get_makers(URL)
    mdict = {}

    print("#Brands")
    for maker in makers:
        print("Working on " + maker.name)
        mdict[maker.name] = maker.get_phones()

    print("#Phones")
    phones = list(itertools.chain(*mdict.values()))
    for phone in itertools.islice(phones,50):
        print("Working on " + phone.name)
        try:
            phone.get_page()
        except Exception as e:
            logging.error("encountered exception for {0}", phone.name)
            logging.exception(e)
        pass

