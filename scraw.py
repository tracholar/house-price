# coding:utf-8
import requests
import lxml
import Queue

root_urls = 'root_urls.txt'
visited_urls = 'data/visited_urls.txt'

url_queue = Queue()

def scraw_root(url):
    pass

def scraw_fangzi_info(url):
    pass
    
handlers = {
    'root' : scraw_root,
    'fangzi_info' : scraw_fangzi_info
}
def main():
    if url_queue.empty():
        return True

    url_type, url = url_queue.get()

    if url_type in handlers:
        handlers[url_type](url)
    return True



if __name__ == '__main__':
    for url in open(root_urls).read().split('\n'):
        url_queue.put(('root', url.strip()))

    main()
