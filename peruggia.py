import requests
from bs4 import BeautifulSoup
from PIL import Image
import re

# img = 'https://drogeriefiala.cz/files/i/10%20807.jpg'
kategorie_axn = {
    'duni':'MDAuMDF8ZHVuaXwwfDYzNXwyMg==',
    'katrin':'MDAuMDJ8a2F0cmlufDF8OTUzfDM=',
    'papirova-hygiena':'MDAuMDN8cGFwaXJvdmEtaHlnaWVuYXwxfDk1NHw0',
    'drogerie':'MDAuMDR8ZHJvZ2VyaWV8MXw2Njd8Mjg=',
    'kosmetika':'MDAuMDV8a29zbWV0aWthfDB8NjkxfDI4',
    'uklidove-ochranne-pomucky':'MDAuMDZ8dWtsaWRvdmUtb2NocmFubmUtcG9tdWNreXwwfDc2N3wyMQ==',
    'zahradni-sezonni-produkty':'MDAuMDd8emFocmFkbmktc2V6b25uaS1wcm9kdWt0eXwwfDg1M3w2',
    'technicke-kapaliny-lepidla':'MDAuMDh8dGVjaG5pY2tlLWthcGFsaW55LWxlcGlkbGF8MHw5MDJ8Mg',
    'drobna-elektronika':'',
    'dekorace-domacnost':'MDAuMTB8ZGVrb3JhY2UtZG9tYWNub3N0fDB8OTE2fDE1'
}

def drawBand(treshold, url):

        r = requests.get(url, stream = True)

        if r.ok:
            print(img['alt'])
            print(img['src'])
            im = Image.open(r.raw)
            px = im.load()
            width, height = im.size
            pasmo = ( round(width * treshold / 100 ) , round(width * ( 100 - treshold ) / 100 ) ), (round(height * treshold / 100 ), round(height * (100 - treshold) / 100 ))
            dim = []
            for y in range(height):
                if y < pasmo[1][0] or y > pasmo[1][1]:
                    for x in range(width):
                        if x < pasmo[0][0] or x > pasmo[0][1]:
                            r,g,b = px[x,y]
                            dim.append(f'[x={x},y={y}]:[r={r}, g={g}, b={b}]')
                            # print(f'[x={x},y={y}]:[r={r}, g={g}, b={b}]')

            print(f'Pocet pixelu v sirce pasma {treshold}%: {len(dim)}')
            print(f'Celkove rozliseni obrazu: {width}x{height}')
            print('-'*60)

rootDir = 'https://drogeriefiala.cz/'
treshold = 3
productList = rootDir+'productlistnext.php?axn='
s = requests.Session()
reqNum = 0

for link, axn in kategorie_axn.items():
    print('='*92)
    print(link.upper().center(92))
    print('='*92)
    r = requests.get(rootDir+link)
    if r.ok:
        source = BeautifulSoup(r.text, 'lxml')

        if source.find('div', class_ = 'dd'):
            lenOfPages = source.find('div', class_ = 'dd').text
            num = int(''.join(re.findall(r'[0-9]',lenOfPages)))
        else:
            num = 0

        glRequest = productList + axn

        for i in range(num // 24 + 1):
            glResponse = s.get(glRequest).text
            bs = BeautifulSoup(glResponse,'lxml')
            for img in bs.find_all('img'):
                reqNum += 1
                drawBand(treshold, img['src'])

print(reqNum)
