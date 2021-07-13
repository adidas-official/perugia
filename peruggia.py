import requests
from bs4 import BeautifulSoup
from PIL import Image
import re

kategorie_axn = {
    # 'duni':'MDAuMDF8ZHVuaXwwfDYzNXwyMg==',
    'katrin':'MDAuMDJ8a2F0cmlufDF8OTUzfDM='
    # 'papirova-hygiena':'MDAuMDN8cGFwaXJvdmEtaHlnaWVuYXwxfDk1NHw0',
    # 'drogerie':'MDAuMDR8ZHJvZ2VyaWV8MXw2Njd8Mjg=',
    # 'kosmetika':'MDAuMDV8a29zbWV0aWthfDB8NjkxfDI4',
    # 'uklidove-ochranne-pomucky':'MDAuMDZ8dWtsaWRvdmUtb2NocmFubmUtcG9tdWNreXwwfDc2N3wyMQ==',
    # 'zahradni-sezonni-produkty':'MDAuMDd8emFocmFkbmktc2V6b25uaS1wcm9kdWt0eXwwfDg1M3w2',
    # 'technicke-kapaliny-lepidla':'MDAuMDh8dGVjaG5pY2tlLWthcGFsaW55LWxlcGlkbGF8MHw5MDJ8Mg',
    # 'drobna-elektronika':'',
    # 'dekorace-domacnost':'MDAuMTB8ZGVrb3JhY2UtZG9tYWNub3N0fDB8OTE2fDE1'
}


def checkColor(image):
    l = []

    r = requests.get(image,stream=True)
    if r.ok:
        # print(image)
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
            print(f'Pos:({x};{y}), rgb: {px[x,y]}')
            for rgb in px[x,y]:
                if rgb < 252:
                    print(f'Not white: ({x};{y}), rgb: {px[x,y]}')
                    return 0
                    break


def run():
    rootDir = 'https://drogeriefiala.cz/'
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
                        print(url)
                        nonWhite += 1


    print(reqNum)
    print(nonWhite)


img = 'https://drogeriefiala.cz/files/i/89735.jpg'
checkColor(img)

# run()


