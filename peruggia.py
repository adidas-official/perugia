import requests
from bs4 import BeautifulSoup
from PIL import Image

# img = 'https://drogeriefiala.cz/files/i/10%20807.jpg'
print('Start')

rootDir = 'https://drogeriefiala.cz'
# source = requests.get(rootDir).text
# soup = BeautifulSoup(source, 'lxml')
# l = soup.find('ul', class_='m')
# anchors = l.find_all('a')
# for a in anchors:
#     url = rootDir+a['href']
#     print(url)
#     r = requests.get(url).text
#     s = BeautifulSoup(r,'lxml')

r = requests.get(rootDir+'/duni')
if r.ok:
    source = BeautifulSoup(r.text, 'lxml')
    lenOfPages = source.find('div', class_ = 'dd').text
    print(lenOfPages)
    # print(len(source.text))
    axn = 'MDAuMDF8ZHVuaXwwfDYzNXwyMg=='
    goload = 'https://drogeriefiala.cz/productlistnext.php?axn='+axn
    s = requests.Session()
    gl = s.get(goload).text


url = rootDir + '/files/i/'
treshold = 3

def drawBand(treshold, url):

    for i in range(610, 2000):
        fpath = list(f'{i:,}')
        new_fpath = [sub.replace(',', ' ') for sub in fpath]
        img = ''.join(new_fpath) + '.jpg'
        u = url+img
        r = requests.get(u, stream = True)

        '''
        ###########
        #.........#
        #.........#
        #.........#
        #.........#
        ###########
        '''
        if r.ok:
            print(img)
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

# drawBand(treshold, url)
