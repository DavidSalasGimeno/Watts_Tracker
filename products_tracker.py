import requests 
from bs4 import BeautifulSoup
import wget
import image_reader
from time import sleep
import sqlite3

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

    

def getUrls(url, number=24):
    html = getHtml(url)
    urls = html.select('.a-link-normal.a-text-normal')
    titles = html.select('.a-size-base-plus.a-color-base.a-text-normal')
    urls = urls[::2]
    if number != 1:
        number = len(urls)
    for i in range(number):

        urls[i] = urls[i].attrs['href']

        if number == 1 and urls[i][:4] == '/gp/':

            return False


        
        elif urls[i][:4] == '/gp/':
            urls[i] = getUrls('https://www.amazon.es/s?k=' + titles[i].string, 1)

            if urls[i] and urls[i][:4] != 'http':
                urls[i] = urls[i][0]
                
            else:
                urls[i] = None

        

        elif urls[i][:4] != 'http':

            urls[i] = 'https://www.amazon.es' + urls[i]


    

    return urls


def getFeatures(url):
    
    html = getHtml(url)


    title = html.find("span", {"id": "productTitle"}).string.replace('\n','')


    try:
        stars = html.select('.a-icon-alt')
        stars = stars[0].string
        stars = stars[0:3]
        stars = stars.replace(',', '.')
        stars = float(stars)
    except:
        stars = None

    prize = html.select('.a-offscreen')
    prize = prize[0].string
    prize = prize.replace('.', '')
    prize = prize.replace(',', '.')
    prize = prize.replace('€', '')
    prize = float(prize)

    severalFeautes = html.select('tr.a-spacing-small')
    brand = None
    capacity = None
    try:
        for i in range(len(severalFeautes)):

            featureName = severalFeautes[i].select('td')[0].select('span')[0].string
            if featureName == 'Marca':
                brand = severalFeautes[i].select('td')[1].select('span')[0].string
            elif featureName == 'Capacidad':
                capacity = severalFeautes[i].select('td')[1].select('span')[0].string
    except:
        brand = None
        capacity = None


    try:
        img = html.select('#energy_guide_image')[0].attrs['src']
        imgName = img[36:]
        imgName = wget.download(img)

        cost = image_reader.read_img(imgName)
    except:
        return None
    

    
    return [title[:15], img, stars, capacity, prize, cost]


    


def manager(url):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    
    

    for page in range(1,10):
        urls = getUrls('https://www.amazon.es/s?i=appliances&rh=n%3A14565215031&page=' + str(page) + '&brr=1&pd_rd_r=bcfe237f-ff0f-4df5-af35-507a00f1dfa0&pd_rd_w=Zbnoz&pd_rd_wg=K8JCE&qid=1638545572&rd=1&ref=sr_pg_2')


        for url in urls:
            if url == None:
                continue
            print(url)
            features = getFeatures(url)
            print(features, '        ', page)
            r = 0
            if features == None:
                continue
            for i in features:
                if i is None:
                    r = 1
            if r:
                continue
            cur.execute("INSERT INTO Fridges VALUES ('"+ features[0] +"','"+ features[1] +"',"+ str(features[2]) +"," + str(features[-1]) +", "+ str(features[-2])+")")
    con.commit()
    con.close()
            
        

        

manager('https://www.amazon.es/s?i=appliances&bbn=14565215031&rh=n%3A4772050031%2Cn%3A14565170031%2Cn%3A14565215031%2Cn%3A14565324031&dc&brr=1&pd_rd_r=72ba1ed9-7112-4a12-9a0c-e8474a9239f6&pd_rd_w=z5r2h&pd_rd_wg=ShPae&qid=1638396500&rd=1&rnid=14565215031&ref=sr_nr_n_2')


