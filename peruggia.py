import requests
from bs4 import BeautifulSoup
from PIL import Image
import re

# img = 'https://drogeriefiala.cz/files/i/10%20807.jpg'
kategorie_axn = {
    # 'duni':'MDAuMDF8ZHVuaXwwfDYzNXwyMg==',
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
            # print(img['alt'])
            # print(url)
            im = Image.open(r.raw)
            px = im.load()
            width, height = im.size
            # pasmo = ( round(width * treshold / 100 ) , round(width * ( 100 - treshold ) / 100 ) ), (round(height * treshold / 100 ), round(height * (100 - treshold) / 100 ))
            pasmo = ( (1, width - 1), (1, height - 1) )
            dim = []
            totalPix = 0
            notWhite = 0
            for y in range(height):
                for x in range(width):
                    if y < pasmo[1][0] or y > pasmo[1][1] or x < pasmo[0][0] or x > pasmo[0][1]:
                        totalPix += 1
                        for pixVal in px[x,y]:
                            if pixVal < 253:
                                # brightness = pixVal // 256 * 100
                                notWhite += 1
                                break



            # print(f'Pocet pixelu v sirce pasma {treshold}%: {totalPix}')
            # print(f'Z toho {notWhite / totalPix * 100}% NEMA bilou barvu')
            # print(f'Celkove rozliseni obrazu: {width}x{height}')
            # print('-'*60)

            if notWhite / totalPix > 0.1:
                print(img['alt'])
                print(url)
                print(f'{notWhite} / {totalPix}')
                print()
                return 1
            else:
                return 0

def checkColor(image):
    l = []

    r = requests.get(image,stream=True)
    if r.ok:
        print(image)
        i = Image.open(r.raw)
        px = i.load()
        width = i.size[0]
        height = i.size[1]

        for x in range(width):
            l.append((x,0))
            if x < width-1:
                l.append((x,height-1))


        for y in range(1,height):
            if y < height-1:
                l.append((0,y))
            l.append((width-1,y))

        l.sort(key=lambda tup: tup[1])

        for x,y in l:
            # print(f'Pos:({x};{y}), rgb: {px[x,y]}')
            for rgb in px[x,y]:
                if rgb < 252:
                    print(f'{x},{y}: {px[x,y]}')
                    print('Not white')
                    return 0

rootDir = 'https://drogeriefiala.cz/'
# treshold = 0.25
productList = rootDir+'productlistnext.php?axn='
s = requests.Session()
reqNum = 0
nonWhite = 0

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
                url = str(img['src']).replace('._','')
                # print(url)
                reqNum += 1
                if checkColor(url) == False:
                    nonWhite += 1
                # drawBand(1,url)


print(reqNum)
print(nonWhite)

img = 'https://drogeriefiala.cz/files/i/104513.jpg'
# img = 'https://drogeriefiala.cz/files/i/168272.jpg'

# checkColor(img)




# i = Image.open('image-test-rect-01.jpg')

# px = i.load()
# print(i.size)
# for x in range(i.size[0]):
#     print(x, px[x,1])

