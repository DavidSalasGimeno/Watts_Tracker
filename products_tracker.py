import requests 
from time import sleep
from bs4 import BeautifulSoup



def getHtml(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',        
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)

    # Simple check to check if page was blocked (Usually 503)
    if 500 < r.status_code:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Parsing html
    html = BeautifulSoup(r.text,'html.parser')

    
    return html

    

def getFeatures(html):
    counter= float('inf')
    urls = html.select('.s-main-slot')
    html = ''
    
    for i in urls:
        
        html += str(i) 
    html = BeautifulSoup(html,'html.parser')
    urls = html.select('.a-link-normal')
    html = ''
    
    for i in urls:
        
        html += str(i) 
    html = BeautifulSoup(html,'html.parser')
    urls = html.select('.a-text-normal')
    url=[]

    for i in urls:
        o = BeautifulSoup(str(i),'html.parser').select('.a-link-normal .a-text-normal')
        if o != []:
            url.append(i)



    idx = 0
    for i in range(len(url)):

        url[i - idx] = url[i - idx].attrs['href']
        
        if url[i - idx][0] == '/':
            url[i - idx] = 'https://www.amazon.es' + url[i - idx]
        
        
        if len(url[i - idx]) < counter:
            counter = len(url[i - idx])
    for i in url:
        print(i + '\n')

def manager():
    html = getHtml('https://www.amazon.es/s?rh=n%3A14565215031&brr=1&pd_rd_r=65cb3175-d957-4fb4-a02b-536f48ebc2eb&pd_rd_w=Apy2S&pd_rd_wg=R4EBz&rd=1&ref=Oct_d_odnav_d_14565170031_0')
    getFeatures(html)

manager()
