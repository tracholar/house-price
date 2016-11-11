# coding:utf-8
import requests
import lxml
from Queue import Queue
from lxml import etree
from StringIO import StringIO
import re

root_urls = 'root_urls.txt'
visited_urls = 'data/visited_urls.txt'
data_file = 'data/res.csv'
fp = None

url_queue = Queue()

headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}

session = requests.session()

visited_urls_set = set(open(visited_urls).read().split('\n'))

def get_dom_from_string(html):
    try:
        tree = etree.parse(StringIO(html), etree.HTMLParser())
    except Exception:
        tree = None

    return tree

def dom_to_html(elem):
    return etree.tostring(elem, pretty_print=True)

def dom_text_content(elem, replace=''):
    if elem is None:
        return ''
    return re.sub(r'\s+', replace, etree.tostring(elem, method='text',encoding='unicode').strip())

def save_url(url):
    f = open(visited_urls,'a')
    f.write(url + '\n')
    f.close()

def save_data(data):
    global fp
    if fp is None:
        fp = open(data_file, 'a')
    fp.write(data)
    #fp.close()

def scraw_root(url):
    for i in range(1, 101):
        newurl = url + '/pg%d/' % i
        url_queue.put(('fangzi_info', newurl))



def scraw_fangzi_info(url):
    print 'scraw URL: %s' % url
    if url in visited_urls_set:
        return

    html = session.get(url, headers = headers)
    dom = get_dom_from_string(html.content)
    if dom is not None:
        lis = dom.findall('//li[@class="clear"]')
        if lis is not None:
            for li in lis:
                link = li.find('div/div[@class="title"]/a')
                title = link.text
                url = link.attrib['href']

                print title

                addr = dom_text_content(li.find('div/div[@class="address"]/div'))

                pos = dom_text_content(li.find('div/div[@class="flood"]/div'))

                followinfo = dom_text_content(li.find('div/div[@class="followInfo"]'))
                tag = dom_text_content(li.find('div/div[@class="tag"]'), '|')
                total_price = dom_text_content(li.find('div/div[@class="priceInfo"]/div[@class="totalPrice"]'))
                unit_price = dom_text_content(li.find('div/div[@class="priceInfo"]/div[@class="unitPrice"]'))

                data = [url, title, addr, pos, followinfo, tag, total_price, unit_price]
                raw = '\t'.join(data) + '\n'
                save_data(raw.encode('utf-8','ignore'))




handlers = {
    'root' : scraw_root,
    'fangzi_info' : scraw_fangzi_info
}
def main():
    while not url_queue.empty():
        url_type, url = url_queue.get()

        if url_type in handlers:
            handlers[url_type](url)
            save_url(url)
    return True



if __name__ == '__main__':
    for url in open(root_urls).read().split('\n'):
        if url.strip() == '':
            continue
        url_queue.put(('root', url.strip()))

    main()
