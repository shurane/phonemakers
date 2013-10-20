import bs4
import requests
import requests_cache
import tld
import multiprocessing
requests_cache.install_cache("phonemakers.cache")

URL = "http://www.gsmarena.com/makers.php3"
TLD_URL = tld.get_tld(URL)
USER_AGENT = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.49 Safari/537.36"

HEADERS = { "User-Agent" : USER_AGENT
           , "Accept" : "text/html" }

def grab_url(url):
    print("working on {0}".format(url))
    return requests.get(url)

def get_makers(root_soup):
    makers = soup.select("#main tr > td > a")
    hrefs= []
    # every other element is a duplicate
    for maker in makers[::2]:
        hrefs.append("http://{0}/{1}".format(TLD_URL,maker.attrs["href"]))

    return hrefs

def get_phones(maker_soup):
    phones = maker_soup.select("#main .makers > ul > li")
    hrefs = []
    for phone in phones:
        hrefs.append("http://{0}/{1}".format(TLD_URL,phone.a.attrs["href"]))

    return hrefs

if __name__ == "__main__":

    r = requests.get(URL)
    soup = bs4.BeautifulSoup(r.text)

    #makers = soup.select("#main tr > td > a")
    #phonemaker_hrefs= []
    ## every other element is a duplicate
    #for maker in makers[::2]:
        #phonemaker_hrefs.append("http://{0}/{1}".format(TLD_URL,maker.attrs["href"]))

    makers = get_makers(soup)

    #pool = multiprocessing.Pool(processes=10)
    #phonemaker_pages = pool.map(grab_url, phonemaker_hrefs)

    acer_phones = open("acer-phones-59.php").read()
    acer_soup = bs4.BeautifulSoup(acer_phones)

    phones = acer_soup.select("#main .makers > ul > li")
    phone_hrefs = []
    for phone in phones:
        phone_hrefs.append("http://{0}/{1}".format(TLD_URL,phone.a.attrs["href"]))

