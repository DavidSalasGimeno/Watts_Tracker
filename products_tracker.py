import requests 
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
    #print("Downloading %s"%url)
    
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

    

def getUrls(url, number=33):
    html = getHtml(url)
    urls = html.select('.a-link-normal.a-text-normal')
    titles = html.select('.a-size-base-plus.a-color-base.a-text-normal')
    urls = urls[::2]
    for i in range(number):

        urls[i] = urls[i].attrs['href']

        if number == 1 and urls[i][:4] == '/gp/':

            return False


        
        elif urls[i][:4] == '/gp/':
            urls[i] = getUrls('https://www.amazon.es/s?k=' + titles[i].string, 1)

            if urls[i]:
                urls[i] = 'https://www.amazon.es' + urls[i][0]
                
            else:
                urls[i] = None

        else:
            urls[i] = 'https://www.amazon.es' + urls[i]


    

    return urls


def getFeatures(url):
    html = getHtml(url)


    title = html.find("span", {"id": "productTitle"}).string.replace('\n','')



    stars = html.select('.a-icon-alt')
    stars = stars[0].string
    stars = stars[0:3]
    stars = stars.replace(',', '.')
    stars = float(stars)


    prize = html.select('.a-offscreen')
    prize = prize[0].string
    prize = prize.replace('.', '')
    prize = prize.replace(',', '.')
    prize = prize.replace('€', '')
    prize = float(prize)




def manager(url):
    
    urls = getUrls(url)

    for url in urls:

        features = getFeatures(url)
        break
        




