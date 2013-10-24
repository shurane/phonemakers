import bs4
import requests
import requests_cache
import tld
import itertools
import re
import warnings
requests_cache.install_cache("phonemakers.cache")

"""
This grabs the phone data from GSMArena. It goes through a list of makers,
then goes through the list of phones by each maker, and then pulls out
whatever specs GSMArena lists for said phones.

The goal of this project is to make more informed data about which phones to
buy. You can filter by what operating system it has, when it was released,
whether it supports and SD card, the diagonal size of the screen, and more.
This relies entirely on the data from GSMArena and similar websites

#TODO:
What details do we care about?
    - model name
    - phone carriers supported on ( or unlocked)
    - SIM card type ( if available)
    - announce date
    - release date
    - weight
    - colors
    - hardware specs
        - phone dimensions
        - screen dimensions, pixel density
        - microsd card slot
        - internal storage options
        - RAM amount
        - NFC support
        - Bluetooth version
        - Camera [ primary, secondary ]
        - Android OS shipped with, list of OTA updates
        - CPU
        - GPU
        - sensors
        - GPS
        - endurance rating
        - standard battery
"""

URL = "http://www.gsmarena.com/makers.php3"
TLD_URL = tld.get_tld(URL)
USER_AGENT = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.49 Safari/537.36"

HEADERS = { "User-Agent" : USER_AGENT
           , "Accept" : "text/html" }

def rget(url, **kwargs):
    return requests.get(url,headers=HEADERS,**kwargs)

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
        r = rget(self.url)
        soup = bs4.BeautifulSoup(r.text)
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
        r = rget(self.url)
        soup = bs4.BeautifulSoup(r.text)
        description = soup.select("#specs-list > p")
        self.description = description[0].text if description else None

        tables = soup.select("table")
        for table in tables:
            title = table.th.text
            subvalues = itertools.izip(table.select(".ttl"),
                                       table.select(".nfo"))
            subdict = {}
            for key, value in subvalues:
                clean_key = cleanse(key.text)
                clean_value = cleanse(value.text)
                if not clean_key:
                    warnings.warn("Empty key. '{0}'->('{1}':'{2}')"
                                  .format(title, clean_key, clean_value))
                subdict[clean_key] = clean_value

            self.fields[title] = subdict

        pass

def get_makers(url):
    r = rget(url)
    root_soup = bs4.BeautifulSoup(r.text)
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

    #makers = get_makers(URL)
    #mdict = {}

    #for maker in makers:
        #print("Working on " + maker.name)
        #mdict[maker.name] = maker.get_phones()

    #phones = list(itertools.chain(*mdict.values()))
    #for phone in phones:
        #time.sleep(0.2)
        #pass
    pass

